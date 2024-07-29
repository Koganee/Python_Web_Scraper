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
MONGODB_COLLECTION2 = "words"

def getWord():                                                          #Function for getting word
    searchValue = inputWord.get()
    searchDatabase(searchValue)
    findMostCommonWords(searchValue)

def searchDatabase(searchValue):                                        #Function for searching for specified word.
    count = 0
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]

        # Query the database
        query = {"title": {"$regex": searchValue, "$options": "i"}}     #Includes substrings.
        results = collection.find(query)
        lst = []

        # Print results
        for result in results:
            title = result.get("title", "")
            url = result.get("url", "")                                 #Get URL
            if searchValue.lower() in title.lower():                    #Check if searchValue is in title.
                if url not in lst:                                      #Only prints if url is not already in list.
                    print(result)
                lst.append(url)                                         #Add url to list.
            else:
                print("Hi")     

    finally:
        # Close the connection
        client.close()

def findMostCommonWords(searchValue):
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]
        #collection2 = db[MONGODB_COLLECTION2]

        db[MONGODB_COLLECTION2].drop()
        collection2 = db[MONGODB_COLLECTION2]

        word_counts = {}
        listWords = []

        # Query the database
        
        results = collection.find({})

        for result in results:
            title = result.get("title", "")
            words = title.split()
            for word in words:
                if word not in listWords:
                    listWords.append(word)
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1
        for word, count in word_counts.items():
            print(f"'{word}': {count}")
            stuffToAdd = {"word": word, "count": count}
            collection2.insert_one(stuffToAdd)
            #print(f"'{searchValue}': {count}")                 
    finally:
        #print(collection2.get("word", searchValue))
        # Close the connection
        client.close()

#UI---------------------------------------------------
root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Search Word Here:").grid(column=0, row=0)

inputWord = ttk.Entry(frm)                                              #Search Input Box.
inputWord.grid(column=1, row=0)

ttk.Button(frm, text="Get Value", command=getWord).grid(column=1, row=1)    
root.mainloop()
#UI---------------------------------------------------
