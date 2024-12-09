import os
import pathlib
import pickle
import time
import datetime
from dataclasses import dataclass
import pymupdf4llm
import tiktoken


@dataclass
class TOC:
    text: str
    titles: list[str]


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
        self.__max_tokens = 15000
        self.__min_tokens = 1000
        self.__min_num_lines = 20

    def read(self, file_path: str):

        md_text = pymupdf4llm.to_markdown(file_path, margins=(0, 0))

        chunks = self.__divide_into_chunks(md_text, 1)

        return chunks

    @staticmethod
    def __validate_title(text: str, level: int = 1) -> bool:
        if text.startswith("#"):
            return True
        if level == 1:
            return False
        if text.startswith("*") and text.endswith("*"):
            if level == 2:
                if text == text.upper():
                    return True
                else:
                    return False
            else:
                return True
        if level == 2:
            return False
        if text.startswith("_") and text.endswith("_"):
            return True
        return False

    def __divide_into_chunks(self, md_text: str, level: int = 1) -> list[Chunk]:

        retval = list()

        title = None
        text = ""
        num_lines = 0
        num_pages = 1
        contains_tables = False
        for line in md_text.split("\n"):
            if self.__validate_title(line, level) and self.__evaluate(title, text, num_lines):
                chunks = self.__generate_chunks(title, text, num_lines, num_pages, contains_tables, level)
                retval.extend(chunks)
                title = None
                text = ""
                num_lines = 0
                num_pages = 1
                contains_tables = False

            if self.__validate_title(line, level) and title is None:
                title = line.strip("#").strip()
                while "  " in title:
                    title = title.replace("  ", " ")

            if line.strip() == "-----":
                num_pages += 1

            if line.strip().startswith("|"):
                contains_tables = True

            text += f"{line}\n"
            num_lines += 1

        if title is not None and len(text) > 0:
            chunks = self.__generate_chunks(title, text, num_lines, num_pages, contains_tables, level)
            retval.extend(chunks)

        return retval

    def __evaluate(self, title: str | None, text: str, num_lines: int) -> bool:

        if title is None:
            return False

        if num_lines < self.__min_num_lines:
            return False

        num_tokens = len(self.__encoder.encode(text.replace("\n\n-----\n", "")))
        if num_tokens < self.__min_tokens:
            if "table of contents" in title.lower() or "executive summary" in title.lower():
                return True
            else:
                return False

        return True

    def __generate_chunks(self,
                          title: str,
                          text: str,
                          num_lines: int,
                          num_pages: int,
                          contains_tables: bool,
                          level: int) -> list[Chunk]:

        num_tokens = len(self.__encoder.encode(text.replace("\n\n-----\n", "")))
        if num_tokens > self.__max_tokens:
            level += 1
            if level > 3:
                return [self.__get_chunk(title, text, num_lines, num_pages, num_tokens, contains_tables)]
            else:
                return self.__divide_into_chunks(text, level)
        else:
            return [self.__get_chunk(title, text, num_lines, num_pages, num_tokens, contains_tables)]

    @staticmethod
    def __get_chunk(title: str,
                    text: str,
                    num_lines: int,
                    num_pages: int,
                    num_tokens: int,
                    contains_tables: bool) -> Chunk:

        chunk = Chunk(title=title,
                  text=text,
                  size=len(text),
                  num_lines=num_lines,
                  num_pages=num_pages,
                  num_tokens=num_tokens,
                  contains_tables=contains_tables)

        return chunk


if __name__ == '__main__':

    start = time.time()

    file_paths = [
        "../data/1706515389439-Warburg Pincus Capital Solutions Founders Fund Overview_9.30.2023_vF.pdf",
        "../data/1706515721063-Warburg Pincus Capital Solutions Founders Fund, L.P. - PPM (EEA Investors).pdf",
        "../data/Falcon Hybrid SPC - Confidential Private Placement Memorandum 1st May 2024.pdf",
        "../data/HL Global Private Assets Fund - PPM.pdf",
        "../data/Project-Tuscany-PPM.pdf",
        "../data/RE7 OFFERING MEMORANDUM (AS AT 27.3.2024) (1) (2).pdf",
        "../data/Warburg.pdf"
    ]

    input_dir = "../data"
    output_dir = "../data/chunks"

    reader = PDFReader()
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".pdf"):
            chunks = reader.read(file_path)
            file_name = file_name[:-4] + ".pkl"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "wb") as output_file:
                pickle.dump(chunks, output_file)
            max_size = 0
            for chunk in chunks:
                print("\n--------------------------------------------------------------------------\n")
                print(
                    f"{chunk.title}\n\tSize: {chunk.size}\n\tNumber of lines: {chunk.num_lines}\n\tNumber of pages: {chunk.num_pages}\n\tNumber of tokens: {chunk.num_tokens}\n\tContains tables: {chunk.contains_tables}")
                if chunk.num_tokens > max_size:
                    max_size = chunk.num_tokens
            print(f"\n\nTotal {len(chunks)} chunks.\nMax tokens: {max_size}\n\n")
            print()


    end = time.time()
    diff = end - start
    print("Processing completed in " + str(datetime.timedelta(seconds=diff)))
