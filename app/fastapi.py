from fastapi import FastApi
from fastapi import JSONResponse
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# Create an instance of the User model
user_data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
user = User(**user_data)

print(user)
print(user.name)