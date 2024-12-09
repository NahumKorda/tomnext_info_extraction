import pymupdf4llm
from crewai.tools import BaseTool


class PDFReader(BaseTool):
    name: str = "PDF Reader"
    description: str = "Reads a PDF file and converts it into markdown format ready to be used with LLMs."

    def _run(self, file_path: str) -> str:
        return pymupdf4llm.to_markdown(file_path, margins=(0, 0))
