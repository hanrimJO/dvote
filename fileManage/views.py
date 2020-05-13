# from rest_framework import viewsets
# import json
# import base64
# from .serializers import ChallengeRecordSerializer, UploadedFileSerializer
# from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render, HttpResponse
from .models import *
from .result_validate import result_validate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.db import connection
import subprocess
import after_response
import sys


@after_response.enable
def verify(upload_id, member_id, selected_precinct_id):
    today = datetime.now()
    today_date = f"{today.year}_{today.month}_{today.day}"

    member_email = Member.objects.get(member_id=member_id).email
    #    file_name = Upload.objects.get(
    #        upload_id=upload_id, member_id=member_id
    #    ).file_name  # type: str

    file_location = Upload.objects.get(
        upload_id=upload_id, member_id=member_id
    ).file_location  # type: FieldFile

    file_name = file_location.split('/')[-1]

    # 참가자가 업로드한 .ipynb 파일을 data 폴더로 복사하기
    copy = subprocess.run(
        f"cp {file_location} /tmp/{member_id}/data/{file_name}".split()
    )

    # 금지 단어 필터링하기
    with open(f'/tmp/{member_id}/data/{file_name}') as f:
        contents = f.read()

    bans = ['sudo', 'system', 'kill', 'rm']

    contents = contents.replace('\\', ' ').replace('#', ' ').replace('/', ' ').replace('!', ' ').replace('=',
                                                                                                         ' ').replace(
        '-', ' ').replace('.', ' ').replace(',', ' ').replace(':', ' ').replace(';', ' ').replace("'", ' ').replace('"',
                                                                                                                    ' ').replace(
        '(', ' ').replace(')', ' ').replace('[', ' ').replace(']', ' ').replace('{', ' ').replace('}', ' ').split()

    result = [(ban, '존재') for ban in bans if ban in contents]

    if len(result) != 0:
        result_status = '비정상분석'
        result_description = '금지단어가발견됐습니다.'

        with open(f"./logs/log.txt", "at") as file:
            file.write(
                f"<[{datetime.now()}] {member_email} {result_status} {result_description}>\n"
            )

        sys.exit(0)

    # data 폴더로 복사해온 .ipynb 파일을 .py로 변환하기 (by 서브프로세스)
    process = subprocess.run(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "python",
            f"/tmp/{member_id}/data/{file_name}",
        ],
        # capture_output=True,
        encoding="utf-8",
    )

    # 파일명과 확장자 분리하기
    FILE_NAME = file_name[:-6]

    # 변환된 .py를 실행하기 (by 서브프로세스)
    excute = subprocess.Popen(
        ["python", f"/tmp/{member_id}/data/{FILE_NAME}.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )

    # 서브프로세스에서 출력되는 에러 메시지 받아오기
    # output_msg = excute.stdout.read()
    error_msg = excute.stderr.read()

    print('error_msg: ', error_msg)

    # 컴파일 에러가 발생했을 경우 로그 작성하기
    if error_msg != "":
        result_status = "컴파일에러"
        result_description = error_msg.replace(" ", "").replace("\n", "")

        with open(f"./logs/log.txt", "at") as file:
            file.write(
                f"<[{datetime.now()}] {member_email} {result_status} {result_description}>\n"
            )

    try:
        # 최종 결과가 기록되어 있는 result.txt 파일을 열어서 분석 결과값을 읽어 온다. ex) 강남구 값, 홍길동
        with open(f"/tmp/{member_id}/data/result.txt", "r") as file:
            result = file.read()

        precinct, candidate = result.split(", ")

        precinct = precinct.replace(' ', '')
        candidate = candidate.replace(' ', '')

    except Exception:
        # Exception : [Errno 2] No such file or directory: './temp/{member_id}/data/result.txt'
        # 복사해 온 .ipynb 파일과 변환된 .py 파일 삭제하기

        print("check 01")
        excute = subprocess.Popen(
            f"rm -r /tmp/{member_id}/data/{FILE_NAME}.ipynb /tmp/{member_id}/data/{FILE_NAME}.py".split()
        )

        print("check 02")

        # 컴파일에러는 없으나 result.txt를 쓰지 못한경우 (파일 분석 내용이 없는경우 등)

        try:
            if result_status:
                pass
        except:
            result_status = '컴파일에러'
            result_description = '분석내용이없습니다'
            with open(f"./logs/log.txt", "at") as file:
                file.write(
                    f"<[{datetime.now()}] {member_email} {result_status} {result_description}>\n"
                )

        with connection.cursor() as cursor:
            print("cursor 진입")
            cursor.execute("SELECT next_val FROM hibernate_sequence FOR UPDATE;")
            challenge_record_id = cursor.fetchall()[0][0]
            print(challenge_record_id)
            cursor.execute(f"UPDATE hibernate_sequence SET next_val = {challenge_record_id}+1;")
            cursor.fetchone()

        row = ChallengeRecord(
            challenge_record_id=challenge_record_id,
            admin_check=0,
            precinct_id=selected_precinct_id,
            member_id=member_id,
            upload_upload_id=upload_id,
            result_status=result_status,
            result_description=result_description
        )
        row.save()

        print("check 03")
        sys.exit(0)

    # 분석 결과값(지역구와 후보명) 검증하기
    valid_result, error_msg = result_validate(precinct, candidate, selected_precinct_id)

    validation = True if error_msg == "" else False

    # 분석 결과값 검증을 통과 했다면 upload 테이블과 challenge_record 테이블에 값 반영하기
    if valid_result:
        result_status = "정상처리"

        uploadRow = Upload.objects.get(upload_id=upload_id)
        uploadRow.validation = True  # True
        uploadRow.save()

        precinct_id = Precinct.objects.get(precinct_name=precinct).precinct_id
        candidate_id = Candidate.objects.get(candidate_name__icontains=candidate).candidate_id

        # 정상적인 분석 결과를 ChallengeRankingBoard 테이블에 반영한다.
        challenge_ranking_board_id = Member.objects.get(
            member_id=member_id).challenge_ranking_board_challenge_ranking_board_id
        total_precinct_id_list = ChallengeRecord.objects.filter(member_id=member_id, result_status='정상처리').values_list(
            'precinct_id', flat=True)

        vote_result_id = Candidate.objects.get(candidate_id=candidate_id).vote_result_vote_result_id

        print(precinct_id, candidate_id, challenge_ranking_board_id, total_precinct_id_list)

        boardRow = ChallengeRankingBoard.objects.get(challenge_ranking_board_id=challenge_ranking_board_id)

        # 현재 투표한 지역구를 이전에 투표한 기록이 있는가?
        if precinct_id in total_precinct_id_list:
            # 이미 기존에 투표했던 지역구이므로 투표수만 +1 증가
            # boardRow = ChallengeRankingBoard.objects.get(challenge_ranking_board_id = challenge_ranking_board_id)
            boardRow.count += 1

            q = ChallengeRecord.objects.filter(member_id=member_id, precinct_id=precinct_id, result_status='정상처리')
            latest_candidate_id = q.order_by('-created_date')[0].candidate_id

            # 같은 지역구를 투표했다면 가장 최근에 투표한 후보자와 현재 투표한 후보자가 다른 경우
            if latest_candidate_id != candidate_id:
                # 이전에 투표받았던 후보자의 카운트를 -1 차감
                latest_vote_result_id = Candidate.objects.get(
                    candidate_id=latest_candidate_id).vote_result_vote_result_id
                prevRow = VoteResult.objects.get(vote_result_id=latest_vote_result_id)
                prevRow.count -= 1

                prevRow.save()

                # 현재 투표받은 후보자의 카운트를 +1 증가
                nowRow = VoteResult.objects.get(vote_result_id=vote_result_id)
                nowRow.count += 1

                nowRow.save()
        else:
            # 현재 투표한 지역구가 최초 투표 지역구이기 때문에 지역구와 투표수를 +1 증가
            boardRow.precinct_count += 1
            boardRow.count += 1

            # 최초로 투표받은 후보자이기 때문에 카운트를 +1 증가
            voteRow = VoteResult.objects.get(vote_result_id=vote_result_id)
            voteRow.count += 1

            voteRow.save()

        boardRow.save()
    else:
        precinct_id = selected_precinct_id
        candidate_id = None
        result_status = "비정상분석"

    # 분석 결과값 검증에서 오류가 있는 경우 로그 작성하기
    result_description = error_msg.replace(" ", "").replace("\n", "")

    with open(f"./logs/log.txt", "at") as file:
        file.write(
            f"<[{datetime.now()}] {member_email} {result_status} {result_description}>\n"
        )

    # 복사해 온 .ipynb 파일과 변환된 .py 파일 삭제하기
    print("check04")
    excute = subprocess.Popen(
        f"rm -r /tmp/{member_id}/data/result.txt /tmp/{member_id}/data/{FILE_NAME}.ipynb /tmp/{member_id}/data/{FILE_NAME}.py".split()
    )

    print("check05")
    with connection.cursor() as cursor:
        print("cursor 진입")
        cursor.execute("SELECT next_val FROM hibernate_sequence FOR UPDATE;")
        challenge_record_id = cursor.fetchall()[0][0]
        print(challenge_record_id)
        cursor.execute(f"UPDATE hibernate_sequence SET next_val = {challenge_record_id}+1;")
        cursor.fetchone()

    recordRow = ChallengeRecord(
        challenge_record_id=challenge_record_id,
        admin_check=0,
        member_id=member_id,
        candidate_id=candidate_id,
        precinct_id=precinct_id,
        result_status=result_status,
        result_description=result_description,
        upload_upload_id=upload_id,
    )

    recordRow.save()

    result = {
        "upload_id": upload_id,
        "member_id": member_id,
        "validation": validation,
        "precinct": precinct,
        "candidate": candidate,
        "error_msg": error_msg,
    }

    return Response(data=result, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def djangoServer(request):
    if request.method == "POST":
        upload_id = request.data["uploadId"]
        member_id = request.data["memberId"]
        selected_precinct_id = request.data["precinctId"]
        print(selected_precinct_id)
        msg = {"message": "정상적으로 접수됐습니다."}

        verify.after_response(upload_id, member_id, selected_precinct_id)

        return Response(data=msg, status=status.HTTP_200_OK)

    elif request.method == "GET":
        msg = {"message": "잘못된 요청입니다."}
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
