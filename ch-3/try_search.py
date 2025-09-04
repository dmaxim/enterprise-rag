from azure.search.documents.models import VectorizedQuery
from upload_sql_records import embed_text, search_client

query = "Dubious parenting advice"

embedding = embed_text(query)

vector_query = VectorizedQuery(
    vector=embedding,
    k_nearest_neighbors=3,
    fields="Vector"
)

results = search_client.search(
    search_text=query,
    vector_queries=[vector_query],
    top=1
)

for result in results:
    print(f"Found result: {result}")

query = "tennis racket"

embedding = embed_text(query)

vector_query = VectorizedQuery(
    vector=embedding,
    k_nearest_neighbors=3,
    fields="Vector"
)

results = search_client.search(
    search_text=query,
    vector_queries=[vector_query],
    filter="Manufacturer eq 'Banana Angel inc.'",
    select=["ProductName"],
    top=3
)

results_list = list(results)
for result in results_list:
    print(f"Found result: {result}")

def sort_results(
        results_list,
        field_name,
        descending=False):
    
    sorted_results = sorted(
        results_list,
        key=lambda x: x[field_name],
        reverse=descending)
    return sorted_results

print("***************")
print(sort_results(results_list, "ProductName", descending=False))