import sqlite3
import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(api_key="pcsk_7LYtfz_8qjsKyFyF7DhxdhybHjypTkvu2HhvrBzaNGRX5vyNWhewDxy2YU5RRD1wzuMHBq")
index_name = "criminal-embeddings"

# Step 1: Delete old Pinecone index if it exists
existing_indexes = pc.list_indexes().names()
if index_name in existing_indexes:
    pc.delete_index(index_name)
    print(f"🗑️ Deleted existing index: {index_name}")

# Step 2: Create a new index with dimension 512
pc.create_index(
    name=index_name,
    dimension=512,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
print(f"✅ Created new index: {index_name}")

# Step 3: Connect to the index
index = pc.Index(index_name)

# Step 4: Set up SQLite database
db_file = "criminal_database.db"  # Database file name
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 5: Create a table to store embeddings
cursor.execute('''
CREATE TABLE IF NOT EXISTS embeddings (
    id TEXT PRIMARY KEY,
    vector BLOB
)
''')
conn.commit()
print("📂 SQLite database and table set up successfully.")

# Step 6: Sample embeddings (Replace this with actual embeddings)
vectors = [
    ("id1", [0.1] * 512),
    ("id2", [0.2] * 512),
    ("id3", [0.3] * 512),
    ("id4", [0.4] * 512),
    ("id5", [0.5] * 512),
]

# Step 7: Store embeddings in SQLite and Pinecone
for vid, vec in vectors:
    # Convert vector to a binary format for SQLite
    vector_blob = bytes(str(vec), encoding='utf-8')

    # Store in SQLite
    cursor.execute("INSERT OR REPLACE INTO embeddings (id, vector) VALUES (?, ?)", (vid, vector_blob))
    
    # Store in Pinecone
    index.upsert(vectors=[(vid, vec)])

conn.commit()
conn.close()

print("✅ Embeddings stored in SQLite and uploaded to Pinecone!")
