from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名
    """
    return filename.split(".")[-1]

def load_docs(filename: str) -> List[Document]:
    """
    加载文件
    :param filename: 文件名
    :return:
    """
    file_extension = get_file_extension(filename)
    if file_extension == "pdf":
        return PyPDFLoader(filename)
    elif file_extension == "docx" or file_extension == "doc":
        return UnstructuredWordDocumentLoader(filename)
    else:
        return NotImplementedError(f"Unsupported file extension: {file_extension}")
def ask_docment(
        filename: str,
        query: str,
) -> str:
    "根据pdf文档的内容回答问题"
    "使用langchain中pdf加载器读取pdf文档的内容并回答问题"
    
    loader=load_docs(filename)
    pages=loader.load_and_split()
    if len(pages)==0:
        return "No content found in the file."
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len,
    )
    docs = text_splitter.split_documents(pages)
    if len(docs)==0 or docs is None:
        return "No content found in the file."
    db=Chroma.from_ducuments(
        documents=docs,
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002"),
    )
    qa_chain=RetrievalQA.from_chain_type(
        llm=OpenAI(model="gpt-3.5-turbo",temperature=0,seed=42),
        chain_type="stuff",
        retriever=db.as_retriever(),
    )
    response=qa_chain.run(query+"{请问中文回答}")
    return response

if __name__ == "__main__":
    filename = "../data/2023年10月份销售计划.docx"
    query = "销售额达标的标准是多少？"
    response=ask_document(filename,query)
    print(response)