"""
Day 4: Python SDK Starter Lab for Beginners
CBC DSAI - NoSQL Database Course

Welcome to your first Python SDK lab!
This script is designed for complete beginners. You can run it immediately with:
    python3 starter_python_sdk.py

Follow the numbered sections below to understand how Python interacts with NoSQL data.
"""

import json
from pathlib import Path


# ==============================================================================
# LESSON 1: Understanding Python Dictionaries (JSON in Python)
# ==============================================================================
def lesson_1_python_basics():
    print("=" * 60)
    print("LESSON 1: Python Dictionaries are just JSON Documents!")
    print("=" * 60)

    # In Python, curly braces {} create a dictionary (same as a JSON object)
    student = {
        "id": "STU-001",
        "name": "Sarah Connor",
        "program": "DSAI",
        "isEnrolled": True,
        "courses": ["NoSQL", "Python", "AI Foundations"]  # A list is just a JSON array []
    }

    print("Student Document:")
    print(student)

    # How to read a specific field:
    print(f"\nStudent Name: {student['name']}")
    print(f"First Course: {student['courses'][0]}")

    # How to add a new field to a document:
    student["semester"] = "Fall 2024"
    print(f"Added semester field: {student['semester']}")


# ==============================================================================
# LESSON 2: Reading NoSQL JSON Files in Python
# ==============================================================================
def lesson_2_read_json_file():
    print("\n" + "=" * 60)
    print("LESSON 2: Reading sample_data.json with Python")
    print("=" * 60)

    file_path = Path(__file__).resolve().parent / "sample_data.json"

    # Open and load the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"Loaded {len(data)} total records from sample_data.json.")

    # Let's count how many documents are of each type:
    type_counts = {}
    for doc in data:
        doc_type = doc.get("type", "unknown")
        type_counts[doc_type] = type_counts.get(doc_type, 0) + 1

    print("\nDocument Breakdown:")
    for doc_type, count in type_counts.items():
        print(f"  • {doc_type.capitalize()} documents: {count}")


# ==============================================================================
# LESSON 3: The 3-Step SDK Flow (Simulated / In-Memory)
# ==============================================================================
def lesson_3_simulated_sdk():
    """
    Shows students how an SDK works conceptually before connecting to the cloud.
    """
    print("\n" + "=" * 60)
    print("LESSON 3: How an SDK Works (Step-by-Step Simulation)")
    print("=" * 60)

    print("Step 1: Connecting to Database Server... [CONNECTED]")
    print("Step 2: Selecting Database 'CollegeDB' and Container 'Students'... [SELECTED]")

    # Simulated database container (a simple in-memory list)
    database_container = {}

    # Step 3: Insert (Upsert) an item
    new_doc = {
        "id": "CUST-999",
        "name": "Bruce Wayne",
        "membershipLevel": "Platinum"
    }

    # Simulate container.upsert_item()
    database_container[new_doc["id"]] = new_doc
    print(f"\nStep 3a: Inserted new item '{new_doc['id']}' into the container.")

    # Step 4: Point Read by ID (Simulate container.read_item())
    retrieved = database_container.get("CUST-999")
    print(f"Step 3b: Point Read returned: {retrieved['name']} ({retrieved['membershipLevel']})")


# ==============================================================================
# LESSON 4: Real Azure Cosmos DB SDK Code (When You Have Credentials)
# ==============================================================================
def lesson_4_real_cosmos_db_sdk_template():
    print("\n" + "=" * 60)
    print("LESSON 4: Real Azure Cosmos DB Code Template")
    print("=" * 60)
    print("When you are ready to connect to your live Azure Cosmos DB account,")
    print("install the library with: pip install azure-cosmos")
    print("\nHere is the exact code to use:\n")

    code_sample = '''
from azure.cosmos import CosmosClient

ENDPOINT = "https://<your-account-name>.documents.azure.com:443/"
PRIMARY_KEY = "<your-primary-key-from-azure-portal>"

# 1. Connect
client = CosmosClient(ENDPOINT, credential=PRIMARY_KEY)

# 2. Select Database & Container
db = client.get_database_client("RetailDB")
container = db.get_container_client("Store")

# 3. Create/Insert a document
item = {
    "id": "STU-001",
    "customerId": "STU-001",
    "name": "Sarah Connor",
    "type": "customer"
}
container.upsert_item(item)
print("Item inserted successfully!")

# 4. Point Read (Cost: 1.0 RU, ~1ms)
result = container.read_item(item="STU-001", partition_key="STU-001")
print("Retrieved item:", result["name"])
'''
    print(code_sample)


# ==============================================================================
# LESSON 5: Real MongoDB pymongo SDK Code (When You Have Local MongoDB)
# ==============================================================================
def lesson_5_real_mongodb_sdk_template():
    print("=" * 60)
    print("LESSON 5: Real MongoDB (pymongo) Code Template")
    print("=" * 60)
    print("To connect to your local MongoDB (from Day 1), run: pip install pymongo\n")

    code_sample = '''
from pymongo import MongoClient

# 1. Connect to local server
client = MongoClient("mongodb://localhost:27017/")

# 2. Select Database & Collection
db = client["RetailDB"]
collection = db["Store"]

# 3. Insert a document
new_item = {
    "id": "STU-001",
    "name": "Sarah Connor",
    "type": "customer"
}
collection.insert_one(new_item)
print("Inserted into MongoDB!")

# 4. Read back the document
result = collection.find_one({"id": "STU-001"})
print("Found in MongoDB:", result["name"])
'''
    print(code_sample)


# ==============================================================================
# Main Execution
# ==============================================================================
if __name__ == "__main__":
    lesson_1_python_basics()
    lesson_2_read_json_file()
    lesson_3_simulated_sdk()
    lesson_4_real_cosmos_db_sdk_template()
    lesson_5_real_mongodb_sdk_template()
    print("=" * 60)
    print("🎉 Congratulations! You have completed the Python SDK 101 Starter Lab!")
    print("=" * 60)
