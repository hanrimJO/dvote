
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Candidate(models.Model):
    candidate_id = models.BigIntegerField(primary_key=True)
    candidate_name = models.CharField(max_length=255, blank=True, null=True)
    party_id = models.BigIntegerField(blank=True, null=True)
    precinct_id = models.BigIntegerField(blank=True, null=True)
    vote_result_vote_result_id = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.CharField(max_length=255, blank=True, null=True)
    criminal_info = models.CharField(max_length=255, blank=True, null=True)
    education_info = models.CharField(max_length=255, blank=True, null=True)
    election_number = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    job_info = models.CharField(max_length=255, blank=True, null=True)
    militery_status = models.CharField(max_length=255, blank=True, null=True)
    work_experience = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidate'


class ChallengeRankingBoard(models.Model):
    challenge_ranking_board_id = models.BigIntegerField(primary_key=True)
    count = models.IntegerField()
    precinct_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'challenge_ranking_board'


class ChallengeRecord(models.Model):
    challenge_record_id = models.BigIntegerField(primary_key=True)
    admin_check = models.CharField(max_length=255, blank=True, null=True)
    candidate_id = models.BigIntegerField(blank=True, null=True)
    member_id = models.BigIntegerField(blank=True, null=True)
    precinct_id = models.BigIntegerField(blank=True, null=True)
    result_description = models.CharField(max_length=255, blank=True, null=True)
    result_status = models.CharField(max_length=255, blank=True, null=True)
    upload_upload_id = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'challenge_record'


class District(models.Model):
    district_id = models.BigIntegerField(primary_key=True)
    district_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district'


class HibernateSequence(models.Model):
    next_val = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hibernate_sequence'


class Member(models.Model):
    member_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    validation = models.CharField(max_length=32, blank=True, null=True)
    challenge_ranking_board_challenge_ranking_board_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'


class Neighborhood(models.Model):
    neighborhood_id = models.BigIntegerField(primary_key=True)
    neighborhood_name = models.CharField(max_length=255, blank=True, null=True)
    precinct_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'neighborhood'


class Party(models.Model):
    party_id = models.BigIntegerField(primary_key=True)
    party_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'party'


class PastElectionResult(models.Model):
    past_election_result_id = models.BigIntegerField(primary_key=True)
    election_name = models.CharField(max_length=255, blank=True, null=True)
    vote_result_rate = models.CharField(max_length=255, blank=True, null=True)
    district_id = models.BigIntegerField(blank=True, null=True)
    party_id = models.BigIntegerField(blank=True, null=True)
    precinct_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'past_election_result'


class Pledge(models.Model):
    pledge_id = models.BigIntegerField(primary_key=True)
    pledge_content = models.TextField(blank=True, null=True)
    candidate_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pledge'


class Precinct(models.Model):
    precinct_id = models.BigIntegerField(primary_key=True)
    geo_arcs = models.TextField(blank=True, null=True)
    precinct_name = models.CharField(max_length=255, blank=True, null=True)
    district_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'precinct'


class Upload(models.Model):
    upload_id = models.BigIntegerField(primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    file_location = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    validation = models.BooleanField()  # This field type is a guess.
    member_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upload'


class VoteResult(models.Model):
    vote_result_id = models.BigIntegerField(primary_key=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vote_result'
