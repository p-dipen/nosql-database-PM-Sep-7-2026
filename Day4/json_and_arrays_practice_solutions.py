# Python JSON & Arrays Practice Lab (Solutions)

# -------------------------------------------------------------
# Exercise 1: Create a Document (Dictionary)
# -------------------------------------------------------------
student = {
    "name": "Sarah",
    "age": 25,
    "course": "NoSQL"
}

print("Student:", student)


# -------------------------------------------------------------
# Exercise 2: Read Values from a Document
# -------------------------------------------------------------
employee = {
    "id": 101,
    "name": "John Doe",
    "department": "IT",
    "salary": 75000
}

emp_name = employee["name"]
emp_salary = employee["salary"]

print("Employee Name:", emp_name)
print("Employee Salary:", emp_salary)


# -------------------------------------------------------------
# Exercise 3: Update and Add New Fields
# -------------------------------------------------------------
car = {
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2020
}

car["year"] = 2024
car["color"] = "Blue"

print("Updated Car:", car)


# -------------------------------------------------------------
# Exercise 4: Nested Documents (Object inside Object)
# -------------------------------------------------------------
user = {
    "username": "alex99",
    "profile": {
        "city": "Toronto",
        "country": "Canada"
    }
}

print("City:", user["profile"]["city"])

user["profile"]["city"] = "Montreal"
print("Updated User:", user)


# -------------------------------------------------------------
# Exercise 5: JSON Arrays (Lists)
# -------------------------------------------------------------
skills = ["Python", "MongoDB", "CosmosDB", "SQL"]

print("First skill:", skills[0])
print("Second skill:", skills[1])


# -------------------------------------------------------------
# Exercise 6: Document with an Array
# -------------------------------------------------------------
product = {
    "id": "P100",
    "title": "Headphones",
    "price": 150,
    "tags": ["audio", "wireless", "electronics"]
}

print("Title:", product["title"])
print("First tag:", product["tags"][0])


# -------------------------------------------------------------
# Exercise 7: Array of Documents (Simulating Database Results)
# -------------------------------------------------------------
students = [
    {"name": "Alice", "score": 90},
    {"name": "Bob", "score": 85},
    {"name": "Charlie", "score": 95}
]

print("First student name:", students[0]["name"])
print("Third student score:", students[2]["score"])
