# Day 3: Hands-On Labs, Sizing Exercises & Certification Check

This document provides four hands-on labs and assessment modules designed to solidify your practical skills in MongoDB and Azure Cosmos DB for NoSQL.

---

# Lab 1: MongoDB Hands-On Queries & Aggregation

### Objective
Load the sample dataset into MongoDB and execute real-world queries, update operations, index creation, and multi-stage aggregation pipelines.

---

### Step 1: Import Sample Data into MongoDB
Open your terminal and run `mongoimport` (or use MongoDB Compass):

```bash
mongoimport --db store_db --collection products --file sample_data.json --jsonArray
```

Or within `mongosh`:
```javascript
use store_db
// Read and insert directly if running script in mongosh
const sampleData = cat('./sample_data.json');
db.products.insertMany(JSON.parse(sampleData));
```

---

### Step 2: Querying with Filter Operators

#### Task 2.1: Find Electronics priced between $50 and $150
```javascript
db.products.find({
  category: "Electronics",
  price: { $gte: 50, $lte: 150 }
}, { name: 1, price: 1, sku: 1, _id: 0 })
```

#### Task 2.2: Find products containing the tag `"wireless"` OR `"bluetooth"`
```javascript
db.products.find({
  tags: { $in: ["wireless", "bluetooth"] }
}, { name: 1, tags: 1 })
```

#### Task 2.3: Query nested specifications
Find products with battery life of at least 30 hours:
```javascript
db.products.find({
  "specifications.batteryLifeHours": { $gte: 30 }
}, { name: 1, "specifications.batteryLifeHours": 1 })
```

---

### Step 3: Updates with Operators

#### Task 3.1: Apply a 10% discount to all Audio products and flag them as on sale
```javascript
db.products.updateMany(
  { category: "Audio" },
  {
    $mul: { price: 0.90 },
    $set: { onSale: true, updatedAt: new Date() }
  }
)
```

#### Task 3.2: Add a new tag `"prime-shipping"` without creating duplicates
```javascript
db.products.updateOne(
  { sku: "TECH-KB-01" },
  { $addToSet: { tags: "prime-shipping" } }
)
```

---

### Step 4: Multi-Stage Aggregation Pipeline

#### Task: Aggregate inventory metrics by category
Compute:
1. Number of products in each category.
2. Average product rating (rounded to 2 decimal places).
3. Total stock quantity available.
4. Total inventory valuation (`price * stock`).
5. Filter only categories having more than 1 product.
6. Sort by total inventory value descending.

```javascript
db.products.aggregate([
  // Stage 1: Group by category
  {
    $group: {
      _id: "$category",
      totalProducts: { $sum: 1 },
      avgRating: { $avg: "$rating" },
      totalStock: { $sum: "$stock" },
      inventoryValue: { $sum: { $multiply: ["$price", "$stock"] } }
    }
  },
  // Stage 2: Filter categories with at least 2 items
  {
    $match: {
      totalProducts: { $gte: 2 }
    }
  },
  // Stage 3: Format and project output
  {
    $project: {
      _id: 0,
      category: "$_id",
      totalProducts: 1,
      avgRating: { $round: ["$avgRating", 2] },
      totalStock: 1,
      inventoryValue: { $round: ["$inventoryValue", 2] }
    }
  },
  // Stage 4: Sort descending by valuation
  {
    $sort: { inventoryValue: -1 }
  }
])
```

---

### Step 5: Index Creation & Performance Analysis

#### Task 5.1: Create a compound index supporting the ESR Rule (Equality, Sort, Range)
```javascript
db.products.createIndex({ category: 1, price: -1 })
```

#### Task 5.2: Verify index usage with `explain()`
```javascript
db.products.find({ category: "Electronics" })
  .sort({ price: -1 })
  .explain("executionStats")
```
*Expected Result*: The winning plan should use `IXSCAN` on `category_1_price_-1` without an in-memory `SORT` stage.

---

# Lab 2: Azure Cosmos DB Capacity Planning & RU Calculation

### Scenario Overview
A retail e-commerce company is migrating its order tracking service to Azure Cosmos DB for NoSQL. You are the cloud database engineer responsible for sizing the provisioned throughput.

### Workload Parameters
- **Data volume**: 2,000,000 documents initially, growing by 50,000 docs/month.
- **Average document size**: 2 KB.
- **Peak traffic pattern**:
  - **Reads**: 1,200 point reads per second (fetching order by `id` and `customerId`).
  - **Queries**: 80 queries per second (fetching customer order history, average cost: 4.5 RUs).
  - **Writes (Inserts)**: 150 new orders created per second.
  - **Updates**: 50 status updates per second.

---

### Exercise Sizing Calculations

#### 1. Calculate Read RU/s Requirement
- Point reads (2 KB item = ~1.5 RUs under Session consistency):
  $$1,200 \times 1.5 = 1,800 \text{ RU/s}$$
