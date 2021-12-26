# -----------------------------------------------------------
# This file contains the functions to clean data scraped
#
# 2021, Mirko Tritella, Aurora Cerabolini, Corinna Strada
# email m.tritella@campus.unimib.it
# -----------------------------------------------------------
import re

def digitsInLine(charList:list) -> int:
    """
    Return the number of digits in a list.

    :param charList: List of characters.
    :type charList: list
    :return: Number of digits in the list.
    :rtype: int

    """
    value = 0
    for char in charList:
        if char.isdigit():
            value += 1
    return value


def getEvaluations(line:str) -> list:
    """
    Get the list of different valutations of the anime from review csv in order Overall, Story, Animation, Sound, Charachter, Enjoyment.

    :param line: Line of the csv file.
    :type line: str
    :return: List of valutations.
    :rtype: list

    """
    line = line.split("|")[2]
    charList = list(line[:81])
    
    line = line[:69 + int(digitsInLine(charList))].split()
    return(line[1::2])


def cleanReviews() -> None:
    """
    Open the csv file and foreach line modify it to have Overall, Story, Animation, Sound, Charachter, Enjoyment columns and rewrite it in another csv file. named cleanedReviews.csv.

    :return: None.

    """
    with open("../data/scraping/reviews.csv", "r") as f:
        for line in f:
            row = line.split("|")
            with open("../data/scraping/cleanedReviews.csv", "a") as file:
                stringToAppend = evaluationsListtoString(getEvaluations(line))
                
                text = improveReviewText(row[2])
                file.write(str(row[0] + '|' + stringToAppend + text))


def improveReviewText(review:str) -> str:
    """
    Improve the text of the review removing extra spaces.

    :param review: Text of the review.
    :type review: str
    :return: New text of the review.
    :return: str

    """
    text = review[69 + int(digitsInLine(list(review[:81]))):]
    text = re.sub(' +', ' ', text).replace('Helpful read more ', '')

    return text


def evaluationsListtoString(list:list) -> str:
    """
    Convert a list of valutations to a string with the valutations separated by a pipe to insert them in csv file.

    :param list: List of valutations.
    :type list: list
    :return: String with the valutations separated by a pipe.
    :return: str

    """
    stringToAppend = ''
    for value in list:
        stringToAppend = stringToAppend + value + "|"
    
    return stringToAppend



if __name__ == "__main__":
    cleanReviews()