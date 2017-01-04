#!/usr/bin/env python3

###########################
##   PROJECT 1 PHASE 1   ##
##  NAME: STEPHEN SMART  ##
###########################

# ---------------
# --- Imports ---
# ---------------
import os
from bs4 import BeautifulSoup
import sqlite3
import re
import codecs

# ------------------------
# --- Global Variables ---
# ------------------------
base_dir = 'www.thelatinlibrary.com/'
latin_texts = ['theodosius', 'silius', 'may', 'lucan', 'verg']
# List of passages (each passage is a list containing 9 elements)
# title, book, language, author, dates, chapter, verse, passage, link
passages = []

# -----------------
# --- Functions ---
# -----------------
def download_files():
    # Downloading all of the files from the latin library website if the files
    # have not already been downloaded
    if not os.path.exists(os.getcwd() + '/' + base_dir):
        for text in latin_texts:
            os.system('wget -r -l 1 '+ base_dir + text + '.html')

# --------------- End download_files() ---------------

def parse_files():
    # --- Theodosius Parsing ---

    # Creating a beautiful soup object to parse the html for the html file
    with codecs.open(base_dir + latin_texts[0] + '.html', encoding='utf-8', errors='replace') as f: 
        soup = BeautifulSoup(f, 'html.parser')

    # Collecting data from the html
    title = soup.find('p', class_='pagehead').text.strip()
    language = 'latin'
    author = 'null'
    dates = 'null'

    # Parsing the individual book files
    for file_name in os.listdir(base_dir + latin_texts[0]):
        with codecs.open(base_dir + latin_texts[0] + '/' + file_name, encoding='utf-8', errors='replace') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Collecting the book and link data
        book = soup.title.text.strip()
        link = base_dir + latin_texts[0] + '/' + file_name

        # Creating a list of all paragraphs using BeautifulSoup
        paragraphs = soup.find_all('p')[4:-2]

        # Initializing chapter, verse, and passage variables
        chapter = ''
        verse = ''
        passage = ''
        
        # Looping through each paragraph in the file and collecting the data for chapter
        # verse, and passage
        for i in range(0, len(paragraphs)):

            # Grabbing the text from within the <p> tag
            text = paragraphs[i].text.strip()

            # If the text is blank, then there is nothing to do this iteration
            if text == '':
                continue

            # Grabbing the verse number (if it exists) from the paragraph text
            pat = re.compile(r'CTh\.\d+\.\d+\.(\d+).*')
            match = pat.match(text)

            # If the verse exists and is equal to 0, then the text represents a new chapter.
            # If the verse exists but does not equal 0, then the text represents a new verse and passage
            # and is stored in the passages list.
            # If the verse does not exist then the text represents passage text and is appended to the
            # passage string for later storage
            if match:
                verse_candidate = match.group(1)
                if verse_candidate == '0':
                    chapter = text
                else:
                    if passage is not '':
                        passages.append([title, book, language,
                                         author, dates, chapter,
                                         verse, passage, link])
                        passage = ''

                    verse = verse_candidate
            else:
                passage += text

        # Appending the last passage that was in the file
        passages.append([title, book, language,
                         author, dates, chapter,
                         verse, passage, link])

    # --- End Theodosius Parsing ---

    # --- Silius Parsing ---

    # Creating a beautiful soup object to parse the html for the html file
    with codecs.open(base_dir + latin_texts[1] + '.html', encoding='utf-8', errors='replace') as f: 
        soup = BeautifulSoup(f, 'html.parser')

    # Collecting data from the html
    title = soup.h1.text.strip()
    language = 'latin'
    author = title
    dates = soup.h2.text.strip()

    # Parsing the individual book files
    for file_name in os.listdir(base_dir + latin_texts[1]):
        with codecs.open(base_dir + latin_texts[1] + '/' + file_name, encoding='utf-8', errors='replace') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Collecting the book, line, and chapter data
        book = soup.find('p', class_='pagehead').text.strip()
        link = base_dir + latin_texts[1] + '/' + file_name
        chapter = 'null'

        # Collecting verse, and passage data
        lines = soup.find_all('p')[2].text.strip().splitlines()
        verse = 1
        for passage in lines:
            if passage is not '' and (passage[-1].isdigit() or passage[-2].isdigit()):
                pattern = re.compile(r'(\D*)\d+.*')
                passage = pattern.match(passage).group(1).strip()

            if passage == '':
                continue

            passage = passage.strip()

            passages.append([title, book, language,
                             author, dates, chapter,
                             str(verse), passage, link])
            verse += 1

    # --- End Silius Parsing ---

    # --- May Parsing ---

    # Creating a beautiful soup object to parse the html for the html file
    with codecs.open(base_dir + latin_texts[2] + '.html', encoding='utf-8', errors='replace') as f: 
        soup = BeautifulSoup(f, 'html.parser')

    # Collecting data from the html
    pagehead = soup.find('p', class_='pagehead').text.strip().splitlines()
    title = pagehead[0]
    language = 'latin'
    author = title
    dates = pagehead[1]

    # Parsing the individual book files
    for file_name in os.listdir(base_dir + latin_texts[2]):
        if file_name == 'maytitle.shtml':
            continue

        with codecs.open(base_dir + latin_texts[2] + '/' + file_name, encoding='utf-8', errors='replace') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Collecting the book, line, and chapter data
        book = soup.find('p', class_='pagehead').text.strip()
        link = base_dir + latin_texts[2] + '/' + file_name
        chapter = 'null'

        # Collecting verse, and passage data
        lines = soup.find_all('p')[2].text.strip().splitlines()
        verse = 1
        for passage in lines:
            if passage is not '' and (passage[-1].isdigit() or passage[-2].isdigit()):
                pattern = re.compile(r'(\D*)\d+.*')
                passage = pattern.match(passage).group(1).strip()

            if passage == '':
                continue

            passage = passage.strip()

            passages.append([title, book, language,
                             author, dates, chapter,
                             str(verse), passage, link])
            verse += 1

    # --- End May Parsing ---

    # --- Lucan Parsing ---

    # Creating a beautiful soup object to parse the html for the html file
    with codecs.open(base_dir + latin_texts[3] + '.html', encoding='utf-8', errors='replace') as f: 
        soup = BeautifulSoup(f, 'html.parser')

    # Collecting data from the html
    title = soup.h1.text.strip()
    language = 'latin'
    author = title
    dates = soup.h2.text.strip()

    # Parsing the individual book files
    for file_name in os.listdir(base_dir + latin_texts[3]):
        with codecs.open(base_dir + latin_texts[3] + '/' + file_name, encoding='utf-8', errors='replace') as f:
            soup = BeautifulSoup(re.sub(r'<br>\S', '<br>\n', f.read()), 'html.parser')

        # Collecting the book, line, and chapter data
        book = soup.find('p', class_='pagehead').text.strip()
        link = base_dir + latin_texts[3] + '/' + file_name
        chapter = 'null'

        # Collecting verse, and passage data
        lines = soup.find_all('p')[2].text.strip().splitlines()
        verse = 1
        for passage in lines:
            if passage is not '' and (passage[-1].isdigit() or passage[-2].isdigit()):
                pattern = re.compile(r'(\D*)\d+.*')
                passage = pattern.match(passage).group(1).strip()

            if passage == '':
                continue

            passage = passage.strip()

            passages.append([title, book, language,
                             author, dates, chapter,
                             str(verse), passage, link])
            verse += 1

    # --- End Lucan Parsing ---

    # --- Virgil Parsing ---

    # Creating a beautiful soup object to parse the html for the html file
    with codecs.open(base_dir + latin_texts[4] + '.html', encoding='utf-8', errors='replace') as f: 
        soup = BeautifulSoup(f, 'html.parser')

    # Collecting data from the html
    title = soup.h1.text.strip()
    language = 'latin'
    author = title
    dates = soup.h2.text.strip()

    # Parsing the individual book files
    folder_name = 'vergil'

    for file_name in os.listdir(base_dir + folder_name):
        with codecs.open(base_dir + folder_name + '/' + file_name, encoding='utf-8', errors='replace') as f:
            soup = BeautifulSoup(re.sub(r'<br>\S', '<br>\n', f.read(), flags=re.I), 'html.parser')

        # Collecting the book, line, and chapter data
        book = soup.find('p', class_='pagehead')
        if book == None:
            book = soup.h1.text.strip()
        else:
            book = book.text.strip()
        link = base_dir + folder_name + '/' + file_name
        chapter = 'null'

        # Collecting verse, and passage data
        lines = soup.text.strip().splitlines()[0:-3]
        verse = 1

        for passage in lines:
            if re.match(r'^\s+', passage):
                continue

            passage = passage.strip()

            if passage is not '' and not passage.startswith('P. VERGILI'):
                if passage[-1].isdigit() or passage[-2].isdigit():
                    pattern = re.compile(r'(\D*)\d+.*')
                    passage = pattern.match(passage).group(1).strip()

                passages.append([title, book, language,
                                 author, dates, chapter,
                                 str(verse), passage, link])
                verse += 1

    # --- End Virgil Parsing ---

