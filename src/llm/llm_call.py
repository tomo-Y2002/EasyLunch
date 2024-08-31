import yaml

from src.llm.aws import AWSBedrockClient

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)
