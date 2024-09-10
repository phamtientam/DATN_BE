from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from io import StringIO
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
import os
import pandas as pd
import boto3
from botocore.config import Config
from datetime import datetime
load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_s3 = os.getenv('BUCKET')
FILE_NAME_EMPLOYEE = 'hr_employee.csv'
FILE_NAME_DEPARTMENT = 'hr_department.csv'
FILE_NAME_CONTRACT = 'contract_enterprise.csv'
FILE_NAME_JOB = 'job.csv'
FILE_NAME_LEVEL = 'level.csv'
FILE_NAME_PROJECT = 'project_project.csv'
s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name='ap-southeast-2',
                  config=Config(signature_version='s3v4'))


# get file from AWS
def get_object(bucket, key):
    """
    Get Data from S3
    """
    object_body = s3.get_object(Bucket=bucket, Key=key)
    data = StringIO(object_body["Body"].read().decode("utf-8"))
    df = pd.read_csv(data)
    return df


def fetch_data(module):
    try:
        data_s3 = get_object(bucket_s3, module)
        return data_s3
    except:
        return HttpResponse(status=404)


def handle_data_dashboard(
    df_employee,
    df_contract,
    df_job,
    df_level,
    df_project,
    df_department,
):
    dict_data = {}
    count_contract = df_contract.shape[0]
    count_job = df_job.shape[0]
    count_level = df_level.shape[0]
    count_project = df_project.shape[0]
    count_department = df_department.shape[0]
    count_employee = df_employee.shape[0]
    dict_data["employee"] = count_employee
    dict_data["contract"] = count_contract
    dict_data["job"] = count_job
    dict_data["level"] = count_level
    dict_data["project"] = count_project
    dict_data["department"] = count_department
    return dict_data


@csrf_exempt
def get_data_menu_dashboard(request):
    try:
        if request.method == 'GET':
            df_employee = fetch_data(FILE_NAME_EMPLOYEE)
            df_contract = fetch_data(FILE_NAME_CONTRACT)
            df_job = fetch_data(FILE_NAME_JOB)
            df_level = fetch_data(FILE_NAME_LEVEL)
            df_project = fetch_data(FILE_NAME_PROJECT)
            df_department = fetch_data(FILE_NAME_DEPARTMENT)
            data_handle = handle_data_dashboard(
                df_employee,
                df_contract,
                df_job,
                df_level,
                df_project,
                df_department,
            )

            return JsonResponse(data_handle, safe=False)
    except:
        return HttpResponse(status=404)


@csrf_exempt
def analyze_employee_active_by_month(request):
    try:
        if request.method == 'GET':
            df_contract = fetch_data(FILE_NAME_CONTRACT)
            df_contract['start_date'] = pd.to_datetime(df_contract['start_date'])
            df_contract['end_date'] = pd.to_datetime(df_contract['end_date'])
            dict_data = {}
            data_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            max_value = 0
            current_year = datetime.now().year
            # running
            data_running = []
            for month in data_month:
                filtered_rows = df_contract[
                    (
                        ((df_contract['end_date'].dt.month >= month) & (df_contract['start_date'].dt.month <= month)) |
                        ((df_contract['end_date'].dt.year > current_year) & (df_contract['start_date'].dt.month <= month))
                    ) & (df_contract['status'].isin(['running']))].shape[0]
                if filtered_rows > max_value:
                    max_value = filtered_rows
                data_running.append(filtered_rows)
            dict_data["running"] = data_running
            # new
            data_new = []

            for month in data_month:
                filtered_rows = df_contract[
                    (
                        ((df_contract['end_date'].dt.month >= month) & (
                                    df_contract['start_date'].dt.month <= month)) |
                        ((df_contract['end_date'].dt.year > current_year) & (
                                    df_contract['start_date'].dt.month <= month))
                    ) & (df_contract['status'].isin(['new']))].shape[0]
                if filtered_rows > max_value:
                    max_value = filtered_rows
                data_new.append(filtered_rows)
            dict_data["new"] = data_new
            # expert
            data_expired = []
            for month in data_month:
                filtered_rows = df_contract[
                    (
                            ((df_contract['end_date'].dt.month >= month) & (
                                        df_contract['start_date'].dt.month <= month)) |
                            ((df_contract['end_date'].dt.year > current_year) & (
                                        df_contract['start_date'].dt.month <= month))
                    ) & (df_contract['status'].isin(['expired']))].shape[0]
                if filtered_rows > max_value:
                    max_value = filtered_rows
                data_expired.append(filtered_rows)
            dict_data["expired"] = data_expired
            dict_data["max_height"] = max_value
            return JsonResponse(dict_data, safe=False)
    except:
        return HttpResponse(status=404)


@csrf_exempt
def analyze_status_project(request):
    try:
        if request.method == 'GET':
            df_project = fetch_data(FILE_NAME_PROJECT)
            df_status = df_project["last_update_status"].value_counts().sort_index()
            status_groups = df_status.index.tolist()
            counts = df_status.values.tolist()
            for i in range(len(status_groups)):
                status_groups[i] = f"{status_groups[i].replace('_', ' ')}({counts[i]})"
            custom_data = {
                "labels": status_groups,
                "data": counts
            }
            return JsonResponse(custom_data, safe=False)
    except:
        return HttpResponse(status=404)


@csrf_exempt
def analyze_number_of_project(request):
    try:
        if request.method == 'GET':
            df_project = fetch_data(FILE_NAME_PROJECT)
            current_year = datetime.now().year
            df_project['date_start'] = pd.to_datetime(df_project['date_start'])
            df_project['date'] = pd.to_datetime(df_project['date'])
            max_value = 0
            dict_data = {}
            data_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            data_project = []
            for month in data_month:
                filtered_rows = df_project[
                    (
                            ((df_project['date'].dt.month >= month) & (
                                    df_project['date_start'].dt.month <= month)) |
                            ((df_project['date'].dt.year > current_year) & (
                                    df_project['date_start'].dt.month <= month))
                    )].shape[0]
                if filtered_rows > max_value:
                    max_value = filtered_rows
                data_project.append(filtered_rows)
            dict_data["number_of_project"] = data_project
            dict_data["max_value"] = max_value
            return JsonResponse(dict_data, safe=False)
    except:
        return HttpResponse(status=404)

