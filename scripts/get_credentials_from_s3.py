from scripts.utils import _configure_s3_client
import json

import constants


def main():
    s3_client = _configure_s3_client()

    download = s3_client.get_object(Key='credentials.json', Bucket=constants.S3_BUCKET_NAME)
    content = download["Body"].read()
    content_dict = json.loads(content)
    with open('credentials.json', 'w') as f:
        json.dump(content_dict, f)


if __name__ == '__main__':
    main()