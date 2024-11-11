from typing import Sequence
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader

def loaded_data(file_path: str, web_paths: Sequence[str]) -> list:
    web_loader = WebBaseLoader(
        web_paths = web_paths,
        bs_kwargs={
            "parse_only": bs4.SoupStrainer(class_="wixui-rich-text__text"),
        },
        bs_get_text_kwargs={"separator": " ", "strip": True},
    )
    pdf_loader = PyPDFLoader(file_path)

    web_docs = web_loader.load()

    pdf_docs = []
    for doc in pdf_loader.load():
        pdf_docs.append(doc)

    return  web_docs + pdf_docs
