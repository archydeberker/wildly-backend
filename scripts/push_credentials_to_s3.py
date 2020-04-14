from scripts.utils import _configure_s3_client
import json

import constants


def main():
    s3_client = _configure_s3_client()

    with open('../credentials.json') as f:
        data = json.load(f)
        s3_client.put_object(Body=json.dumps(data), Bucket=constants.S3_BUCKET_NAME, Key='credentials.json')


if __name__ == '__main__':
    main()