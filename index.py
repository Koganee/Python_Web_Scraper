from tkinter import *
from tkinter import ttk
import subprocess
import sys
import os
import pymongo

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "stackoverflow"
MONGODB_COLLECTION = "questions"

def getWord():
    searchValue = inputWord.get()
    searchDatabase(searchValue)

def searchDatabase(searchValue):
    count = 0
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]

        # Query the database
        query = {"title": {"$regex": searchValue, "$options": "i"}}  # Using text index for searching
        results = collection.find(query)
        array = [results]
        lst = [1000000]
        # Print results
        for result in results:
            title = result.get("title", "")
            if searchValue.lower() in title.lower():
                if result not in lst:
                    print(result)
                lst[count] = result
            else:
                print("Hi") 
            count += 1       

    finally:
        # Close the connection
        # print("Total questions matching search: " + count)
        client.close()

root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Search Word Here:").grid(column=0, row=0)
#ttk.Button(frm, text="Search", command=run_scrapy).grid(column=2, row=0)

inputWord = ttk.Entry(frm)
inputWord.grid(column=1, row=0)

ttk.Button(frm, text="Get Value", command=getWord).grid(column=1, row=1)    
root.mainloop()

