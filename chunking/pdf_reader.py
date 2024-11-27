import time
import datetime
from dataclasses import dataclass
import pymupdf4llm
import tiktoken


@dataclass
class Chunk:
    title: str
    text: str
    size: float
    num_lines: int
    num_pages: int
    num_tokens: int
    contains_tables: bool


class PDFReader:

    def __init__(self):
        self.__encoder = tiktoken.encoding_for_model("gpt-3.5-turbo-")

    def read(self, file_path: str):

        md_text = pymupdf4llm.to_markdown(file_path)

        chunks = self.__generate_chunks(md_text)

        for chunk in chunks:
            print("\n--------------------------------------------------------------------------\n")
            print(f"{chunk.title}\n\tSize: {chunk.size}\n\tNumber of lines: {chunk.num_lines}\n\tNumber of pages: {chunk.num_pages}\n\tNumber of tokens: {chunk.num_tokens}\n\tContains tables: {chunk.contains_tables}")

        print(f"\n\nTotal {len(chunks)} chunks.\n\n")

    def __generate_chunks(self, md_text: str) -> list[Chunk]:

        retval = list()

        title = None
        text = ""
        num_lines = 0
        num_pages = 0
        contains_tables = False
        for line in md_text.split("\n"):
            if line.strip().startswith("#") and len(text) > 0 and num_lines > 20:
                num_tokens = len(self.__encoder.encode(text))
                chunk = Chunk(title=title,
                              text=text,
                              size=len(text),
                              num_lines=num_lines,
                              num_pages=num_pages,
                              num_tokens=num_tokens,
                              contains_tables=contains_tables)
                retval.append(chunk)
                title = None
                text = ""
                num_lines = 0
                num_pages = 0
                contains_tables = False

            if line.strip().startswith("#") and title is None:
                title = line.strip("#")

            if line.strip() == "-----":
                num_pages += 1

            if line.strip().startswith("|"):
                contains_tables = True

            text += f"{line}\n"
            num_lines += 1

        return retval


if __name__ == '__main__':

    start = time.time()

    file_path = "../data/HL Global Private Assets Fund - PPM.pdf"

    reader = PDFReader()
    reader.read(file_path)

    end = time.time()
    diff = end - start
    print("Processing completed in " + str(datetime.timedelta(seconds=diff)))
