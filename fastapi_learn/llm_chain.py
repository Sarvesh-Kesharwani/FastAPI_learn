from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def summarize_doc(file_bytes):
    text = file_bytes.decode(
        "utf-8", errors="ignore"
    )  # or use PyMuPDF/DocxLoader if not txt
    docs = [Document(page_content=text)]

    llm = ChatOpenAI(temperature=0)  # or another LLM
    chain = load_summarize_chain(llm, chain_type="stuff")

    result = chain.run(docs)
    return result
