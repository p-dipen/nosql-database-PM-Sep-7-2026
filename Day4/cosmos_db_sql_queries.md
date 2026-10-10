# Day 4: Azure Cosmos DB for NoSQL - SQL API Query Mastery

Azure Cosmos DB for NoSQL allows developers and data scientists to query hierarchical JSON documents using a familiar **SQL-like dialect**. While the syntax resembles ANSI SQL (`SELECT`, `FROM`, `WHERE`), it includes specialized extensions for handling nested objects, arrays, and JSON-specific data structures.

---

## 1. Core Syntax & The Document Alias

In Cosmos DB SQL API, the container is represented as the collection source, and every document is typically aliased using a single letter (commonly `c` for container):

```sql
SELECT c.id, c.name, c.email
FROM c
WHERE c.type = "customer"
```

### Accessing Nested Objects & Fields
1. **Dot Notation**: Used for standard alphanumeric field names:
   ```sql
   SELECT c.name, c.address.city, c.address.province
   FROM c
   WHERE c.address.country = "Canada"
   ```
2. **Bracket Notation (`c["field"]`)**: Required when property names have special characters, hyphens, or spaces:
   ```sql
   SELECT c["order-id"], c["total amount"]
   FROM c
   WHERE c["postal-code"] = "M4B 1B3"
   ```

### Custom Schema Projection (Constructing New JSON on the Fly)
You can reshape query outputs directly into custom JSON structures:
```sql
SELECT 
    c.id AS customerId,
    c.name AS fullName,
    {
        "location": c.address.city || ", " || c.address.province,
        "isCanada": (c.address.country = "Canada")
    } AS locationInfo
FROM c
WHERE c.type = "customer"
```

---

## 2. Querying Nested Arrays: The `JOIN` Keyword

In relational SQL, `JOIN` combines two separate tables. In Cosmos DB, `JOIN` is an **intra-document self-join** used to iterate over and flatten arrays inside a single document.

### Scenario: Find All Individual Line Items Purchased Across All Orders
To query the items array inside each order:

```sql
SELECT 
    c.orderId,
    c.orderDate,
    item.productId,
    item.productName,
    item.unitPrice,
    item.quantity
FROM c
JOIN item IN c.items
WHERE c.type = "order"
```

### Filtering on Array Items via Self-Join:
```sql
SELECT 
    c.orderId,
    item.productName,
    item.lineTotal
FROM c
JOIN item IN c.items
WHERE item.lineTotal > 200
```

---

## 3. Powerful System Functions

Cosmos DB provides built-in system functions that execute server-side with zero client overhead.

### A. Array Functions

| Function | Example | Description |
| :--- | :--- | :--- |
| `ARRAY_CONTAINS(arr, val [, partial])` | `ARRAY_CONTAINS(c.tags, "wireless")` | Returns true if the array contains the value |
| `ARRAY_LENGTH(arr)` | `ARRAY_LENGTH(c.items) >= 2` | Returns the number of elements in the array |
| `ARRAY_SLICE(arr, start, len)` | `ARRAY_SLICE(c.reviews, 0, 3)` | Returns a subset slice of elements |

#### Example: Find Products with Specific Tags
```sql
SELECT c.name, c.price, c.tags
FROM c
WHERE c.type = "product" 
  AND ARRAY_CONTAINS(c.tags, "audio")
```

---

### B. Type Checking & Existence Functions

Because NoSQL documents are schema-flexible, some documents may omit fields entirely.

```sql
SELECT c.name, c.email
FROM c
WHERE IS_DEFINED(c.preferences.newsletter)
  AND c.preferences.newsletter = true
```

* `IS_DEFINED(expr)`: Returns true if the property exists in the document.
* `IS_ARRAY(expr)`: Verifies if the target property is an array.
* `IS_NUMBER(expr)`, `IS_STRING(expr)`, `IS_BOOL(expr)`: Verifies property data types.

---

### C. String Functions

| Function | Example | Description |
| :--- | :--- | :--- |
| `CONTAINS(str, substr [, caseInsensitive])` | `CONTAINS(c.name, "Smart", true)` | Case-insensitive substring match |
| `STARTSWITH(str, prefix)` | `STARTSWITH(c.email, "sarah")` | Checks prefix string |
| `ENDSWITH(str, suffix)` | `ENDSWITH(c.email, "@example.com")` | Checks domain suffix |
| `UPPER(str)`, `LOWER(str)` | `UPPER(c.membershipLevel)` | Case conversion |
| `SUBSTRING(str, start, len)` | `SUBSTRING(c.orderDate, 0, 10)` | Extracts date string `YYYY-MM-DD` |

---

### D. Mathematical & Aggregate Functions

```sql
SELECT 
    c.category,
    COUNT(1) AS totalProducts,
    AVG(c.price) AS averagePrice,
    MIN(c.price) AS minPrice,
    MAX(c.price) AS maxPrice
FROM c
WHERE c.type = "product"
GROUP BY c.category
```

> [!NOTE]
> `GROUP BY` in Azure Cosmos DB requires the container's indexing policy to support the queried path. Aggregate queries consume Request Units based on the number of items evaluated.

---

## 4. Correlated Subqueries & `EXISTS`

Correlated subqueries allow you to evaluate nested arrays without flattening the parent document.

### Example: Find Orders that Contain at Least One Item Costing > $300
```sql
SELECT c.orderId, c.customerId, c.totalAmount
FROM c
WHERE c.type = "order"
  AND EXISTS (
      SELECT 1 
      FROM item IN c.items 
      WHERE item.unitPrice >= 300
  )
```

---

## 5. Pagination with `OFFSET` and `LIMIT`

To build performant user interfaces, search results, or data science batches, use `OFFSET` and `LIMIT`:

```sql
SELECT c.id, c.name, c.price, c.rating
FROM c
WHERE c.type = "product"
ORDER BY c.price DESC
OFFSET 0 LIMIT 10
```

* `OFFSET 0 LIMIT 10` returns the first 10 items (Page 1).
* `OFFSET 10 LIMIT 10` skips the first 10 items and returns the next 10 (Page 2).

> [!TIP]
> **Composite Index Requirement**: Any query combining `ORDER BY` with multiple properties, or combining equality filters with `ORDER BY`, requires a **Composite Index** configured in the container's indexing policy. Without it, Cosmos DB will reject the query.

---

## 6. Query Performance & RU Optimization Checklist

When evaluating query performance in the Azure Portal Data Explorer or via SDKs, check the **Query Metrics** tab:

1. **Include the Partition Key**:
   * Single-Partition Query: `WHERE c.customerId = "CUST-001"` costs **~2.8 RUs**.
   * Cross-Partition Query (omitting `customerId`): Cosmos DB fans out across all physical partitions, costing **~25 to 150+ RUs**.
2. **Project Only Needed Attributes (`SELECT c.id, c.name` vs. `SELECT *`)**:
   * `SELECT *` retrieves full payload sizes, consuming more serialization time and bandwidth.
3. **Check `Index Hit Document Count` vs `Retrieved Document Count`**:
   * If `Retrieved Document Count` is 10,000 but `Output Document Count` is 2, the query is performing a full table scan. Add an index to reduce RU costs.
4. **Avoid High `OFFSET` Values**:
   * `OFFSET 10000 LIMIT 10` still requires the engine to evaluate and skip 10,000 records. For large dataset pagination, use **Continuation Tokens** instead.
