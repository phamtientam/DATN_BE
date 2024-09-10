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


@csrf_exempt
def analyze_count_level_by_employee(request):
    try:
        if request.method == 'GET':
            df_level = fetch_data(FILE_NAME_LEVEL)
            df_employee = fetch_data(FILE_NAME_EMPLOYEE)
            list_level_name = df_level["name"].to_list()
            results = []
            info_level_by_employee = df_employee["level_name"].value_counts().sort_index()
            level_name_epl = info_level_by_employee.index.tolist()
            counts_level_name_epl = info_level_by_employee.values.tolist()
            map_data = []
            for name, count in zip(level_name_epl, counts_level_name_epl):
                map_data.append((name, count))
            for level_name in list_level_name:
                count = 0
                for data in map_data:
                    if data[0] == level_name:
                        count += 1
                        results.append(data[1])
                        break
                if count == 0:
                    results.append(0)
            custom_data = {
                "labels": list_level_name,
                "data": results
            }
            return JsonResponse(custom_data, safe=False)
    except:
        return HttpResponse(status=404)


@csrf_exempt
def get_employee_by_level(request):
    try:
        if request.method == 'GET':
            level_name = request.GET.get('level_name', None)
            df_employee = fetch_data(FILE_NAME_EMPLOYEE)
            search_employee = df_employee[
                df_employee["level_name"] == level_name
            ]
            list_data = [list(x) for x in search_employee[["name", "department_name", "level_name"]].values]
            return JsonResponse(list_data, safe=False)
    except:
        return HttpResponse(status=404)
