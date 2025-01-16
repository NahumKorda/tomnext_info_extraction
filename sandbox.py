import os
import time
import datetime

from chunking.pdf_reader import PDFReader
from prompting.configuration import OpenAIConfiguration
from prompting.prompter import OpenAIPrompter
from prompting.templates import OPENAI_MESSAGES, OPENAI_MASK


if __name__ == '__main__':

    start = time.time()

    input_dir = "data"

    config = OpenAIConfiguration()
    config.load("/Users/nahumkorda/code/resources/pwiz/openai_config.yml")

    prompter = OpenAIPrompter(config)

    reader = PDFReader()
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".pdf"):
            chunks = reader.read(file_path)
            print(f"Total chunks: {len(chunks)}")
            for i, chunk in enumerate(chunks):
                response = prompter.prompt(OPENAI_MESSAGES, OPENAI_MASK, chunk.text)
                if "not mentioned" not in response.lower():
                    print(f"\nChunk #{i + 1}\n{response}\n===========\n")
            print("\n\n")

    end = time.time()
    diff = end - start
    print("Processing completed in " + str(datetime.timedelta(seconds=diff)))
