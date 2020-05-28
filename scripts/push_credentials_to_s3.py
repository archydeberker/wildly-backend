from scripts.utils import _configure_s3_client
import json

import constants


def main():
    s3_client = _configure_s3_client()

    with open('../client_secret_330297269332-e69mircs682qbtsb0djdripakudkk2f1.apps.googleusercontent.com.json') as f:
        data = json.load(f)
        s3_client.put_object(Body=json.dumps(data), Bucket=constants.S3_BUCKET_NAME, Key='credentials.json')

    with open('../token_archy@weatherwindowapp.pickle', 'rb') as f:
        s3_client.put_object(Body=f.read(), Bucket=constants.S3_BUCKET_NAME, Key='token.pickle')


if __name__ == '__main__':
    main()