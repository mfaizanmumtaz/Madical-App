from langchain_openai import ChatOpenAI
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain.output_parsers.boolean import BooleanOutputParser
from langchain.retrievers import ContextualCompressionRetriever
from langchain_pinecone import PineconeVectorStore
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")

def extract_medical_metadata(result):
    # medical_metadata = []
    # for doc in result:
        # medical_metadata.append(doc.metadata["reason"])
        # medical_metadata.append(doc.metadata["Diagnoses"])
    return result

def get_medical_chain(symptoms,claim_id):
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index("madicaldata")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    medical_chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    medical_relevance_prompt = """Given the following symptoms and retrieved symptoms, return YES if the retrieved symptoms or context is relevant to the symptoms and NO if it isn't.

> Symptoms: {question}
> Retrieved Symptoms or context:
>>>
{context}
>>>
> Relevant (YES / NO):"""

    medical_relevance_template = PromptTemplate(
    template=medical_relevance_prompt,
    input_variables=["question", "context"],
    output_parser=BooleanOutputParser(),
)

    medical_filter = LLMChainFilter.from_llm(medical_chat_model, prompt=medical_relevance_template)
    medical_compression_retriever = ContextualCompressionRetriever(
        base_compressor=medical_filter, base_retriever=vector_store.as_retriever(search_kwargs={"k":1,'filter': {'ClaimID':claim_id}})
        )

    medical_retriever_chain = vector_store.as_retriever(search_kwargs={"k":1,'filter': {'ClaimID':claim_id}}) | extract_medical_metadata
    return medical_retriever_chain.invoke(symptoms)
