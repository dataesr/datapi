import boto3
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()

s3_access_key_id = os.getenv("OVH_ACCESS_KEY")
s3_bucket = os.getenv("OVH_BUCKET", "cartable")
s3_prefix = os.getenv("OVH_PREFIX")
s3_region_name = os.getenv("OVH_REGION", "gra")
s3_secret_access_key = os.getenv("OVH_SECRET_KEY")

client = None


def get_client():
  global client
  if client is None:
    client = boto3.client(
      "s3",
      endpoint_url=f"https://s3.{s3_region_name}.io.cloud.ovh.net",
      aws_access_key_id=s3_access_key_id,
      aws_secret_access_key=s3_secret_access_key,
      region_name=s3_region_name,
    )
  return client


def get_s3_data(file: str) -> pd.DataFrame:
  client = get_client()
  response = client.get_object(Bucket=s3_bucket, Key=f"{s3_prefix}/{file}")
  return pd.read_csv(response["Body"])