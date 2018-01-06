'''@author: Seyram Kartey'''
'''Reviewed and commented by Alex Waweru'''

'''This program was written to be incorporated into the text editor but eventually
    it was not because of its huge runtime. It was supposed to calculate the text statistics
    of the strings in the text area, or an opened document. It was to find out the most common
    word, the total number of words, and whether a word was i the document or not.
    In its place a the team used a generic counter data structure from python for the above
    functionalities'''

from HashTable import *
wordTable = HashTable()

''' This method adds a new word into the hash table and increases it counter'''
def addWord(word):
    #Inserting a word into a hashtable when entered
    count = wordTable.get(word)
    if count == None:
        wordTable.put(word,1)
    else:
        count += 1
        wordTable.put(word,count)

''' This method returns the total number of words in the hashtable'''
def countWord(words):
    listOfWords = words.split(" ")
    return len(listOfWords)

''' This method returns whether a word is in the hashtable; or not'''
def findWord(word):
    if wordTable.get(word) == None:
        print("No matching result")
    else:
        print(wordTable.get(word),"results")

''' This method returns the most common word on the hashtable'''
def mostPopular():
    maximum = 0
    max_ind = 0
    for i in range(wordTable.size):
        if wordTable.data[i]!= None and wordTable.data[i] > maximum:
            maximum = wordTable.data[i]
            max_ind = i
   

    


