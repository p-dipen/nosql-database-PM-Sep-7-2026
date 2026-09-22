# Day 4: Python SDK 101 for Beginners (Zero to Your First NoSQL Script)

> **Welcome to Python!** If you have never written a line of Python in your life, do not worry. This guide was written specifically for you. By the end of this lesson, you will understand how to connect to a NoSQL database and read/write data using code.

---

## 1. Why Do We Use an SDK?

In Day 2 and Day 3, you clicked buttons in the **Azure Portal** and **MongoDB Compass**.

In real companies, websites and mobile apps cannot click buttons on a screen. When a customer buys a product on an app, code must automatically talk to the database.

An **SDK (Software Development Kit)** is simply a library of pre-written helper tools that lets your programming language (Python) talk directly to your database (Azure Cosmos DB or MongoDB) over the internet.

```text
[Your Python Code] ────(Python SDK)────> [Internet] ────> [Azure Cosmos DB / MongoDB]
```

---

## 2. Python 101: The "Aha!" Moment for NoSQL Students

Here is the best secret in NoSQL: **If you understand JSON, you already understand Python data structures!**

### In JSON:
```json
{
  "name": "Sarah Connor",
  "age": 28,
  "isStudent": true,
  "courses": ["NoSQL", "AI"]
}
```

### In Python:
```python
student = {
    "name": "Sarah Connor",
    "age": 28,
    "isStudent": True,
    "courses": ["NoSQL", "AI"]
}
```
* A JSON Object `{}` is called a **Dictionary** (`dict`) in Python.
* A JSON Array `[]` is called a **List** (`list`) in Python.
* Strings use quotes `"text"`, numbers are just numbers `28`, and booleans are `True` or `False`.

That's it! When you insert a document into NoSQL using Python, you are literally just passing a Python dictionary.

---

## 3. How to Run Python

### Check if Python is installed:
Open your Terminal (Mac) or Command Prompt (Windows) and type:
```bash
python3 --version
```
*(On Windows, you can also type `python --version`)*

### How to run any Python file:
```bash
python3 my_script.py
```

### How to install SDK libraries (`pip`):
Python uses a package manager called `pip` to install libraries. Run this one command:
```bash
pip install pymongo azure-cosmos
```

---

## 4. The 3-Step Recipe for ANY NoSQL SDK

Every NoSQL database SDK follows the exact same 3 steps:

```text
Step 1: CONNECT      ➔ Pass your connection string / endpoint + key.
Step 2: SELECT       ➔ Pick your Database and Container/Collection.
Step 3: INTERACT     ➔ Insert (create), Read (lookup), or Query (filter).
```

---

## 5. Working with MongoDB in Python (`pymongo`)

Here is the complete, beginner-friendly recipe:

```python
# 1. Import the library
from pymongo import MongoClient

# 2. Connect to local MongoDB (from Day 1)
client = MongoClient("mongodb://localhost:27017/")

# 3. Pick the Database and Collection (they will be created automatically if they don't exist!)
db = client["SchoolDB"]
collection = db["Students"]

# 4. Create a document (it's just a Python dictionary!)
new_student = {
    "studentId": "STU-99",
    "name": "Alex River",
    "program": "DSAI",
    "gpa": 3.8
}

# 5. Insert the document
collection.insert_one(new_student)
print("Successfully inserted student into MongoDB!")

# 6. Read it back
found_student = collection.find_one({"studentId": "STU-99"})
print("Found student:", found_student["name"], "- GPA:", found_student["gpa"])
```

---

## 6. Working with Azure Cosmos DB in Python (`azure-cosmos`)

Azure Cosmos DB requires an **Endpoint URL** and a **Primary Key** (which you copy from the Azure Portal under **Keys**).

```python
# 1. Import the Cosmos library
from azure.cosmos import CosmosClient

# 2. Connection details (Get these from Azure Portal -> Keys)
ENDPOINT = "https://your-cosmos-account.documents.azure.com:443/"
KEY = "your-primary-key-here"

# 3. Connect to the client
client = CosmosClient(ENDPOINT, credential=KEY)

# 4. Select Database and Container
database = client.get_database_client("CollegeDB")
container = database.get_container_client("Students")

# 5. Create a document (must have an "id" field!)
new_item = {
    "id": "STU-99",
    "studentId": "STU-99",  # Partition key
    "name": "Alex River",
    "program": "DSAI"
}

# 6. Insert or Update (upsert = insert if new, update if already exists)
container.upsert_item(new_item)
print("Successfully saved item to Azure Cosmos DB!")

# 7. Read it back using a Point Read (Fastest, cheapest 1.0 RU)
item = container.read_item(item="STU-99", partition_key="STU-99")
print("Retrieved from Cosmos DB:", item["name"])
```

---

## 7. What Happens If an Error Occurs?

In Python, we protect our code from crashing using `try` and `except`:

```python
try:
    # Try doing something risky
    item = container.read_item(item="DOES_NOT_EXIST", partition_key="DOES_NOT_EXIST")
except Exception as error:
    print("Oops! Something went wrong, but the program didn't crash:")
    print(error)
```

---

## 8. Summary of Commands Every Beginner Needs

| What You Want to Do | Python Code |
| :--- | :--- |
| **Print something to the screen** | `print("Hello World")` |
| **Store a document in a variable** | `doc = {"id": "1", "name": "Dipen"}` |
| **Get a field from a document** | `doc["name"]` (returns `"Dipen"`) |
| **Loop through a list of documents** | `for doc in documents:` <br> &nbsp;&nbsp;&nbsp;&nbsp;`print(doc["name"])` |
| **Insert into MongoDB** | `collection.insert_one(doc)` |
| **Insert into Cosmos DB** | `container.upsert_item(doc)` |
| **Read by ID in Cosmos DB** | `container.read_item(item=id, partition_key=pk)` |
