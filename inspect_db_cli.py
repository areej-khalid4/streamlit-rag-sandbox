import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "chroma_db", "chroma.sqlite3")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("==========================================")
    print("🔍 CHROMA DB SQLITE LIVE DATA INSPECTOR")
    print("==========================================")

    cursor.execute("SELECT name, dimension FROM collections;")
    collections = cursor.fetchall()
    for col in collections:
        print(f"📁 Collection Name: '{col[0]}' | Vector Dimensions: {col[1] or 384}")

    print("\n--- Stored Document Text Chunks in SQLite ---")
    cursor.execute("SELECT rowid, string_value FROM embedding_fulltext_search;")
    rows = cursor.fetchall()
    print(f"Total Stored Document Chunks: {len(rows)}\n")
    for r in rows:
        print(f"Row #{r[0]} | Content: {r[1][:100]}...")

    conn.close()
