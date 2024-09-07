from openai import AzureOpenAI
import yaml


with open("../../../config.yaml", "r") as f:
    config = yaml.safe_load(f)
client = AzureOpenAI(
    azure_endpoint=config["AZURE_ENDPOINT"],
    api_key=config["AZURE_API_KEY"],
    api_version=config["AZURE_API_VERSION"],
)

response = client.chat.completions.create(
    model="aoai-gpt-4o",  # model = "deployment_name".
    # messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
    #     {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
    #     {"role": "user", "content": "Do other Azure AI services support this too?"}
    # ]
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information.",
        },
        {"role": "user", "content": "日本語で質問してよいですか？"},
    ],
)

print(response.choices[0].message.content)
