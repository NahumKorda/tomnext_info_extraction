from dataclasses import dataclass
import yaml

API_KEY = "api_key"
MODEL = "model"

@dataclass
class OpenAIConfiguration():
    api_key: str = ""
    model: str = ""

    def load(self, file_path: str):
        with open(file_path, "r") as input_file:
            config = yaml.safe_load(input_file)
        self.api_key = config[API_KEY]
        self.model = config[MODEL]
