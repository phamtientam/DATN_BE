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
def analyze_contract_by_status(request):
    try:
        if request.method == 'GET':
            df = fetch_data(FILE_NAME_CONTRACT)
            status_counts = df['status'].value_counts().sort_index()

            contract_groups = status_counts.index.tolist()
            counts = status_counts.values.tolist()

            custom_data = {
                "label": "Biểu Đồ Số Lượng Hợp Đồng Theo Trạng Thái",
                "data": counts,
                "title": contract_groups
            }

            return JsonResponse(custom_data, safe=False)
    except:
        return HttpResponse(status=404)


@csrf_exempt
def analyze_contract_by_contract_name(request):
    try:
        if request.method == 'GET':
            df = fetch_data(FILE_NAME_CONTRACT)
            status_counts = df['name'].value_counts().sort_index()

            contract_groups = status_counts.index.tolist()
            counts = status_counts.values.tolist()

            custom_data = {
                "label": "Biểu Đồ Số Lượng Hợp Đồng Theo Loại Hợp Đồng",
                "data": counts,
                "title": contract_groups
            }

            return JsonResponse(custom_data, safe=False)
    except:
        return HttpResponse(status=404)
