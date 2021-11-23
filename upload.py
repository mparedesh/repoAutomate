from boto3.s3.transfer import S3Transfer
import boto3
import argparse
from users import users
from teams import teams
from repos import repos

my_parser = argparse.ArgumentParser(description='Generate reports from gitgub')

my_parser.add_argument('-org', type=str)
my_parser.add_argument('-api_token', type=str)
my_parser.add_argument('-aws_access_key_id', type=str)
my_parser.add_argument('-aws_secret_access_key', type=str)
my_parser.add_argument('-bucket', type=str)
my_parser.add_argument('-key', type=str)
my_parser.add_argument('-report', type=str)

args = my_parser.parse_args()
ORG = args.org
API_TOKEN = args.api_token
aws_access_key_id = args.aws_access_key_id
aws_secret_access_key = args.aws_secret_access_key
bucket = args.bucket
key = args.key
report = args.report
file_name = ''

try:
    if report == 'users':
        file_name = users(ORG, API_TOKEN)
    elif report == 'teams':
        file_name = teams(ORG, API_TOKEN)
    else:
        file_name = repos(ORG, API_TOKEN)

    client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
    transfer = S3Transfer(client)
    transfer.upload_file(file_name, bucket, key + file_name)
except Exception as e:
    raise SystemExit(e)
