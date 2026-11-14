
from pathlib import Path

from pypdf import PdfReader
from docx import Document

from langchain_core.documents import Document as LCDocument


def load_documents(folder_path):

    documents = []

    folder = Path(folder_path)

    for file_path in folder.rglob("*"):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        try:

            # PDF files
            if extension == ".pdf":

                reader = PdfReader(str(file_path))

                for page_number, page in enumerate(reader.pages):

                    text = page.extract_text() or ""

                    if text.strip():

                        documents.append(
                            LCDocument(
                                page_content=text,
                                metadata={
                                    "source": file_path.name,
                                    "page": page_number + 1,
                                    "type": "pdf"
                                }
                            )
                        )

            # Word files
            elif extension == ".docx":

                doc = Document(str(file_path))

                text = "\n".join(
                    paragraph.text
                    for paragraph in doc.paragraphs
                )

                if text.strip():

                    documents.append(
                        LCDocument(
                            page_content=text,
                            metadata={
                                "source": file_path.name,
                                "type": "docx"
                            }
                        )
                    )

            # Text files
            elif extension == ".txt":

                text = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if text.strip():

                    documents.append(
                        LCDocument(
                            page_content=text,
                            metadata={
                                "source": file_path.name,
                                "type": "txt"
                            }
                        )
                    )

        except Exception as error:

            print(
                f"Error processing {file_path.name}: {error}"
            )

    return documents
