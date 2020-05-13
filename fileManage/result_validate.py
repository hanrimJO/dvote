from .models import Upload, ChallengeRecord, Candidate, Precinct


def result_validate(precinct, candidate, selected_precinct_id):
    state = Precinct.objects.filter(precinct_name=precinct).exists()

    if state:
        precinct_id = Precinct.objects.get(precinct_name=precinct).precinct_id

        if precinct_id != selected_precinct_id:
            error_msg = "선택한지역구와분석한지역구가일치하지않습니다."
            return (False, error_msg)

        candidate_list = Candidate.objects.filter(precinct_id=precinct_id).values_list(
            "candidate_name", flat=True
        )

        candidate_list = [name.split('\n')[0] for name in candidate_list]

        if candidate in candidate_list:
            return (True, "")
        else:
            error_msg = "지역구와후보자명이잘못매칭됐습니다."
            return (False, error_msg)
    else:
        error_msg = "분석한지역구가올바르지않습니다."
        return (False, error_msg)
