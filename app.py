from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from langchain.vectorstores import Chroma
from langchain.callbacks.base import BaseCallbackHandler
import chainlit as cl
from datetime import datetime
from tinydb import TinyDB, Query
import os


embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
db = Chroma(persist_directory="./mentalhealthembedings", embedding_function=embedding_function)

huggingFaceAPiKey = os.getenv('HUGGING_API_KEY')

repoID="mistralai/Mistral-7B-Instruct-v0.1"

template = """You are an AI mental health therapist Julie. You are an expert in psychology and you help people suffering from mental health problems by offering them solutions and making them feel better. Always be polite, kind and respectful. You have a collection of case studies of previous patients and appropriate responses. Whenever possible use the case studies to formulate a similiar response. Generate long and helpful responses. 


Case Studies:
----------------
{context}
----------------

Chat History:
----------------
{chat_history}
----------------


Current User: {human_input}
Helpful Response: """


MessagesDB = TinyDB('chat_messages.json')

messages_table = MessagesDB.table('messages')

def insert_message(user_id, content, is_user_message):    
    
    messages = messages_table.search((Query().user_id == user_id) & (Query().is_user_message == is_user_message))

    if len(messages) >= 3:
        oldest_message = min(messages, key=lambda x: x['timestamp'])
        messages_table.remove(Query().timestamp == oldest_message['timestamp'])

    messages_table.insert({
        'user_id': user_id,
        'content': content,
        'is_user_message': is_user_message,
        'timestamp': datetime.now().timestamp()
    })

def get_latest_messages(user_id):
    human_messages = messages_table.search((Query().user_id == user_id) & (Query().is_user_message == True))
    ai_messages = messages_table.search((Query().user_id == user_id) & (Query().is_user_message == False))

    if len(human_messages) != len(ai_messages):
        messages_table.remove(Query().user_id == user_id)  
        print('User and AI messages are not in sync')
        return ""

    chat_history = ""
    messages = messages_table.search(Query().user_id == user_id)
    for message in messages:
        if message['is_user_message']:
            chat_history += f"Human: {message['content']}\n"
        else:
            chat_history += f"AI: {message['content']}\n"
    return chat_history



@cl.on_chat_start
def main():
    prompt = PromptTemplate(
    input_variables=["human_input", "context", "chat_history"], template=template)
    llmmodel = HuggingFaceHub(repo_id=repoID, model_kwargs={"max_new_tokens": 500, "temperature": 0.7},huggingfacehub_api_token=huggingFaceAPiKey)
    chain = load_qa_chain(llm=llmmodel, prompt=prompt, verbose=True)
    retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.2, 'k':3})
    cl.user_session.set("llm_retriever", retriever)
    cl.user_session.set("llm_chain", chain)    


user_id = 1
@cl.on_message
async def main(query: str):
    chain = cl.user_session.get("llm_chain")  
    retriever = cl.user_session.get("llm_retriever")
    
    docs = retriever.get_relevant_documents(query)
    chatHistory = get_latest_messages(user_id)

    res = await chain.acall({"human_input":query, "input_documents":docs, "chat_history": chatHistory})
    print(res)
    res = res['output_text']
    res = res.strip()

    insert_message(user_id, query, True)
    insert_message(user_id, res, False)

    await cl.Message(content=res).send()