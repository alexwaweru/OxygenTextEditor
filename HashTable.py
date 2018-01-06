''' This Hashtable implemetation was adopted from the 'Problem Solving with Algorithmns and Data Structures'
    online textbook @https://interactivepython.org/runestone/static/pythonds/SortSearch/Hashing.html#implementing-the-map-abstract-data-type'''
''' The code was modified by Seyram Kartey'''
    
class HashTable:
    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.wordSlot = [None] * self.size

    def put(self,key,data):
      stringKey = ''
      if isinstance(key, str):
          stringKey = key
          key = self._convert_to_integer(key)

      hashvalue = self.hashfunction(key,len(self.slots))
          
      if self.slots[hashvalue] == None:
        self.slots[hashvalue] = key
        self.wordSlot[hashvalue] = stringKey
        self.data[hashvalue] = data
      else:
        if self.slots[hashvalue] == key and self.wordSlot[hashvalue] == stringKey:
          self.data[hashvalue] = data  #replace
        else:
          nextslot = self.rehash(hashvalue,len(self.slots))
          while self.slots[nextslot] != None and \
                          self.slots[nextslot] != key and \
                          self.wordSlot[nextslot] != stringKey:
            nextslot = self.rehash(nextslot,len(self.slots))

          if self.slots[nextslot] == None and self.wordSlot[nextslot] == None:
            self.slots[nextslot]=key
            self.wordSlot[nextslot] == stringKey
            self.data[nextslot]=data
          else:
            self.data[nextslot] = data #replace

    def hashfunction(self,key,size):
         return key%size

    def rehash(self,oldhash,size):
        return (oldhash+1)%size
    
    def _convert_to_integer(self, key):
        int_key = 0
        for i in range(len(key)):
            int_key = int_key + (ord(key[i])*(i+1)) 
        return int_key


    def get(self,key):
      if isinstance(key, str):
          key = self._convert_to_integer(key)
      startslot = self.hashfunction(key,len(self.slots))

    
      data = None
      stop = False
      found = False
      position = startslot
      while self.slots[position] != None and  \
                           not found and not stop:
         if self.slots[position] == key:
           found = True
           data = self.data[position]
         else:
           position=self.rehash(position,len(self.slots))
           if position == startslot:
               stop = True
      return data

    def __getitem__(self,key):
        return self.get(key)

    def __setitem__(self,key,data):
        self.put(key,data)
         
