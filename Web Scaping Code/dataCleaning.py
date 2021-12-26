# -----------------------------------------------------------
# This file contains the functions to clean data scraped
#
# 2021, Mirko Tritella, Aurora Cerabolini, Corinna Strada
# email m.tritella@campus.unimib.it
# -----------------------------------------------------------
import re

# Return the number of digits in a string
def digitsInLine(charList):
    value = 0
    for char in charList:
        if char.isdigit():
            value += 1
    return value

# Get the list of different valutations of the anime from review csv
def getEvaluations(line):
    line = line.split("|")[2]
    charList = list(line[:81])
    
    line = line[:69 + int(digitsInLine(charList))].split()
    # Return a list of values that are the valutations of Overall, Story, Animation, Sound, Charachter, Enjoyment
    return(line[1::2])


# Open the csv file and foreach line modify it to have Overall, Story, Animation, Sound, Charachter, Enjoyment columns
def cleanReviews():
    with open("../data/scraping/reviews.csv", "r") as f:
        for line in f:
            row = line.split("|")
            with open("../data/scraping/cleanedReviews.csv", "a") as file:
                stringToAppend = evaluationsListtoString(getEvaluations(line))
                
                text = improveReviewText(row[2])
                file.write(str(row[0] + '|' + stringToAppend + text))

# Improve the text of the review
def improveReviewText(review):
    text = review[69 + int(digitsInLine(list(review[:81]))):]
    text = re.sub(' +', ' ', text).replace('Helpful read more ', '')

    return text

# Convert a list of valutations to a string
def evaluationsListtoString(list):
    stringToAppend = ''
    for value in list:
        stringToAppend = stringToAppend + value + "|"
    
    return stringToAppend



if __name__ == "__main__":
    cleanReviews()