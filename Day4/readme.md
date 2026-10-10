# Day 4: NoSQL Data Modeling, Partitioning Mastery, Visual Tools & Python SDK 101

Welcome to **Day 4** of the NoSQL Database course!

In **Days 1–3**, we built a strong foundation: understanding NoSQL data structures, exploring Azure Cosmos DB's resource hierarchy, mastering MongoDB BSON internals, query operators, and aggregation pipelines, and configuring Cosmos DB capacity, consistency, throughput, and indexing.

Today, in **Day 4**, we advance into core architectural design and introduce the **Python NoSQL SDK** step-by-step:

1. **Data Modeling & Partitioning Architecture**: Learning how to design schemas for high-scale document databases (Embedding vs. Referencing, physical vs. logical partitions, hot partition prevention, synthetic partition keys, and RU query cost optimization).
2. **Azure Cosmos DB SQL API Mastery**: Executing expressive SQL queries in Azure Data Explorer against nested JSON documents, self-joins on arrays, system functions (`ARRAY_CONTAINS`, `IS_DEFINED`, string/math), correlated subqueries, and pagination with `OFFSET ... LIMIT`.
3. **Visual Tools (Azure Data Explorer & MongoDB Compass)**:
   - Reading **Query Stats & Request Unit (RU) charges** directly in the Azure Portal.
   - Using the **Schema Tab** in MongoDB Compass for visual data profiling without writing code.
   - Constructing aggregations stage-by-stage with real-time previews using the **Aggregation Pipeline Builder**.
   - Checking query performance visually with the **Explain Plan** tab (Index Scan vs. Collection Scan).
4. **Python SDK 101 for Beginners (Course Outline Requirement)**:
   - Learning how Python **Dictionaries** (`dict`) and **Lists** (`list`) map 1-to-1 to JSON objects and arrays.
   - The 3-step recipe for connecting any programming language to a NoSQL database (`Connect` ➔ `Select` ➔ `Interact`).
   - Running your first script to read, insert, and query documents with `azure-cosmos` and `pymongo`.
5. **Vector Search & AI in NoSQL (DSAI Conceptual Spotlight)**: How modern NoSQL databases power Generative AI and Retrieval-Augmented Generation (RAG) by storing vector embeddings directly inside JSON documents.

---

## 📚 Learning Modules & Table of Contents

