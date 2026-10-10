# Day 4: Hands-On Labs, Exercises & Certification Practice (Solutions Included)

This workbook contains practical scenarios, architectural modeling challenges, visual queries with solutions, and 10 DP-420 certification-style practice questions. All practical exercises can be executed directly inside the **Azure Portal Data Explorer** or **MongoDB Compass**—no programming required!

---

## 🛠️ Lab 1: Refactoring a Relational Schema into an Optimized Document Model

### Scenario
An online educational platform is migrating its SQL Server database to Azure Cosmos DB for NoSQL. In SQL Server, the schema is normalized across 4 tables:

```text
[Students] (StudentID, Name, Email)
    │
    ├──< [Enrollments] (EnrollmentID, StudentID, CourseID, EnrollmentDate, Status)
            │
            └──> [Courses] (CourseID, Title, InstructorID, Credits)
                    │
                    └──> [Instructors] (InstructorID, Name, Office)
```

**Access Patterns**:
1. When a student logs in, display their profile and their list of enrolled courses with course titles and status. (Executed 50,000 times/day).
2. Course titles rarely change.
3. Students never enroll in more than 40 courses over their academic lifetime.

### Task
Design the single optimized Cosmos DB JSON document structure for a student and justify your embedding vs. referencing decisions.

### ✅ Solution & Rationale

```json
{
  "id": "STU-1001",
  "type": "student",
  "studentId": "STU-1001",
  "name": "Jordan Miller",
  "email": "jordan.m@cbc.ca",
  "enrolledCourses": [
    {
      "courseId": "DSAI-101",
      "courseTitle": "NoSQL Database Engineering",
      "credits": 3,
      "enrollmentDate": "2024-01-10",
      "status": "Active",
      "instructorName": "Prof. Parihar"
    },
    {
      "courseId": "DSAI-102",
      "courseTitle": "Machine Learning Foundations",
      "credits": 4,
      "enrollmentDate": "2024-01-10",
      "status": "Completed",
      "instructorName": "Dr. Sarah Chen"
    }
  ]
}
```

#### Architectural Rationale:
1. **Embedding `enrolledCourses`**:
   - The cardinality is bounded (maximum 40 courses lifetime), well within the 2 MB document limit.
   - The primary access pattern (student profile lookup) can be fulfilled with a **single 1.0 RU point read** (`ReadItem(id, studentId)`), completely eliminating multi-table joins.
2. **Denormalizing `courseTitle` and `instructorName`**:
   - Course titles change very infrequently. Reading them together avoids secondary lookups to a separate `Courses` container.

---

## 🛠️ Lab 2: Partition Key Selection for Real-World Scenarios

### Scenario A: Fleet Telemetry Ingestion
- **Context**: 5,000 delivery trucks send GPS location, speed, and fuel readings every 5 seconds.
- **Query Pattern**: Fetch the latest 1 hour of telemetry for a specific truck.
- **Candidate Keys**: `truckId`, `status`, `readingDate`, `truckId_date`.
- **Selected Key**: `truckId_date` (e.g. `TRUCK_401_20240322`).
- **Justification**:
  - `status` has very low cardinality (causes severe hot partitions).
  - `readingDate` routes all 5,000 trucks on any given day to the exact same physical partition, throttling the 10,000 RU/s cap.
  - `truckId_date` spreads the write load across 5,000 trucks, guarantees logical partitions stay well below 20 GB, and keeps truck queries single-partition.

### Scenario B: Multi-Tenant B2B SaaS Platform
- **Context**: An enterprise SaaS application stores documents for 1,200 corporate clients (tenants).
- **Access Pattern**: 99.9% of queries filter by `tenantId`. Small tenants have 50 MB of data; largest tenant has 8 GB of data.
- **Selected Key**: `tenantId`.
- **Justification**:
  - Perfect isolation: every client query is routed to a single logical partition.
  - Largest tenant (8 GB) is well within the 20 GB logical partition limit.
  - High cardinality (1,200 tenants) allows Azure to balance physical partitions evenly.

---

