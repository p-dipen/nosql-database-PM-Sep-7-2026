# Day 4: Python & NoSQL Integration for Data Science (`pymongo` & `azure-cosmos`)

In modern Data Science, Machine Learning, and AI workflows, Python is the primary language. Data scientists frequently ingest data from NoSQL document stores directly into **Pandas DataFrames**, train models, and persist predictions or vector embeddings back into NoSQL databases.

---

## 1. Environment Setup

To connect to MongoDB and Azure Cosmos DB in Python, install the official client libraries:

```bash
pip install pymongo azure-cosmos pandas
```

---

## 2. Working with MongoDB via `pymongo`

### Connecting and Querying
```python
import os
import pandas as pd
from pymongo import MongoClient

# 1. Initialize Connection
client = MongoClient("mongodb://localhost:27017/")

# 2. Access Database and Collection
db = client["ECommerceDB"]
collection = db["Stores"]

# 3. Simple Query with Projection (exclude MongoDB _id)
query = {"category": "Audio", "price": {"$lte": 300}}
projection = {"_id": 0, "name": 1, "price": 1, "rating": 1, "inventory": 1}

results = list(collection.find(query, projection))

# 4. Convert directly to Pandas DataFrame
df = pd.DataFrame(results)
print("=== Filtered Audio Products ===")
print(df)
```

### Running MongoDB Aggregations in Python
```python
pipeline = [
    {"$match": {"type": "order"}},
    {"$unwind": "$items"},
    {
        "$group": {
            "_id": "$items.productName",
            "totalQuantitySold": {"$sum": "$items.quantity"},
            "totalRevenue": {"$sum": "$items.lineTotal"}
        }
    },
    {"$sort": {"totalRevenue": -1}}
]

agg_results = list(collection.aggregate(pipeline))
df_revenue = pd.DataFrame(agg_results).rename(columns={"_id": "Product"})
print("\n=== Top Selling Products by Revenue ===")
print(df_revenue)
```

---

## 3. Working with Azure Cosmos DB via `azure-cosmos` SDK

The Azure Cosmos DB Python SDK provides classes to manage accounts, databases, containers, and items.

### Core SDK Architecture:
```text
CosmosClient
    └── DatabaseProxy (get_database_client)
            └── ContainerProxy (get_container_client)
                    ├── read_item() [Point Read]
                    ├── create_item() / upsert_item()
                    └── query_items() [SQL Query Stream]
```

### Code Example: Initialize, Point Read, and Query
```python
import os
import pandas as pd
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError

# Connection parameters (prefer reading from environment variables)
ENDPOINT = os.getenv("COSMOS_ENDPOINT", "https://your-cosmos-account.documents.azure.com:443/")
KEY = os.getenv("COSMOS_KEY", "your-primary-key-here")
DATABASE_NAME = "RetailDB"
CONTAINER_NAME = "ECommerce"

# 1. Initialize Client
client = CosmosClient(ENDPOINT, credential=KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

# 2. Fast Point Read (1.0 RU, single-digit ms)
try:
    customer_item = container.read_item(
        item="CUST-001",
        partition_key="CUST-001"
    )
    print("Point Read Success:", customer_item["name"], "-", customer_item["email"])
except CosmosHttpResponseError as e:
    print(f"Read failed: {e.message}")

# 3. Parameterized SQL Query Execution
sql_query = """
SELECT 
    c.id, 
    c.name, 
    c.category, 
    c.price, 
    c.rating,
    c.inventory
FROM c 
WHERE c.type = @docType AND c.price >= @minPrice
"""
parameters = [
    {"name": "@docType", "value": "product"},
    {"name": "@minPrice", "value": 100.0}
]

# Run query (enable_cross_partition_query required if not filtering by single PK)
items = list(container.query_items(
    query=sql_query,
    parameters=parameters,
    enable_cross_partition_query=True
))

# 4. Convert directly into Pandas DataFrame
df_products = pd.DataFrame(items)
print("\n=== Cosmos DB Query Results in Pandas ===")
print(df_products[["name", "category", "price", "rating"]])
```

---

## 4. Ingesting Data from CSV or JSON into Cosmos DB

In data engineering pipelines, you often parse incoming CSVs or raw JSON files and bulk-insert them into Cosmos DB:

```python
import json
from azure.cosmos import CosmosClient

def bulk_import_json(file_path: str, container):
    with open(file_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    
    success_count = 0
    for record in records:
        try:
            # upsert_item creates if not exists, or updates if exists
            container.upsert_item(body=record)
            success_count += 1
        except Exception as e:
            print(f"Failed to insert item {record.get('id')}: {e}")
            
    print(f"Successfully loaded {success_count} documents into Cosmos DB container.")
```

---

## 5. Handling Throttling (HTTP 429: Request Rate Too Large)

In cloud NoSQL systems, if your application exceeds the provisioned Request Units (RU/s), Cosmos DB responds with **HTTP Status 429**.

The official `azure-cosmos` SDK has **built-in retry logic**, but you should always write resilient code:

```python
import time
from azure.cosmos.exceptions import CosmosHttpResponseError

def resilient_upsert(container, document, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            return container.upsert_item(document)
        except CosmosHttpResponseError as e:
            if e.status_code == 429:
                # Extract suggested retry-after duration from header, default to 1 sec
                retry_after_ms = float(e.headers.get("x-ms-retry-after-ms", 1000))
                sleep_sec = retry_after_ms / 1000.0
                print(f"[429 Throttle] RU limit reached. Sleeping for {sleep_sec:.2f} seconds...")
                time.sleep(sleep_sec)
                retries += 1
            else:
                raise e
    raise TimeoutError("Exceeded maximum retries due to RU rate limits.")
```

---

## 6. Summary for Data Science Pipelines

| Task | MongoDB (`pymongo`) | Azure Cosmos DB (`azure-cosmos`) |
| :--- | :--- | :--- |
| **Connection Object** | `MongoClient(conn_str)` | `CosmosClient(endpoint, key)` |
| **Target Collection** | `db["collection_name"]` | `db.get_container_client("name")` |
| **Point Lookup** | `col.find_one({"_id": id})` | `container.read_item(item=id, partition_key=pk)` |
| **Query Mechanism** | MQL filter dictionary or Aggregation | SQL string query (`SELECT ... FROM c`) |
| **Pandas Ingestion** | `pd.DataFrame(list(col.find()))` | `pd.DataFrame(list(container.query_items()))` |
