import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone client
pc = Pinecone(api_key="pcsk_7LYtfz_8qjsKyFyF7DhxdhybHjypTkvu2HhvrBzaNGRX5vyNWhewDxy2YU5RRD1wzuMHBq")

# Check if the index exists, if not, create one
index_name = "criminal-embeddings"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,  # Ensure this matches your embedding model's output
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the existing index
index = pc.Index(index_name)
print(f"Connected to Pinecone index: {index_name}")
