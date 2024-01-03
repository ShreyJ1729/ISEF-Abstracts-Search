import json
import chromadb

client = chromadb.PersistentClient(path="./chromadb.db")

collection = client.get_or_create_collection(
    name="abstracts", metadata={"hnsw:space": "cosine"}
)

if collection.count() == 0:
    with open("abstracts.json", "r") as f:
        data = json.load(f)
        abstracts = [d["title"] + "\n\n" + d["abstract"] for d in data]
        absttract_metadata = [
            {
                "title": d["title"],
                "booth_id": d["booth_id"],
                "year": d["year"],
                "finalist_names": json.dumps(d["finalist_names"]),
                "awards_won": json.dumps(d["awards_won"]),
            }
            for d in data
        ]
        ids = [d["project_id"] for d in data]
        collection.add(
            documents=abstracts,
            metadatas=absttract_metadata,
            ids=ids,
        )

results = collection.query(
    query_texts=[
        "drug discovery to optimize the bottleneck when a drug enters the bloodstream among different races of people"
    ],
    n_results=5,
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains": "search_string"},
)

print(results)