# --------------- End parse_files() ---------------

def store_data(db_name):
    # Creating / connecting to latin-text.db
    db = sqlite3.connect(db_name)

    # Creating db cursor in order to execute sql statements
    db_cursor = db.cursor()

    # Creating table to hold latin text passages
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS passages (
                        title text,
                        book text,
                        language text,
                        author text,
                        dates text,
                        chapter text,
                        verse integer,
                        passage text,
                        link text
                      );''')

    # Storing passages into the database
    for psg in passages:
        db_cursor.execute('INSERT INTO passages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', psg)

    # Creating an fts4 table for the data since we are going to be performing
    # text searches over this data many times
    db_cursor.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS passages_fts 
    						USING fts4(title, book, language, 
    								   author, dates, chapter,
    								   verse, passage, link)''')

    # Populating the fts table with all of the passage data
    db_cursor.execute('INSERT INTO passages_fts SELECT * FROM passages')

    # Saving db actions
    db.commit()

    # Closing db connection
    db.close()

# --------------- End store_data(passages, db_name) ---------------

# --------------
# --- Script ---
# --------------
if __name__ == '__main__':

	# Downloading the html files containing the latin text data
    download_files()

    # Parsing the files into a list of passages
    parse_files()        

    # Storing the list of passages (created above) into the database
    store_data('latin-text.db')

# --------------- End Script ---------------