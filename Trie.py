'''Trie data structure for a dictionary'''
'''@author: Alex Waweru'''

from functools import *

'''This is a trie Node implementation. The node's children are held in a list of size 27,
26 letters (a - z) and an apostrophe'''
class Node:
    
    def __init__(self):
        #Initialized to 27 for letters 'a' through 'z' and apostrophe
        self.children = [None]*27
        
        # isEndOfWord is True if node is the last character of the word
        self.isEndOfWord = False

        # Add list of the specific characters the node is pointing
        #self.nodes_pointing_to = []
        

'''This is a trie data structure implementation.'''
class Trie:

    '''This method initializes the Trie's root and builds a trie from the dictionary
    tet file'''
    def __init__(self):

        # Initialize the trie root as a node
        self.root = self.getNode()
        
        #Builds a trie using the english dictionary
        self.build_trie()


    '''This method creates and returns a new node'''
    def getNode(self):
        
        # Returns a new trie node
        return Node()


    '''This method gets the index of a particular character in the nodes' children list'''
    def _charToIndex(self,ch):
        # Converts key current character into index
        # use 'a' through 'z' and apostrophe
        index = abs(ord(ch)-ord('a'))
        
        # This condition caters for the apostrophe
        if index > 25:
            index = 26
        return index


    '''This method inserts a word into the trie'''
    def insert(self,key):
        # Caters for the two conditions:
        # 1. If key is not present, inserts key into trie
        # 2. If the key is prefix of trie node, mark the leaf node
        # 3. If key is an empty string, do nothing
        
        current_node = self.root
        
        for level in range(len(key)):
            index = self._charToIndex(key[level])
 
            # if current character is not present
            if not current_node.children[index]:
                current_node.children[index] = self.getNode()
            current_node = current_node.children[index]
 
        # mark last node as leaf
        current_node.isEndOfWord = True
        

    '''This methods searches for a word in the trie. If the word exists it
    returns True, else it returns False'''
    def search(self, key):
         
        # Search key in the trie
        # Returns true if key presents 
        # in trie, else false
        
        key = key.lower()
        current_node = self.root

        for level in range(len(key)):
            index = self._charToIndex(key[level])
            if not current_node.children[index]:
                return False
            current_node = current_node.children[index]
 
        return current_node != None and current_node.isEndOfWord


    ''' This methods checks if a particular node contains any child'''
    def _has_children(self, node):

        # Check if all the children nodes
        # If any of them does not contain None return True
        # else return False
        
        for i in range(len(node.children)):
            if node.children[i]!=None:
                return True
            else:
                return False


    '''This methods gets all complete words one letter away from the prefix'''
    def suggest_words(self, prefix):

        # Get all the children of the last letter of the prefix
        # If any of the letters is an end of word append it to results
        # return results
        
        alphabet = "abcdefghijklmnopqrstuvwxyz'"
        prefix = prefix.lower()
        results = []

        current_node = self.root
        for level in range(len(prefix)):
            index = index = self._charToIndex(prefix[level])
            if not current_node.children[index]:
                return False
            current_node = current_node.children[index]
            
        if current_node.isEndOfWord:
                results.append(prefix)
        for i in range(len(current_node.children)):
            if current_node.children[i]!=None and current_node.children[i].isEndOfWord:
                word = prefix
                word = word + alphabet[i]
                results.append(word)
        return results


    ''' This method builds a trie from a dictionary text file'''
    def build_trie(self):

        # Open the dictionary text file and read the words into a list
        # Insert each word in the list into the trie
        
        inputfile = open('english3.txt', 'r')
        keys = inputfile.readlines() 
        inputfile.close()
        for key in keys:
            self.insert(key[:-1])
 
 
