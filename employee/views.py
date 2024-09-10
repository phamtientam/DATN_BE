from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import TaskSerializer
from .models import Task
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
def analyze_data_avg_age(request):
    try:
        if request.method == 'GET':
            df = fetch_data(FILE_NAME_EMPLOYEE)
            df['birthday'] = pd.to_datetime(df['birthday'])
            current_date = datetime.now()
            df['age'] = df['birthday'].apply(
                lambda x: current_date.year - x.year - ((current_date.month, current_date.day) < (x.month, x.day)))
            # Define age ranges
            bins = [20, 30, 40, 50, 60]
            labels = ['20-30', '30-40', '40-50', '50-60']

            # Categorize ages into bins
            df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

            # Count the number of people in each age group
            age_group_counts = df['age_group'].value_counts().sort_index()
            age_groups = age_group_counts.index.tolist()
            counts = age_group_counts.values.tolist()

            custom_data = {
                "label": "Biểu Đồ Số Lượng Nhân Viên Theo Độ Tuổi",
                "data": counts,
                "title": age_groups
            }

            return JsonResponse(custom_data, safe=False)
    except:
        return HttpResponse(status=404)


@csrf_exempt
def analyze_data_employee_by_department(request):
    try:
        if request.method == 'GET':

            df_employees = fetch_data(FILE_NAME_EMPLOYEE)
            df_departments = fetch_data(FILE_NAME_DEPARTMENT)

            df_employees['department_name'] = df_employees['department_name']
            department_counts = df_employees['department_name'].value_counts().reset_index()
            department_counts.columns = ['department_name', 'employee_count']

            all_departments = df_departments[['display_name']].rename(columns={'display_name': 'department_name'})

            result = all_departments.merge(department_counts, on='department_name', how='left').fillna(0)
            result['employee_count'] = result['employee_count'].astype(int)

            title = result['department_name'].tolist()
            data = result['employee_count'].tolist()

            custom_data = {
                "label": "Biểu Đồ Số Lượng Nhân Viên Theo Phòng Ban",
                "data": data,
                "title": title
            }

            return JsonResponse(custom_data, safe=False)

    except:
        return HttpResponse(status=404)


@csrf_exempt
def analyze_employee_breakdown_by_family_and_single(request):
    try:
        if request.method == 'GET':
            df_employees = fetch_data(FILE_NAME_EMPLOYEE)
            data_count = df_employees['marital'].value_counts().reset_index()

            title = data_count["index"].tolist()
            data = data_count["marital"].tolist()
            title = [item.capitalize() for item in title]

            custom_data = {
                "label": "Biểu Đồ Số Lượng Nhân Viên Đã Có Gia Đình Và Chưa Có Gia Đình",
                "data": data,
                "title": title
            }

            return JsonResponse(custom_data, safe=False)

    except:
        return HttpResponse(status=404)
