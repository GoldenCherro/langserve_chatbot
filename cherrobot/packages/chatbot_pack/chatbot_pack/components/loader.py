from typing import Sequence
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader

def loaded_data(file_path: str, web_paths: Sequence[str]) -> list:
    """
    Loads data from a PDF file and specified web URLs, returning a list of document objects.

    Args:
        file_path (str): The path to the PDF file to be loaded.
        web_paths (Sequence[str]): A sequence of URLs from which web page content will be loaded.

    Returns:
        list: A combined list of document objects from both the PDF and web sources.
    """
    
    # Initialize the web loader with BeautifulSoup configuration for specific HTML parsing
    web_loader = WebBaseLoader(
        web_paths=web_paths,
        bs_kwargs={
            "parse_only": bs4.SoupStrainer(class_="wixui-rich-text__text"),
        },
        bs_get_text_kwargs={"separator": " ", "strip": True},
    )
    
    # Initialize the PDF loader
    pdf_loader = PyPDFLoader(file_path)

    # Load documents from the specified web paths
    web_docs = web_loader.load()

    # Load documents from the PDF file and append them to a list
    pdf_docs = []
    for doc in pdf_loader.load():
        pdf_docs.append(doc)

    # Combine web and PDF documents into a single list
    return web_docs + pdf_docs

