from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from upload_sql_records import embed_text
import os
from azure.core.credentials import AzureKeyCredential

#query = "Human Endogenous Retroviruses ALS"
#query = "Chemokine ligand 18"
#query = "reduction in alkaline phosphatase"
query = "accelerated approval of Iqirvo"

embedding = embed_text(query)

vector_query = VectorizedQuery(
    vector=embedding,
    k_nearest_neighbors=3,
    fields="Vector"
)

pub_med_search_client = SearchClient(
    endpoint=os.getenv("AI_SEARCH_ENDPOINT"), # type: ignore
    index_name=os.getenv("AI_PUB_MED_INDEX_NAME"), # type: ignore
    credential=AzureKeyCredential(os.getenv("AI_SEARCH_KEY")), #type: ignore
    )

results = pub_med_search_client.search(
    search_text=query,
    vector_queries=[vector_query],
    top=3
)

for result in results:
    print("**************************")
    print(f"Found result: {result['Title']}\n")
    print(result['Summary'])