## 🛠️ Lab 3: Cosmos DB Data Explorer Query Lab (on `sample_data.json`)

Open **Azure Portal → Data Explorer** (or inspect against `sample_data.json`):

### Challenge 1: Find all Platinum customers living in Toronto
```sql
SELECT c.customerId, c.name, c.email, c.address.city, c.membershipLevel
FROM c
WHERE c.type = "customer" 
  AND c.membershipLevel = "Platinum" 
  AND c.address.city = "Toronto"
```

### Challenge 2: Find all products with the tag 'wireless' and price under $320
```sql
SELECT c.name, c.price, c.category, c.tags
FROM c
WHERE c.type = "product" 
  AND c.price < 320 
  AND ARRAY_CONTAINS(c.tags, "wireless")
```

### Challenge 3: Flatten line items to calculate item sales value
```sql
SELECT 
    c.orderId,
    c.customerId,
    item.productName,
    item.quantity,
    item.unitPrice,
    item.lineTotal
FROM c
JOIN item IN c.items
WHERE c.type = "order"
```

### Challenge 4: Find all orders that contain at least one item costing more than $250
```sql
SELECT c.orderId, c.customerId, c.totalAmount
FROM c
WHERE c.type = "order"
  AND EXISTS (
      SELECT 1 
      FROM item IN c.items 
      WHERE item.unitPrice > 250
  )
```

### Challenge 5: Calculate total inventory and average rating per product category
```sql
SELECT 
    c.category,
    COUNT(1) AS productCount,
    SUM(c.inventory) AS totalStock,
    AVG(c.rating) AS averageRating
FROM c
WHERE c.type = "product"
GROUP BY c.category
```

---

## 🛠️ Lab 4: MongoDB Compass Visual Aggregation Lab

Open **MongoDB Compass** and navigate to the **Aggregations** tab:

### Goal: Calculate Total Revenue by Product Name
1. Click **Add Stage**:
   * Stage: `$match`
   * Filter: `{ "type": "order" }`
2. Click **Add Stage**:
   * Stage: `$unwind`
   * Path: `"$items"`
3. Click **Add Stage**:
   * Stage: `$group`
   * Body:
     ```javascript
     {
       _id: "$items.productName",
       totalRevenue: { $sum: "$items.lineTotal" },
       totalSold: { $sum: "$items.quantity" }
     }
     ```
4. Click **Add Stage**:
   * Stage: `$sort`
   * Body: `{ "totalRevenue": -1 }`

**Result**: You will visually see the ranked products by revenue directly in the Compass interface!

---

## 🎓 DP-420 Certification Practice Questions

#### Question 1
You are designing an Azure Cosmos DB for NoSQL container to store e-commerce customer orders. The application frequently queries orders for a specific customer. Orders are never updated once delivered. Which property should you select as the partition key?
- A) `/orderStatus`
- B) `/orderDate`
- C) `/customerId`
- D) `/country`

**Correct Answer**: **C**  
**Explanation**: `customerId` provides high cardinality and ensures that the most frequent query ("retrieve orders for a customer") is a cheap, fast single-partition query. `orderStatus` and `country` have low cardinality and create hot partitions.

---

#### Question 2
You have a Cosmos DB container with 15 physical partitions. You run a query in Data Explorer that does NOT include the partition key in the `WHERE` clause. What is the impact?
- A) The query fails with an HTTP 400 error.
- B) The query fans out across all 15 physical partitions in parallel, consuming higher RU/s.
- C) Cosmos DB queries only the primary physical partition.
- D) Cosmos DB automatically alters the partition key.

**Correct Answer**: **B**  
**Explanation**: Queries omitting the partition key are cross-partition fan-out queries. The Cosmos DB engine must send subqueries to all physical partitions and merge the results, consuming significantly higher RU/s.

---

#### Question 3
What is the maximum storage limit for a single logical partition in Azure Cosmos DB?
- A) 2 MB
- B) 10 GB
- C) 20 GB
- D) 50 GB

