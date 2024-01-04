import json
import chromadb

client = chromadb.PersistentClient(path="./chromadb.db")

collection = client.get_or_create_collection(
    name="abstracts", metadata={"hnsw:space": "cosine"}
)

if __name__ == "__main__":
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
                "won_anything": False if len(d["awards_won"]) == 0 else True,
            }
            for d in data
        ]
        ids = [d["project_id"] for d in data]
        collection.add(
            documents=abstracts,
            metadatas=absttract_metadata,
            ids=ids,
        )