- Complex queries:
  $$80 \times 4.5 = 360 \text{ RU/s}$$
- **Total Read Throughput**:
  $$1,800 + 360 = 2,160 \text{ RU/s}$$

#### 2. Calculate Write RU/s Requirement
- A 2 KB insert with default indexing costs ~11 RUs:
  $$150 \times 11 = 1,650 \text{ RU/s}$$
- A 2 KB update costs ~9 RUs:
  $$50 \times 9 = 450 \text{ RU/s}$$
- **Total Write Throughput**:
  $$1,650 + 450 = 2,100 \text{ RU/s}$$

#### 3. Total Required Peak Throughput
$$\text{Peak Required RU/s} = 2,160 + 2,100 = 4,260 \text{ RU/s}$$

#### 4. Throughput Architecture Recommendation
- **Manual vs. Autoscale vs. Serverless**:
  - Serverless is capped at 5,000 RU/s and lacks multi-region write capability; unsuitable for this mission-critical load.
  - Traffic varies significantly between day and night (spiky).
  - **Recommendation**: **Autoscale Provisioned Throughput** with a maximum limit of **6,000 RU/s**.
  - System dynamically scales between $600 \text{ RU/s}$ (night) and $6,000 \text{ RU/s}$ (peak rush), saving significant hourly compute costs compared to fixed 6,000 manual RU/s.

---

# Lab 3: Cosmos DB Container Configuration & Indexing Policy

### Scenario
Configure an `Orders` container with:
1. Partition key: `/customerId`
2. Autoscale throughput: Max 4,000 RU/s
3. Time to Live: Documents expire after 90 days (7,776,000 seconds)
4. Indexing policy: Exclude massive order notes payload and add a composite index for customer order sorting.

---

### Step 1: Azure CLI Container Provisioning Script

```bash
# Variables
RESOURCE_GROUP="rg-cosmos-lab"
ACCOUNT_NAME="cosmos-retail-account"
DATABASE_NAME="RetailStoreDB"
CONTAINER_NAME="Orders"

# Create Database with shared or dedicated throughput
az cosmosdb sql database create \
  --resource-group $RESOURCE_GROUP \
  --account-name $ACCOUNT_NAME \
  --name $DATABASE_NAME

# Create Container with autoscale max 4000 RU/s, partition key, and default TTL (90 days)
az cosmosdb sql container create \
  --resource-group $RESOURCE_GROUP \
  --account-name $ACCOUNT_NAME \
  --database-name $DATABASE_NAME \
  --name $CONTAINER_NAME \
  --partition-key-path "/customerId" \
  --max-throughput 4000 \
  --ttl 7776000
```

---

### Step 2: Custom Indexing Policy JSON

