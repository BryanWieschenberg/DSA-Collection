import os
import json
import boto3
from urllib.parse import urlparse
from botocore.client import Config
from dotenv import load_dotenv

from testgen import TestGen


def main():
    problem_id = 1

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))

    load_dotenv(dotenv_path=os.path.join(workspace_root, ".env"))

    generator = TestGen()
    test_cases = generator.get_cases()

    oracle = generator.Solution()
    tests_list = []

    for _, nums in enumerate(test_cases):
        expected_output = oracle.hasDuplicate(nums)
        tests_list.append(
            {
                "input": f"nums = {json.dumps(nums)}",
                "expected": json.dumps(expected_output),
            }
        )

    output_data = [{"id": problem_id, "tests": tests_list}]

    local_file = os.path.join(
        workspace_root, "src", "lib", f"hiddenTests-{problem_id}.json"
    )
    os.makedirs(os.path.dirname(local_file), exist_ok=True)
    with open(local_file, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"Successfully generated {len(tests_list)} cases and wrote to {local_file}")

    full_endpoint = os.getenv("R2_ENDPOINT_URL")
    aws_access_key_id = os.getenv("R2_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("R2_SECRET_KEY")

    if not all([full_endpoint, aws_access_key_id, aws_secret_access_key]):
        print("Error: Missing one or more R2 environment variables in .env.")
        return

    parsed = urlparse(full_endpoint)
    bucket_name = parsed.path.strip("/")
    endpoint_url = f"{parsed.scheme}://{parsed.netloc}"
    object_name = f"hiddenTests-{problem_id}.json"

    print(
        f"Uploading {object_name} to R2 bucket '{bucket_name}' via endpoint '{endpoint_url}'..."
    )
    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        s3_client.upload_file(local_file, bucket_name, object_name)
        print("Upload completed successfully!")
    except Exception as e:
        print(f"Error uploading to Cloudflare R2: {e}")


if __name__ == "__main__":
    main()
