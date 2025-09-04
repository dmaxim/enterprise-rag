import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
import sqlite3
from datetime import date
from dotenv import load_dotenv
load_dotenv()

today = date.today()
date_string = today.strftime("%Y-%m-%d")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

search_client = SearchClient(
    endpoint=os.getenv("AI_SEARCH_ENDPOINT"), # type: ignore
    index_name=os.getenv("AI_SEARCH_INDEX_NAME"), # type: ignore
    credential=AzureKeyCredential(os.getenv("AI_SEARCH_KEY")), #type: ignore
    )

def summary_SQL_record(sql_record):
    record_summary_string = f"""
    Product_Name: {sql_record[1]}
    Product Description: {sql_record[2]}
    Technical Specs: {sql_record[3]}
    Manufacturer: {sql_record[4]}
    """
    print(f"Summarized record for {sql_record[1]}: {record_summary_string}")
    return record_summary_string


def clean_record_summary(record_summary):
    cleaned_record_summary = record_summary.replace("--", "")
    return cleaned_record_summary


def embed_text(cleaned_record_summary):
    response = openai_client.embeddings.create(
        input=cleaned_record_summary,
        model="text-embedding-3-small",
        dimensions=1536
    )
    return response.data[0].embedding # type: ignore


def upload_to_AI_search(record, record_summary, embedded_summary):
      record_to_upload = {}    
      record_to_upload["id"] = str(record[0])
      record_to_upload["Summary"] = record_summary
      record_to_upload["Vector"] = embedded_summary
      record_to_upload["ProductName"] = record[1]
      record_to_upload["ProductDescription"] = record[2]
      record_to_upload["TechnicalSpecification"] = record[3]
      record_to_upload["Manufacturer"] = record[4]
      record_to_upload["DateModified"] = date_string

      search_client.merge_or_upload_documents(
          documents=[record_to_upload]
      )

      print(f"Record for {record[1]} processed and uploaded!")

def summarize_embed_upload(sql_record):
     summarized_SQL_record = summary_SQL_record(sql_record)
     cleaned_summary = clean_record_summary(summarized_SQL_record)
     embedded_summary = embed_text(cleaned_summary)
     upload_to_AI_search(sql_record, cleaned_summary, embedded_summary)

def ingest_all_records(sql_query):
  conn = sqlite3.connect("products.db")
  cur = conn.cursor()
  cur.execute(sql_query)
 
  batch_size = 100
 
  total_records_transformed = 0
  
  while True:
    records = cur.fetchmany(size=batch_size)
    if not records:
      break
 
    for record in records:
        if record[-1] > 0:
          try:
            search_client.delete_documents(
              documents=[{"id": str(record[0])}])
            continue
          except:
            summarize_embed_upload(record)
            continue
 
        else:
          print(f"Summarizing record with ID {record[0]}")
          summarize_embed_upload(record)
    
    total_records_transformed += len(records)
    print(f"Total records uploaded: {total_records_transformed}")
 
  cur.close()
  conn.close()
 
if __name__ == "__main__":
  ingest_all_records("SELECT * FROM Products")