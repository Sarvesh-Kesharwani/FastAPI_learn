from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os
import tempfile
import logging

from langchain.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO)

load_dotenv()
os.environ["OPENAI_API_KEY"]


def summarize_doc(file_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name

        loader = PyPDFLoader(tmp_path)
        docs = loader.load()

        prompt_len = PromptTemplate(
            input_variables=["text"],
            template="summarie the following text in 100 or less words:\n {text}",
        )
        llm = ChatOpenAI(temperature=0)
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt_len)

        result = chain.run(docs)
        return result

    except Exception as e:
        logging.error(f"Error summarizing document: {e}")
        raise e

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
