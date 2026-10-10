# Day 4: Student Lab & Practice Challenges (Student Edition)

**Course**: CBC DSAI - NoSQL Database Engineering  
**Module**: Day 4 - Data Modeling, Partitioning Mastery, Cosmos DB SQL & Python SDK 101  
**Instructions**: Solve the following challenges individually or in pairs. Queries can be tested directly in Azure Portal Data Explorer or MongoDB Compass, and Python challenges can be run in any Python terminal using `starter_python_sdk.py`.

---

## 🎯 Part 1: Data Modeling & Schema Design

### Challenge 1: The Patient Health Record System
A hospital is designing a NoSQL document database. You have the following entities:
* `Patient` (Name, Date of Birth, Blood Type, Contact Info)
* `EmergencyContact` (Name, Relationship, Phone Number - typically 1 or 2 contacts per patient)
* `MedicalVisits` (Over 20 years, a patient might visit the clinic 300+ times; each visit includes doctor notes, prescriptions, and lab tests)

**Questions**:
1. How should you model `EmergencyContact` relative to `Patient`? (Embed or Reference? Explain your reasoning).
2. How should you model `MedicalVisits` relative to `Patient`? (Embed or Reference? Explain your reasoning).
3. Draft a sample JSON document schema for the `Patient` record showing your chosen approach.

---

### Challenge 2: E-Commerce Product Reviews
An e-commerce site sells popular products. Some niche products receive 5 reviews, while flagship smartphones receive over 150,000 customer reviews over several years.
1. Why is embedding all 150,000 reviews directly into the `Product` document an architectural anti-pattern in Azure Cosmos DB?
2. What specific document size limit in Cosmos DB is at risk (e.g. 2 MB, 10 MB, 50 MB)?
3. Propose an optimal data model that supports high-speed product catalog browsing while allowing customers to view paginated reviews.

---

## 🎯 Part 2: Partition Key Architecture

### Challenge 3: Streaming Video Platform
A video streaming app stores user watch histories.
* 10 million active users worldwide.
* Users frequently view their own "Continue Watching" list upon opening the app.
* Marketing teams run a weekly batch report summarizing top trending videos worldwide.

**Questions**:
1. What property would you choose as the **Partition Key** for the `WatchHistory` container? Why?
2. What would happen to performance and scalability if you selected `/country` as the partition key?
3. What would happen if you selected `/starRating` (e.g. 1 to 5 stars) as the partition key?

---

### Challenge 4: IoT Smart Meter Hotspot Prevention
Smart electric meters report power consumption every 60 seconds across 100,000 homes. An engineer proposes using `/readingDate` (e.g. `2024-03-22`) as the partition key.
1. Explain the fatal flaw with using `/readingDate` as the partition key for write-heavy ingestion.
2. What happens to the 10,000 RU/s physical partition throughput limit when all 100,000 meters write to the same date?
3. Propose a **Synthetic Partition Key** that balances both write throughput and fast daily device queries.

---

## 🎯 Part 3: Azure Cosmos DB SQL API Queries (in Data Explorer)

Upload or inspect `sample_data.json` in **Azure Portal Data Explorer**:

### Challenge 5: Basic Filtering & Projection
Write a query to retrieve only the `id`, `name`, and `specs.batteryLifeHours` for all products in the `"Audio"` or `"Wearables"` categories that have a `price` less than $350.

### Challenge 6: Array Searching with `ARRAY_CONTAINS`
Write a query to find all products that have the tag `"smart-home"` or `"matter"`. Return the product name, price, and the full `tags` array.

### Challenge 7: Array Iteration using `JOIN`
Write a query using the `JOIN` keyword to list all products that have received a customer review with a `rating` of 5. Include the product name, reviewer name, and review comment in the output.

### Challenge 8: Existence Check with `IS_DEFINED`
Write a query to find all customers who have explicitly defined preferences for a `"newsletter"`. Return their name and email.

### Challenge 9: Aggregations with `GROUP BY`
Write a query that groups all products by `category` and returns:
- The category name
- The number of distinct products in that category
- The maximum product price in that category

### Challenge 10: Correlated Subquery with `EXISTS`
Write a query to retrieve all orders (`type = "order"`) where the customer bought at least one item with a quantity of 2 or more.

### Challenge 11: String Manipulation
Write a query to find all customers whose email address ends with `"@example.com"`. Return the customer name and an uppercase version of their membership level using the `UPPER()` function.

### Challenge 12: Pagination with `OFFSET ... LIMIT`
Write a query that retrieves products sorted by `price` descending, returning the 2nd and 3rd most expensive products (skipping the #1 most expensive product).

---

## 🎯 Part 4: Python SDK 101 Challenges (Hands-On Code)

Open a Python editor or run Python interactively:

### Challenge 13: Creating Your First Python Document
1. In Python, write a dictionary called `book` that has:
   - `id`: `"BOOK-101"`
   - `title`: `"NoSQL for AI"`
   - `price`: `49.99`
   - `tags`: A list containing `"database"`, `"nosql"`, and `"python"`
2. Print the title and the second tag using Python `print()` statements.

### Challenge 14: The 3-Step SDK Flow
Explain in your own words what the 3 steps of using any NoSQL SDK are:
1. Step 1: ___________________
2. Step 2: ___________________
3. Step 3: ___________________

### Challenge 15: Point Read vs. Query in Code
In the Azure Cosmos DB Python SDK:
- Which method performs a point read: `read_item()` or `query_items()`?
- Why is a point read preferred whenever you already know the `id` and the `partition_key`?

---

## 🎯 Part 5: Conceptual AI & Vector Search

### Challenge 16: Understanding Semantic Search
1. In regular keyword search, if a customer searches for *"sound isolation earphones"*, why might a traditional database fail to find a product titled *"NeuralNoise Cancelling Headphones"*?
2. How does **Vector Search** (semantic embeddings) solve this limitation?
3. Why is **Cosine Similarity** used instead of measuring simple keyword count?
