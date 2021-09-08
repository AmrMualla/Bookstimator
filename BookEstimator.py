#Amr Mualla, RIT, SE.
#The code below uses the Google Books API to retrieve information on a book based on relevance to a user input for the title.
#Once the information is pulled from the Google API, it's displayed for the user. If a piece of information is not available, the program will output Unavailable.
#The program then uses the page count, basic math, values on recorded data for the average human's reading speed and the assumption that 
#the user will read one hour a day minimum, and compute how long it will take to finish the book, and lastly display that value to the reader.

import requests
import json
from flask import Flask, render_template, request, redirect, url_for


# API key
api_file = open("api-key.txt", "r")
api_key = api_file.read()

# Title input
title = input("Enter a book title:\n")
title = title.strip()

# Base url
url = "https://www.googleapis.com/books/v1/volumes?q="
urlapi = (url + title + "&key=" + api_key)

# Get response
r = requests.get(url + title)

# Pulling and skinning information, which begins in a large dictionary.
library = json.loads(r.content)
books = library["items"]

# Choosing the most relevant book and retrieving the title.
relevance = books[0]
bookinfo = relevance["volumeInfo"]
booktitle = bookinfo["title"]

# Converting the authors, from a given list to a string in order to concatenate for output.
# If there's multiple authors, they will be seperated by a comma when displayed.
author = bookinfo.get("authors")
if(author == None):
    authorstr = "Unavailable"
else:
    if len(author) > 0:
        authorstr = ', '.join(author)
    else:
        authorstr = ''.join(author)

# Retrieves the publishdate of the book.
publishdate = bookinfo["publishedDate"]

# Googlebooks API does not guarantee information on all book details. Some books may have them, others may not.
description = bookinfo.get("description")
if(description == None):
    description = "Unavailable"
averagerating = bookinfo.get("averageRating")
if(averagerating == None):
    averagerating = "Unavailable"
pageCount = bookinfo.get("pageCount")
if(pageCount == None):
    pageCount = "Unavailable"

# Converting integers to strings
rating = str(averagerating)
pages = str(pageCount)

# Information Output
print("The most relevant title is: " + booktitle + ".\n")
print("The author(s) of the book is: " + authorstr + ".\n")
print("The book was published in " + publishdate + ".\n")
print("Description: " + description + ".\n")
print("Rating: " + rating + ".\n")
print("Pages: " + pages + ".\n")

# 15 Pages/30 Min a day reading
if(pageCount == "Unavailable"):
    Fifteenpages = "pagecountmissing"

else:
    Halfhour = int(pageCount)/15
    Fifteenpages = round(Halfhour)


# 30 Pages/1 Hr a day reading
if(pageCount == "Unavailable"):
    Thirtypages = " "

else:
    Hour = int(pageCount)/30
    Thirtypages = round(Hour)


#Information for time output
if(Fifteenpages == "pagecountmissing"):
    print("Sorry, the pagecount for this book is unavailable, therefore calculation and estimation are also unavailable.")
else:
    print("It will take you approximately " + str(Fifteenpages) + " days consistently reading 15 pages/30 minutes per day to complete this book" + ".\n")
    print("It will take you approximately " + str(Thirtypages) + " days consistently reading 30 pages/1 hour per day to complete this book" + ".\n")
