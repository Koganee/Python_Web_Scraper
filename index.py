from tkinter import *
from tkinter import ttk
from tkinter import Tk
import subprocess
import sys
import os


#def retrieve_input():
#    value = str(inputWord.get())
#    print("Input value:", value)
#    run_scrapy()

def run_scrapy():
    try:
        os.chdir('C:\\Users\\Aaron\\Web_Scraper\\stack') 
        # Run the Scrapy crawl command
        result = subprocess.run(
            ["scrapy", "crawl", "stack", "-a", f"value={inputWord.get()}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Print standard output and error
        #print("Scrapy command executed successfully.")
        #print("Standard Output:\n", result.stdout)
        #print("Standard Error:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        #print("Standard Output:\n", e.stdout)
        print("Standard Error:\n", e.stderr)

root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text="Search Word Here:").grid(column=0, row=0)
#ttk.Button(frm, text="Search", command=run_scrapy).grid(column=2, row=0)

inputWord = ttk.Entry(frm)
inputWord.grid(column=1, row=0)

value = str(inputWord.get())

ttk.Button(frm, text="Get Value", command=run_scrapy).grid(column=1, row=1)    
root.mainloop()