**Correct Answer**: **C**  
**Explanation**: Each logical partition (all documents sharing the same partition key value) is limited to **20 GB**. Individual items/documents are limited to **2 MB**. Physical partitions can hold up to **50 GB**.

---

#### Question 4
You need to model a social media post that will receive hundreds of thousands of comments. Which modeling approach should you adopt?
- A) Embed all comments as an array inside the post document.
- B) Store each comment as a separate document referencing the `postId`.
- C) Create a new Cosmos DB database for every post.
- D) Store comments in an XML property inside the post.

**Correct Answer**: **B**  
**Explanation**: Hundreds of thousands of comments represents an unbounded 1:Many relationship. Embedding them would quickly breach the 2 MB item size limit. Comments must be stored as individual documents with `postId` as the partition key or reference.

---

#### Question 5
In Azure Cosmos DB SQL API, what is the purpose of the `JOIN` keyword?
- A) To perform an inner join between two distinct containers.
- B) To join Cosmos DB with an Azure SQL database.
- C) To perform an intra-document self-join that flattens arrays inside a single document.
- D) To merge two databases.

**Correct Answer**: **C**  
**Explanation**: Cosmos DB does not support cross-container or cross-database joins. `JOIN` is strictly scoped to the document itself to iterate over nested array elements.

---

#### Question 6
You are writing a query in Data Explorer to retrieve items where the optional field `discountPercentage` is present. Which system function should you use?
- A) `HAS_PROPERTY(c.discountPercentage)`
- B) `IS_DEFINED(c.discountPercentage)`
- C) `EXISTS(c.discountPercentage)`
- D) `IS_NULL(c.discountPercentage)`

**Correct Answer**: **B**  
**Explanation**: `IS_DEFINED()` is the built-in Cosmos DB SQL function that evaluates whether a specified property exists on a document.

---

#### Question 7
In the Azure Portal Data Explorer **Query Stats** tab, what metric indicates the cost of the query in Azure Cosmos DB?
- A) Network Bandwidth (Mbps)
- B) Request Charge (RUs)
- C) Storage Footprint (KB)
- D) CPU Utilization (%)

**Correct Answer**: **B**  
**Explanation**: In Azure Cosmos DB, every database operation (reads, writes, queries) is measured in **Request Units (RUs)**. The Request Charge in Query Stats displays this exact cost.

---

#### Question 8
You have a query:
```sql
SELECT * FROM c WHERE c.type = "product" ORDER BY c.category ASC, c.price DESC
```
The query fails in Cosmos DB Data Explorer. What is the most likely cause?
- A) SQL API does not support `ORDER BY`.
- B) The container lacks a composite index covering `(category ASC, price DESC)`.
- C) Cosmos DB cannot sort numeric fields.
- D) `type` cannot be used in a `WHERE` clause.

**Correct Answer**: **B**  
**Explanation**: Any query with multiple `ORDER BY` properties, or a mix of ASC and DESC sorting across fields, requires a **Composite Index** defined in the indexing policy.

---

#### Question 9
In AI and vector search, why is Cosine Similarity commonly preferred over Euclidean Distance for text embeddings?
- A) Cosine similarity only works with integers.
- B) Cosine similarity measures the angle between vectors, normalizing for document length.
- C) Euclidean distance cannot be computed in NoSQL.
- D) Cosine similarity requires 10x less memory.

**Correct Answer**: **B**  
**Explanation**: Text embeddings generated by language models represent semantic direction. Cosine similarity evaluates the angle between vectors rather than their magnitude, making it invariant to text length.

---

#### Question 10
In MongoDB Compass, what does a red **COLLSCAN** warning in the Explain Plan tab signify?
- A) The database is offline.
- B) MongoDB had to scan every single document on disk because no index was available.
- C) The collection has reached the maximum size.
- D) The query contains a syntax error.

**Correct Answer**: **B**  
**Explanation**: COLLSCAN means "Collection Scan". MongoDB was forced to read every document in the collection one by one, which is slow and resource-intensive on large datasets. Creating an index converts it to an efficient **IXSCAN** (Index Scan).
