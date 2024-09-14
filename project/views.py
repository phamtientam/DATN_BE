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
FILE_NAME_JOB = 'hr_job.csv'
FILE_NAME_LEVEL = 'level.csv'
FILE_NAME_PROJECT = 'project_project.csv'
s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name='ap-southeast-2',
                  config=Config(signature_version='s3v4'))


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
def get_list_status_project(request):
    try:
        if request.method == 'GET':
            results = []
            df_project = fetch_data(FILE_NAME_PROJECT)
            list_status_project = list(df_project[["display_name", 'date_start', 'date', 'last_update_status']].itertuples(index=False, name=None))
            return JsonResponse(list_status_project, safe=False)
    except:
        return HttpResponse(status=404)