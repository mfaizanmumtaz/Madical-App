from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()
import os

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("madicaldata")

def get_medical_chain(symptoms,claim_id):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    medical_retriever_chain = vector_store.as_retriever(search_kwargs={"k":1,'filter': {'ClaimID':claim_id}})
    return medical_retriever_chain.invoke(symptoms)
