import chromadb

client = chromadb.PersistentClient(path="./chromadb.db")

collection = client.get_or_create_collection(
    name="abstracts", metadata={"hnsw:space": "cosine"}
)

print(collection.count())


def query(query_test, n_results=5, metadata={}):
    return collection.query(
        query_texts=[query_test],
        n_results=n_results,
        where=metadata,
    )


print(query("testing"))