| Resource | Description |
| :--- | :--- |
| **[1. Data Modeling & Partitioning Guide](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/data_modeling_and_partitioning.md)** | Deep architectural guide covering Relational 3NF vs NoSQL Denormalization, embedding vs referencing decision trees, logical/physical partition limits (20 GB / 10k RU/s), hot partition prevention, synthetic partition keys, and single vs cross-partition query economics. |
| **[2. Cosmos DB SQL API Query Guide](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/cosmos_db_sql_queries.md)** | Complete guide to querying JSON in Cosmos DB: dot/bracket notation, intra-document `JOIN` on arrays, system functions (`ARRAY_CONTAINS`, `IS_DEFINED`, string, math), correlated subqueries with `EXISTS`, pagination with `OFFSET ... LIMIT`, and query RU optimization. |
| **[3. Azure Data Explorer & Compass Visual Guide](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/mongodb_compass_and_portal_guide.md)** | Visual tools guide: using Azure Portal Data Explorer to inspect Request Charge (RU costs), running queries, and using MongoDB Compass's visual Schema analyzer, Aggregation Pipeline Builder, and Explain Plan. |
| **[4. Python Crash Course for NoSQL (30-Min)](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/python_crash_course_for_nosql.md)** | **Start here if you don't know Python!** 5 visual concepts: variables, dictionaries/lists (JSON bridge), dot notation, imports, and loops with real-world analogies. |
| **[5. Python SDK 101 Beginner Guide](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/python_sdk_beginner_guide.md)** | A gentle, zero-experience-required guide explaining `pip` installation and the 3-step SDK recipe for MongoDB and Azure Cosmos DB. |
| **[6. Python Starter Lab Script (`starter_python_sdk.py`)](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/starter_python_sdk.py)** | Interactive, step-by-step runnable Python script with 5 bite-sized lessons that run right on any laptop without needing external cloud accounts. |
| **[7. JSON & JSON Arrays Sandbox Practice (`json_and_arrays_practice.py`)](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/json_and_arrays_practice.py)** | **Self-testing student coding lab!** 7 hands-on exercises covering JSON documents, nested dictionaries, JSON arrays, query filtering, and aggregations. [Solutions available here](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/json_and_arrays_practice_solutions.py). |
| **[8. Vector Search & AI in NoSQL Guide](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/vector_search_and_ai.md)** | AI concepts guide covering vector embeddings, hybrid search (metadata filter + semantic vector similarity), distance metrics (Cosine vs Euclidean vs Dot Product), Flat vs IVF vs HNSW indexes, Cosmos DB `VectorDistance()`, and RAG pipelines. |
| **[9. Hands-On Labs & Certification Solutions](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/labs_and_exercises.md)** | Comprehensive practical workbook: relational-to-document refactoring lab, real-world partition key selection scenarios, 5 Cosmos DB SQL challenges with full solutions, visual Compass aggregation lab, and 10 DP-420 certification exam questions with detailed explanations. |
| **[10. Student Lab Sheet (No Answers)](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/student_lab.md)** | Hands-on practice challenges across modeling, partitioning, Cosmos DB SQL queries in Data Explorer, visual Compass schema analysis, and beginner Python SDK tasks designed for classroom exercises or homework. |
| **[11. Sample Dataset (`sample_data.json`)](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/sample_data.json)** | Clean, multi-entity e-commerce dataset (customers, products with specs/reviews/embeddings, orders with line items) ready for instant upload into Azure Cosmos DB Data Explorer, MongoDB Compass, or Python scripts. |
| **[12. Advanced Python & Vector Demo (`demo_nosql_python.py`)](file:///Users/dipenparihar/Documents/CBC/DSAI/NoSQL/Day4/demo_nosql_python.py)** | *(Advanced Preview)* A complete demo script showing Pandas DataFrame aggregations and Cosine Similarity vector search. |

---

## 🎯 Learning Objectives

By the end of Day 4, students will be able to:
1. **Architect High-Performance Document Models**:
   - Apply the 1:1, 1:Few, 1:Many Unbounded, and Many:Many decision frameworks to choose between embedding and referencing.
   - Refactor multi-table relational schemas into single-read denormalized document models.
2. **Master Cosmos DB Partitioning**:
   - Differentiate between Logical (20 GB) and Physical (50 GB / 10,000 RU/s) partitions.
   - Prevent storage and throughput hot partitions by selecting high-cardinality keys.
3. **Execute Complex Cosmos DB SQL Queries in Azure Portal**:
   - Query nested arrays using the intra-document `JOIN` keyword.
   - Filter documents using array functions (`ARRAY_CONTAINS`), existence checks (`IS_DEFINED`), and subqueries (`EXISTS`).
   - Read and interpret **Query Stats** (Request Units / RU cost) in Azure Data Explorer.
4. **Master Visual MongoDB Compass Tools**:
   - Analyze dataset distributions and detect missing fields visually using the **Schema Tab**.
   - Build multi-stage pipelines with live previews using the visual **Aggregation Pipeline Builder**.
5. **Understand and Run Python NoSQL SDK Code**:
   - Understand how Python dictionaries and lists represent JSON documents.
   - Follow the 3-step SDK pattern (`Connect` ➔ `Select` ➔ `Interact`) to read and write items using code.

---

## 🚀 How to Run the Beginner Python SDK Lab

Open your terminal or command prompt and run:

```bash
cd Day4
python3 starter_python_sdk.py
```

This will run all 5 interactive lessons and print friendly explanations right on the screen!
