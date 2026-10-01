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

# 1. Print the user's city
# 2. Change city to "Montreal"

# Write your code here:
print(user["profile"]["city"])
user["profile"]["city"] = "Montreal"


print("Updated User:", user)
