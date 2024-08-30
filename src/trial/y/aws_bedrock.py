import boto3
import json

from botocore.exceptions import ClientError

session = boto3.Session(profile_name="test")
client = session.client(service_name="bedrock-runtime", region_name="us-east-1")
# Use this line if you are using the default profile
# client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"
body = json.dumps(
    {
        "anthropic_version": "bedrock-2023-05-31",  # The version of the Anthropic API to use.
        "max_tokens": 1024,  # The maximum number of tokens to generate.
        "temperature": 0.5,  # The randomness of the generated text.
        "messages": [
            {
                "role": "user",
                "content": "クリスマスについて小学生でもわかるように説明してください。",
            }
            # {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64_image_data}},
            # {"type": "text", "text": prompt_text}
        ],
    }
)
try:
    response = client.invoke_model(modelId=modelId, body=body)
except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{modelId}'. Reason: {e}")
    exit(1)
response_body = json.loads(response.get("body").read())
response_text = response_body["content"][0]["text"]
print(response_text)
