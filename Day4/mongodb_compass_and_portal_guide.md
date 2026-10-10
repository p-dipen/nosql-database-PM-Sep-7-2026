# Day 4: Azure Portal Data Explorer & MongoDB Compass Visual Mastery

As database engineers and data analysts, you do not need to be a software developer or Python programmer to inspect, query, and manage NoSQL databases. The two premier tools used daily in enterprise environments are:
1. **Azure Portal Data Explorer** (for Azure Cosmos DB)
2. **MongoDB Compass** (the official visual GUI for MongoDB)

This guide walks you through navigating, querying, and analyzing your data visually with zero code required.

---

## Part 1: Azure Cosmos DB Data Explorer

The **Data Explorer** is a web-based management tool built directly into the Azure Portal. It allows you to create collections, insert documents, run queries, and inspect real-time performance metrics.

```text
Azure Portal 
  └── Your Cosmos DB Account
        └── Data Explorer (left-hand sidebar)
              ├── Database: "RetailDB"
              │     └── Container: "ECommerce"
              │           ├── Items (View/Edit JSON)
              │           ├── Settings (RU/s, Indexing, TTL)
              │           └── New SQL Query (Query Editor)
```

### 1. How to Import Sample Data in Data Explorer
1. Open the [Azure Portal](https://portal.azure.com).
2. Navigate to your Cosmos DB Account.
3. Click **Data Explorer** in the left navigation menu.
4. Expand your Database and click on your Container (or create one: Database `RetailDB`, Container `Store`, Partition Key `/customerId`).
5. Click **Items** in the container menu.
6. Click **Upload Item** on the toolbar, select `sample_data.json`, and upload.
7. Click on any document in the list to inspect and edit its JSON structure directly in the portal.

---

### 2. Running SQL Queries & Reading Query Metrics
To execute queries:
1. Click **New SQL Query** in the toolbar.
2. Enter your query, for example:
   ```sql
   SELECT c.name, c.price, c.category
   FROM c
   WHERE c.type = "product" AND c.price > 150
   ```
3. Click **Execute Query** (or press `Ctrl + Enter`).
4. In the bottom results pane, switch between **Results** (viewing output JSON) and **Query Stats**.

### Why "Query Stats" is Critical:
The **Query Stats** tab shows:
* **Request Charge**: The exact number of Request Units (RU) consumed by your query (e.g., `2.83 RUs`).
* **Retrieved Document Count**: How many documents Cosmos DB had to scan.
* **Output Document Count**: How many documents were returned.
> **Rule of thumb**: If Retrieved Document Count is 1,000 but Output Document Count is only 2, your query is inefficient and needs an index!

---

## Part 2: MongoDB Compass Visual Mastery

**MongoDB Compass** is the official graphical user interface (GUI) for MongoDB. It allows you to explore your schema, run queries, and visualize aggregation pipelines without memorizing complex syntax.

```text
MongoDB Compass GUI
├── [Documents Tab]   ➔ Browse, filter, insert, and edit JSON documents
├── [Aggregations Tab]➔ Visual drag-and-drop pipeline builder with live previews
├── [Schema Tab]      ➔ Instant statistical charts of fields and data types
└── [Explain Plan Tab]➔ Visual performance diagnostics (Index scan vs. Collection scan)
```

---

### 1. The Schema Tab: Instant Data Profiling
One of Compass's most powerful features for data analysts is the **Schema Tab**:
1. Click on your collection in the left sidebar.
2. Click the **Schema** tab at the top.
3. Click **Analyze Schema**.
4. Compass automatically samples your documents and generates:
   * **Data Type Distribution**: Shows if a field is a string in 90% of documents and an integer in 10% (detecting dirty data!).
   * **Value Frequency Charts**: Bar charts showing the most common categories, price ranges, or dates.
   * **Missing Field Detection**: Highlights documents that are missing required fields.

---

### 2. The Visual Aggregation Pipeline Builder
Instead of writing complex nested JSON code for aggregations, Compass gives you a **stage-by-stage visual builder**:

1. Click the **Aggregations** tab in Compass.
2. Click **Add Stage**.
3. **Stage 1 (`$match`)**:
   * Select `$match` from the dropdown.
   * Enter: `{ type: "order" }`
   * Notice that Compass immediately shows a live preview of matching documents on the right-hand panel!
4. **Stage 2 (`$unwind`)**:
   * Click **Add Stage**.
   * Select `$unwind`.
   * Enter: `"$items"`
   * The live preview instantly shows your order documents flattened per line item!
5. **Stage 3 (`$group`)**:
   * Click **Add Stage**.
   * Select `$group`.
   * Enter:
     ```javascript
     {
       _id: "$items.productName",
       totalRevenue: { $sum: "$items.lineTotal" },
       totalSold: { $sum: "$items.quantity" }
     }
     ```
6. Compass previews the final grouped revenue table in real-time. If you make a mistake in any stage, you see the error immediately without crashing your application.

---

### 3. The Explain Plan Tab: Query Optimization
How do you know if your query is fast or slow?
1. Click the **Explain Plan** tab.
2. Type a query filter, e.g., `{ "category": "Audio" }`.
3. Click **Explain**.
4. Compass displays a visual diagnostic card:
   * **COLLSCAN (Red/Warning)**: Collection Scan. MongoDB had to read every single document on disk because no index existed.
   * **IXSCAN (Green/Success)**: Index Scan. MongoDB used an index to jump directly to the matching records in milliseconds.

---

## Summary Comparison: Azure Data Explorer vs. MongoDB Compass

| Feature | Azure Cosmos DB Data Explorer | MongoDB Compass |
| :--- | :--- | :--- |
| **Interface** | Web-based (Azure Portal) | Desktop Application (Mac / Windows / Linux) |
| **Query Language** | SQL API (`SELECT ... FROM c`) | MongoDB Query Language (MQL) |
| **Schema Analysis** | Manual inspection / Query Stats | Visual **Schema Tab** with automatic charts |
| **Aggregation Tool**| SQL `GROUP BY` and subqueries | Visual **Aggregation Pipeline Builder** |
| **Performance Check**| **Query Stats** tab (RU Cost) | **Explain Plan** tab (IXSCAN vs COLLSCAN) |
| **Target Audience** | Cloud architects, Data engineers | Data analysts, Database administrators |
