
'''@authors: Alex Waweru, Ekiyor Odoko, Seyram Kartey'''

import tkinter
from tkinter import *
from tkinter import ttk, Text, filedialog
from collections import Counter
from Trie import *
from Spell import *
 
class Editor(ttk.Frame):
    '''Initializes the text area, and binds events to it'''    
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        #Initialize the Trie (dictionary)
        self.dictionary = Trie()
        
        #initialize text widget
        self.text = Text(self.root, width=100, height=40)
        self.text.grid(column=0, row=2)

        #Initialize the menu
        self.init_gui()

        #Bind space and right-click events on the text widget
        self.text.bind("<space>", self.spell_check)
        self.text.bind('<Button-3>', self.autocorrect)
        self.text.bind('<Key>', self.typing_suggestions)

        #Initize the filename to empty string
        self.filename = ''

        #Initialize the underline tag for mispelt words
        self.text.tag_configure('underline', foreground='red', underline = True)

        #Initialize the highligh tag for found words
        self.text.tag_configure('highlight', background='red')
        self.text.tag_configure('unhighlight', background='white')

        #Initialize pop-up menu for right click
        self.pop_menu = tkinter.Menu(parent, tearoff=0)

        #Initialize pop-up menu for text statistics
        self.pop_stats = tkinter.Menu(parent, tearoff=0)

    '''Exits program.'''
    def on_quit(self):
        self.save()
        quit()

    '''Saves an unsaved file'''
    def save_as(self):
        t = self.text.get("1.0", "end-1c")
        self.filename =filedialog.asksaveasfilename()
        file1=open(self.filename, "w+")
        file1.write(t)
        file1.close()

    '''opens a file'''
    def open_file(self):
        self.filename = filedialog.askopenfilename(parent=root)
        f = open(self.filename, 'r')
        self.text.insert(1.0, f.read())
        f.close()

    '''saves an initially saved file'''
    def save(self):
        if self.filename == '':
            self.save_as()
        else:
            f = open(self.filename, 'w')
            f.write(self.text.get('1.0', 'end'))
            f.close()
            tkinter.messagebox.showinfo('FYI', 'File Saved.')

    '''Changes the text font to Helvetica'''       
    def FontHelvetica(self):
        self.text.config(font="Helvetica")

    '''Changes the text font to Courier'''
    def FontCourier(self):
        self.text.config(font="Courier")

    '''Creates a new file'''
    def new(self):
        root = tkinter.Tk()
        Editor(root)
        root.mainloop()

    '''Spellcheck the word preceeding the insertion point (after clicking spacebar)'''
    def spell_check(self, event):
        index = self.text.search(r'\s', "insert", backwards=True, regexp=True)
        if index == "":
            index ="1.0"
        else:
            index = self.text.index("%s+1c" % index)
            word = self.text.get(index, "insert")
        if not self.dictionary.search(word):
            self.text.tag_add('underline', index, "%s+%dc" % (index, len(word)))
        else:
            self.text.tag_remove('underline', index, "%s+%dc" % (index, len(word)))

    '''Provide suggestions when a incorrect word is right clicked'''
    def autocorrect(self, event):
        suggestion = ''
        # get the index of the mouse click
        index = self.text.index("@%s,%s" % (event.x, event.y))
        
        # get the indices of all "underline" tags
        tag_indices = list(self.text.tag_ranges('underline'))

        # iterate them pairwise (start and end index)
        for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
            # check if the tag matches the mouse click index
            if self.text.compare(start, '<=', index) and self.text.compare(index, '<', end):
                # return string between tag start and end
                word = self.text.get(start, end)
                suggestion = correction(word)

        def replace(suggestion):
            self.text.delete(start, end)
            self.text.insert(start, suggestion)
                
        if suggestion!='':
            self.pop_menu.delete(0)
            self.pop_menu.add_command(label=suggestion, command=replace(suggestion))
            self.pop_menu.post(event.x_root, event.y_root)            
        else:
            pass

    ''' This method checks if the string before the insertion point is a valid english word.
        If the string is not a valid english word, it is underlined red.'''
    def typing_suggestions(self, event):
        index = self.text.search(r'\s', "insert", backwards=True, regexp=True)
        if index == "":
            index ="1.0"
        else:
            index = self.text.index("%s+1c" % index)
            word = self.text.get(index, "insert")
            self.suggestions.set(self.dictionary.suggest_words(word))
            self.text.tag_remove('highlight', '1.0', 'end')


    ''' This method highlights the occurences of a string in the text area'''
    def find(self):
        key = self.find_bar.get()
        document = self.text.get('1.0', 'end')
        word_length = len(key)

        start_indices = []
        stop_indices = []
        start_pos = []
        stop_pos = []
        
        start_index = document.find(key)
        while start_index!=-1:
            start_indices.append(start_index)
            
            stop_index = start_index + word_length
            stop_indices.append(stop_index)
            
            start_index = document.find(key, stop_index, len(document))

            
        for i in range(len(start_indices)):
            start_row = start_indices[i]//99 + 1
            stop_row = stop_indices[i]//99 + 1
            start_col = start_indices[i]%100
            stop_col = stop_indices[i]%100
            start_index = str(start_row)+'.'+str(start_col)
            stop_index = str(stop_row)+'.'+str(stop_col)
            start_pos.append(start_index)
            stop_pos.append(stop_index)
            
        for l in range(len(start_indices)):
            start = start_pos[l]
            stop =  stop_pos[l]
            self.text.tag_add('highlight', start, stop)

            

    '''Pop out the statistics of the document'''
    def statistics(self):
        document = self.text.get("1.0", "end-1c")
        list_of_words = document.split()

        most_common = Counter(list_of_words).most_common(1)
        most_common = most_common[0]
        word = most_common[0]
        count = most_common[1]
                
        total_words = 'Total words: ' + str(len(list_of_words))
        most_popular_word = 'Most common word: ' + str(word)+' : '+str(count)
        

        if document!='':
            self.pop_stats.delete(0)
            self.pop_stats.delete(1)
            
            self.pop_stats.add_command(label=total_words, command='')
            self.pop_stats.add_command(label=most_popular_word, command='')
            self.pop_stats.post(500, 80)            
        else:
            pass
        

    """Builds Menu of the user interface"""
    def init_gui(self):
        self.root.title('Oxygen Text Editor')
        self.root.option_add('*tearOff', 'FALSE')
 
        self.grid(column=0, row=0, sticky='nsew')
 
        self.menubar = tkinter.Menu(self.root)
 
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='New', command=self.new)
        self.menu_file.add_command(label='Open', command=self.open_file)
        self.menu_file.add_command(label='Save As', command=self.save_as)
        self.menu_file.add_command(label='Save', command=self.save)
        self.menu_file.add_command(label='Quit', command=self.on_quit)

        self.menu_font = tkinter.Menu(self.menubar)
        self.menu_font.add_command(label='Helvetica', command=self.FontHelvetica)
        self.menu_font.add_command(label='Courier', command=self.FontCourier)

        self.menu_tools = tkinter.Menu(self.menubar)
        self.menu_tools.add_command(label='Find and Replace', command=self.find)
        self.menu_tools.add_command(label='Document statistics', command=self.statistics)

        self.menu_help = tkinter.Menu(self.menubar)
        self.menu_help.add_command(label='About', command=self.on_quit)
 
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_font, label='Fonts')
        self.menubar.add_cascade(menu=self.menu_tools, label='Tools')
        self.menubar.add_cascade(menu=self.menu_help, label='Help')
 
        self.root.config(menu=self.menubar)

        self.suggestions = StringVar()
        ttk.Label(self, text="  Suggestions", width = 12).grid(column=0, row=1,sticky='w')
        self.suggestion_bar = ttk.Entry(self, textvariable=self.suggestions, width= 48)
        self.suggestion_bar.grid(column=1, row = 1)
        ttk.Label(self, text="  Find", width = 8).grid(column=2, row=1,sticky='w')
        self.find_bar = ttk.Entry(self, width=20)
        self.find_bar.grid(column=3, row = 1)

 
if __name__ == '__main__':
    root = tkinter.Tk()
    Editor(root)
    root.mainloop()
