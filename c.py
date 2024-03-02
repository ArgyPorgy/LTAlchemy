

# !pip install langchain rank_bm25 pypdf unstructured chromadb

# !pip install unstructured['pdf'] unstructured

# !apt-get install poppler-utils

# !apt-get install -y tesseract-ocr
# !apt-get install -y libtesseract-dev
# !pip install pytesseract

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import Chroma

from langchain.llms import HuggingFaceHub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain.retrievers import BM25Retriever, EnsembleRetriever

import os
from getpass import getpass

HF_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN

path1 = "./scan.pdf"
data1 = UnstructuredPDFLoader(path1)
content = data1.load()

print(content[0].page_content)

path2 = "./sample_2.pdf"
data2 = UnstructuredPDFLoader(path2)
content2 = data2.load()

content2

docs = content + content2

docs

splitter = RecursiveCharacterTextSplitter(chunk_size=256,chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_TOKEN, model_name="BAAI/bge-base-en-v1.5"
)

vectorstore = Chroma.from_documents(chunks, embeddings)

retriever_vectordb = vectorstore.as_retriever(search_kwargs={"k": 2})

keyword_retriever = BM25Retriever.from_documents(chunks)
keyword_retriever.k =  2

ensemble_retriever = EnsembleRetriever(retrievers=[retriever_vectordb,keyword_retriever],
                                       weights=[0.5, 0.5])

llm = HuggingFaceHub(
    repo_id="huggingfaceh4/zephyr-7b-alpha",
    model_kwargs={"temperature": 0.5,"max_new_tokens":512}
)

template = """
<|system|>>
You are an AI Assistant that follows instructions extremely well.
Please be truthful and give direct answers. Please tell 'I don't know' if user query is not in CONTEXT

Keep in mind, you will lose the job, if you answer out of CONTEXT questions

CONTEXT: {context}
</s>
<|user|>
{query}
</s>
<|assistant|>
"""

prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()

chain = (
    {"context": ensemble_retriever, "query": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

print(chain.invoke("In what year was the letter sent to PN Condall in scan document?"))

print(chain.invoke("who is PJ Cross in scan document?"))

print(chain.invoke("who is Messi?"))