Save the following as `indexing-policy.json`:

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/*"
    }
  ],
  "excludedPaths": [
    {
      "path": "/orderNotes/*"
    },
    {
      "path": "/internalDiagnosticPayload/*"
    },
    {
      "path": "/\"_etag\"/?"
    }
  ],
  "compositeIndexes": [
    [
      {
        "path": "/orderDate",
        "order": "descending"
      },
      {
        "path": "/totalAmount",
        "order": "ascending"
      }
    ]
  ]
}
```

Apply the policy via Azure CLI:
```bash
az cosmosdb sql container update \
  --resource-group $RESOURCE_GROUP \
  --account-name $ACCOUNT_NAME \
  --database-name $DATABASE_NAME \
  --name $CONTAINER_NAME \
  --idx @indexing-policy.json
```

---

# Lab 4: Certification Practice & Knowledge Check

Test your knowledge with 10 questions modeled after Microsoft Exam **DP-420** (Designing and Implementing Cloud-Native Applications Using Microsoft Azure Cosmos DB).

---

### Question 1
**You are designing a global e-commerce cart service where users add items to a cart from multiple regions. Users must always see their own updates immediately, but other users can tolerate minor replication delays. Which consistency level provides the lowest latency and RU cost while meeting this requirement?**
- A) Strong
- B) Bounded Staleness
- C) Session
- D) Consistent Prefix

> **Answer: C**
> **Explanation**: Session consistency is the default and provides *read-your-own-writes* and *monotonic reads* for the active client session token at single-region latency and 1x RU cost. Strong and Bounded Staleness cost 2x RUs and incur higher latency.

---

### Question 2
**You have an Azure Cosmos DB container with 500 GB of data. The container is configured with manual provisioned throughput of 10,000 RU/s. How many physical partitions are created at minimum?**
- A) 1
- B) 5
- C) 10
- D) 11

> **Answer: C**
> **Explanation**: A physical partition in Cosmos DB supports up to 50 GB of storage and up to 10,000 RU/s. To store 500 GB of data: $\frac{500 \text{ GB}}{50 \text{ GB}} = 10 \text{ physical partitions}$.

---

### Question 3
**You need to run a query that filters on `storeId` and sorts results by `orderDate DESC` and `totalCost ASC`. When you run the query, it fails with an error stating that the query requires a composite index. What should you do?**
- A) Enable serverless throughput on the container.
- B) Add a composite index on `(orderDate DESC, totalCost ASC)` in the indexing policy.
- C) Change the container consistency level to Strong.
- D) Re-index the container with `indexingMode: none`.

> **Answer: B**
> **Explanation**: Any query with an `ORDER BY` clause involving two or more properties requires a composite index matching the exact properties and sort orders.

---

### Question 4
**You want temporary session tokens to automatically expire after 1,800 seconds (30 minutes). You enable TTL on the container with `DefaultTimeToLive = -1`. What happens to items inserted into this container?**
- A) All items will expire after 1,800 seconds automatically.
- B) All items are deleted immediately.
- C) Items will only expire if they contain a `"ttl": 1800` property in their individual JSON document.
- D) The container returns HTTP error 400.

> **Answer: C**
> **Explanation**: Setting `DefaultTimeToLive = -1` (On, no default) means TTL is enabled on the container, but items will not expire unless individual documents explicitly include a `ttl` integer property specifying their lifespan in seconds.

---

### Question 5
**You need to migrate 2 TB of historical operational data from an on-premises MongoDB instance to Azure Cosmos DB for NoSQL with minimal cost and maximum speed during a scheduled weekend maintenance window. Which strategy should you execute?**
- A) Keep throughput at 400 RU/s and use single `insertOne()` calls.
- B) Temporarily scale up container throughput to 50,000 RU/s, temporarily set `indexingMode: none`, use Azure Data Factory or bulk executor, and restore indexes and baseline RU/s post-migration.
- C) Use Consistent Prefix consistency and replicate over public internet without partition keys.
- D) Change database throughput to serverless.

> **Answer: B**
> **Explanation**: Best practices for mass bulk migration include pre-scaling RU/s to accommodate high ingestion volume without HTTP 429 throttling, disabling indexing (`indexingMode: none`) to save write RUs, using parallel bulk ingestion tools, and re-enabling indexing once loading completes.

---

### Question 6
**In MongoDB, what is the primary difference between `$push` and `$addToSet` when updating an array?**
- A) `$push` sorts the array, while `$addToSet` reverses it.
- B) `$push` appends the element unconditionally, potentially creating duplicates; `$addToSet` only appends if the value does not already exist.
- C) `$addToSet` only works on numbers.
- D) `$push` creates a new collection.

> **Answer: B**
> **Explanation**: `$addToSet` treats the target array as a mathematical set, ensuring uniqueness by preventing duplicate values from being inserted.

---

### Question 7
**Which aggregation pipeline stage in MongoDB is used to flatten/deconstruct an array field into individual documents for each element?**
- A) `$project`
- B) `$unwind`
- C) `$lookup`
- D) `$group`

> **Answer: B**
> **Explanation**: `$unwind` deconstructs an array field from the input documents to output a document for each element in the array.

---

### Question 8
**An application using Azure Cosmos DB for NoSQL frequently encounters HTTP status code 429. What does this indicate?**
- A) Authentication token expired.
- B) The item was not found.
- C) Request rate is too large (RU/s exceeded provisioned throughput).
- D) A composite index is missing.

> **Answer: C**
> **Explanation**: HTTP 429 is `RequestRateTooLarge`. It indicates that the consumed Request Units exceeded the provisioned RU/s for that partition or container.

---

### Question 9
**What is the minimum throughput that can be configured when provisioning Autoscale on a Cosmos DB container?**
- A) 100 RU/s
- B) 400 RU/s
- C) 1,000 RU/s (scales between 100 and 1,000 RU/s)
- D) 10,000 RU/s

> **Answer: C**
> **Explanation**: For Autoscale provisioned throughput, the minimum configurable maximum throughput ($T_{max}$) is 1,000 RU/s, which automatically scales between 100 RU/s (10%) and 1,000 RU/s (100%).

---

### Question 10
**You have 20 small lookup containers in a single Azure Cosmos DB database. Each container receives minimal, infrequent requests (1-2 queries per minute). What is the most cost-effective throughput configuration?**
- A) Provision dedicated 400 RU/s on each of the 20 containers individually.
- B) Provision shared database-level throughput of 400 RU/s across all 20 containers.
- C) Use Strong consistency across multiple regions.
- D) Set autoscale to 20,000 RU/s.

> **Answer: B**
> **Explanation**: Provisioning shared database throughput allows all 20 containers to share a single 400 RU/s pool, costing significantly less than provisioning 20 dedicated containers at 400 RU/s each ($20 \times 400 = 8,000 \text{ RU/s}$).
