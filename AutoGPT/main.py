#加载环境变量文件
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from Tools import *
from Agent.AutoGPT import AutoGPT
from Tools.PythonTool import ExcelAnalyser

def lanch_agent(agent: AutoGPT) -> None:
    human_icon = "\U0001F468"
    ai_icon = "\U0001F916"
    while True:
        task = input(f"{ai_icon}：有什么可以帮您？\n{human_icon}：")
        if task.strip().lower() == "quit":
            break
        reply = agent.run(task, verbose=True)
        print(f"{ai_icon}：{reply}\n")

def main():
    #语言模型
    llm=ChatOpenAI(model_name="gpt-4-1106-preview",temperature=0.9,model_kwargs={"seed":42})
    
    #存储长时记忆的向量数据库
    db=Chroma.from_documents(
        documents=[Document(page_content="")],
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002"),
        collection_name="autogpt"
    )
    retriever = db.as_retriever(
        search_kwargs={"k": 1}
    )
 # 自定义工具集
    tools = [
        document_qa_tool,
        document_generation_tool,
        email_tool,
        excel_inspection_tool,
        directory_inspection_tool,
        finish_placeholder,
        ExcelAnalyser(
            prompt_file="./prompts/tools/excel_analyser.txt",
            verbose=True
        ).as_tool()
    ]

    # 定义智能体
    agent = AutoGPT(
        llm=llm,
        tools=tools,
        work_dir="./data",
        main_prompt_file="./prompts/main/main.txt",
        final_prompt_file="./prompts/main/final_step.txt",
        max_thought_steps=20,
        memery_retriever=retriever
    )
    
    lanch_agent(agent)


if __name__ == "__main__":
    main()
