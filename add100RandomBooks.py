#!/usr/bin/env python3

import requests
import json
from faker import Faker


APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic", 
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            },
        data = json.dumps(book)
    )
    if r.status_code == 200:
        print(f"Book {book} added.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book {book}.")

# Get the Auth Token Key
apiKey = getAuthToken()

# Using the faker module, generate random "fake" books
fake = Faker()
for i in range(4,29 ):
    fakeTitle = fake.catch_phrase()
    fakeAuthor = fake.name()
    fakeISBN = fake.isbn13()
    book = {"id":i, "title": fakeTitle, "author": fakeAuthor, "isbn": fakeISBN}
    # add the new random "fake" book using the API
    addBook(book, apiKey) 
def getBooks(apiKey):
    r = requests.get(
        f"{APIHOST}/api/v1/books",
        headers = {"X-API-Key": apiKey}
    )
    if r.status_code == 200:
        return r.json()  # Assuming this returns a list of books (dicts)
    else:
        raise Exception(f"Error {r.status_code} while fetching books: {r.text}")

def deleteBook(bookId, apiKey):
    r = requests.delete(
        f"{APIHOST}/api/v1/books/{bookId}",
        headers = {"X-API-Key": apiKey}
    )
    if r.status_code == 200:
        print(f"Deleted book with ID {bookId}")
    else:
        raise Exception(f"Error {r.status_code} while deleting book {bookId}: {r.text}")
# Fetch all books
books = getBooks(apiKey)

# Check if there are at least 10 books to delete
if len(books) >= 10:
    first_five = books[:5]
    last_five = books[-5:]

    # Delete first five books
    for book in first_five:
        deleteBook(book['id'], apiKey)

    # Delete last five books
    for book in last_five:
        deleteBook(book['id'], apiKey)
else:
    print("Not enough books to delete first and last five.")
