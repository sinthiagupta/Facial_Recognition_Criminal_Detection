import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(api_key="pcsk_4jjSMN_4J5EM96zKSXu78aipZ4927xf8zDFHdWTBxkv7gFbyhSnTLpv8SdjBjo6DnsX5ao")  # Replace with your actual API key

# Define the index name
index_name = "embedding-db"  # Change this if needed

# Check if the index exists
if index_name not in pc.list_indexes().names():
    print(f"Creating index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=1024,  # Set the correct dimension for your embeddings
        metric='euclidean',  # Change to 'cosine' or 'dotproduct' if needed
        spec=ServerlessSpec(
            cloud='aws',  # Change if needed
            region='us-east-1'  # Change if needed
        )
    )
else:
    print(f"Index '{index_name}' already exists.")

# Connect to the index
index = pc.Index(index_name)
print(f"Connected to index: {index_name}")

# Example: Insert a sample vector (Replace this with your actual data)
sample_id = "123"
sample_vector = [0.1] * 1536  # Replace with your real embedding

index.upsert(vectors=[(sample_id, sample_vector)])
print(f"Inserted vector with ID: {sample_id}")

# Example: Query the index with a random vector
query_vector = [0.1] * 1536  # Replace with actual query vector
results = index.query(queries=[query_vector], top_k=5, include_metadata=True)

print("Query Results:", results)
