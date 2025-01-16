import os
import yaml
from agents.crew import ExecutiveExtractionCrew


def run():

    with open("local_path.yaml", "r") as input_file:
        local_file_path = yaml.safe_load(input_file)

    with open(local_file_path["api_file_path"], "r") as input_file:
        keys = yaml.safe_load(input_file)

    os.environ["OPENAI_API_KEY"] = keys["openai_api_key"]
    os.environ["SERPER_API_KEY"] = keys["serper_api_key"]

    inputs = {
        'file_path': '../data/HL Global Private Assets Fund - PPM.pdf'
    }

    result = ExecutiveExtractionCrew().crew().kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()
