"""
Day 4: Python NoSQL & Vector Similarity Demonstration Script
CBC DSAI - NoSQL Database Course

This script demonstrates:
1. Loading and filtering NoSQL documents from sample_data.json.
2. Converting NoSQL JSON datasets directly into Pandas DataFrames.
3. Performing data analytics (revenue aggregation by product, sales summary).
4. Mathematical demonstration of Vector Cosine Similarity Search (how AI search works in NoSQL).
"""

import json
import math
import os
from pathlib import Path

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def load_sample_data():
    """Loads the Day 4 sample e-commerce dataset."""
    current_dir = Path(__file__).resolve().parent
    data_file = current_dir / "sample_data.json"
    
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_cosine_similarity(vec_a, vec_b):
    """
    Calculates the cosine similarity between two numeric vectors.
    Formula: (A · B) / (||A|| * ||B||)
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same number of dimensions")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def run_pandas_analytics(data):
    """Demonstrates converting nested NoSQL data into Pandas DataFrames."""
    print("\n" + "=" * 60)
    print("STEP 1: NoSQL Document to Pandas DataFrame Analysis")
    print("=" * 60)

    # Filter products
    products = [doc for doc in data if doc.get("type") == "product"]
    
    # Filter orders and flatten line items
    flattened_items = []
    for doc in data:
        if doc.get("type") == "order":
            order_id = doc["orderId"]
            customer_id = doc["customerId"]
            order_date = doc["orderDate"]
            for item in doc.get("items", []):
                flattened_items.append({
                    "orderId": order_id,
                    "customerId": customer_id,
                    "orderDate": order_date,
                    "productId": item["productId"],
                    "productName": item["productName"],
                    "quantity": item["quantity"],
                    "unitPrice": item["unitPrice"],
                    "lineTotal": item["lineTotal"]
                })

    if PANDAS_AVAILABLE:
        df_products = pd.DataFrame(products)
        print("\n--- Product Catalog DataFrame ---")
        print(df_products[["productId", "name", "category", "price", "rating", "inventory"]].to_string(index=False))

        df_sales = pd.DataFrame(flattened_items)
        print("\n--- Flattened Order Line Items ---")
        print(df_sales[["orderId", "productName", "quantity", "lineTotal"]].to_string(index=False))

        # Aggregation: Total Revenue per Product
        revenue_summary = (
            df_sales.groupby("productName")
            .agg(total_units_sold=("quantity", "sum"), total_revenue=("lineTotal", "sum"))
            .reset_index()
            .sort_values(by="total_revenue", ascending=False)
        )
        print("\n--- Total Revenue by Product (Aggregation) ---")
        print(revenue_summary.to_string(index=False))
    else:
        print("Pandas not installed in this environment. Showing raw extracted items:")
        for item in flattened_items[:3]:
            print(item)


def run_vector_search_demo(data):
    """
    Demonstrates semantic similarity search using Vector Distance on product embeddings.
    """
    print("\n" + "=" * 60)
    print("STEP 2: Vector Search / Semantic Similarity Demo (DSAI)")
    print("=" * 60)

    # Let's define a mock search query:
    # A user searches for: "Silent music earphones with long battery life"
    # A text embedding model converts this query into a 3D vector:
    user_query_vector = [0.80, -0.10, 0.40]
    print(f"User Query: 'Silent music earphones with long battery life'")
    print(f"User Query Embedding: {user_query_vector}")

    products = [doc for doc in data if doc.get("type") == "product" and "embedding" in doc]

    ranked_products = []
    for prod in products:
        similarity = calculate_cosine_similarity(user_query_vector, prod["embedding"])
        ranked_products.append({
            "name": prod["name"],
            "category": prod["category"],
            "price": prod["price"],
            "similarity": similarity
        })

    # Sort descending by similarity score
    ranked_products.sort(key=lambda x: x["similarity"], reverse=True)

    print("\n--- Top Ranked Products by Semantic Similarity (Cosine Score) ---")
    for rank, p in enumerate(ranked_products, start=1):
        print(f"#{rank} [Score: {p['similarity']:.4f}] - {p['name']} (${p['price']}) [{p['category']}]")

    print("\nInsight: The 'NeuralNoise Cancelling Headphones' has the highest cosine similarity")
    print("because its semantic vector is closely aligned with the user's intent, even without exact keyword match!")


if __name__ == "__main__":
    print("Initializing Day 4 Python Demonstration...")
    data = load_sample_data()
    print(f"Loaded {len(data)} documents from sample_data.json successfully.")

    run_pandas_analytics(data)
    run_vector_search_demo(data)
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
