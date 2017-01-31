Latin Text Manipulation
-----------------------
The purpose of this project is to to extract, process, and manage a collection of latin texts
as well as provide translation services and visualize the data.

### Run Instructions
First run data_extraction.py to extract the latin textual data and populate a sqlite database
with the extracted data.

This should create the latin-texts folder as well as the latin_text.db sqlite database file.

Next, run latin_search.py to begin the program that searches, translates, and visualizes the data.
Further explanation of the options within this program are discussed below.

### Project Discussion / Explanation
##### Data Extraction
In order to extract the required data for the application, I just ran a bunch of wget
commands (using python code) that went to www.thelatinlibrary.com/mycollection and
downloaded all of the html files that I needed. This part was straight forward.

##### Database Population
I thought this part would be straight forward, but after diving in to the task it proved
to be the hardest part of the 4. Each collection had to be parsed separately due to the
differences in the html. One of major causes for errors was the fact that sometimes the html
files were incorrect (missing closing tags etc.) This caused even BeautifulSoup to struggle
because BeautifulSoup assumes the html is correct. Numerous edge cases had to be taken
into account in order to correctly parse these files. Once the files were parsed, populating
the database was straight forward. A table was made called "passages" in a sqlite3 database
and the data was simply inserted in there. After that, I created a virtual fts4 table that
contained the data from the regular table since we will be performing text based searches on
this data all the time.

##### Translation Services
To complete the translation services part, All that needed to be done was to write a python
function that accepted an english term (word or phrase) and execute an api call to the
mymemory.translated.net website. This returned a json object containing multiple translations.

After matches were grabbed from the json object, they were simply returned and used for searching
just like the latin searh.

##### Search Results and Visualization
I elected to user a command line user interface for this application. With more time I would
probably create a simple website or even a really cool website to search over all of the latin
textual data, but with the time I had, a robust terminal application did the trick. I created a
menu driven interface in the terminal that prompts the user for 5 options:

1. Search (latin) -         This option simply searches the database for passages that have matches with
					    	the given latin search term and displays the passage as well as the collection
					    	title, book, chapter, verse, and link.

2. Search (english) -   	This option does the same thing, but before searching the database it translates
							the english term into mutliple latin terms and searches for EACH latin translated
							term. It displays the the search results for EACH translated term to the user
							separated by a label showing the user what translation each section of results is
							displaying

3. Usage Chart (latin) -    This option prompts the user for a latin search term and executes a select count
							statement into the database to get the data required to display a bar chart showing
							the usage for each collection for that term. The chart's y axis is simply the number
							of occurences for that term and the x-axis is just each collection. If a collection
							does not ever use the given term, the bar is not plotted resulting in the remaining
							bars being larger to adjust to the chart

4. Usage Chart (english) -  This option does the exact same thing as option 3 but prompts the user for an
							english term. Instead of displaying separate bar charts for each possible translation,
							all translations are used and summed together. So if the user were to type in "death"
							as their translation, then the select statement would count all the occurences for
							"necro", "mors", and "morti" and sum them all up and then display the data in the
							chart.

5. Exit Program - 			This option simply exits the program gracefully.

If the user gives any option other than these options, they are informed that their selected option is invalid
and they can give a new option until they choose one of the options above.

### Parsing Notes
##### 1: Theodosius:
This collection was not too bad to parse but it is definitely
much more difficult to parse than many other collections.
Each book is laid out with chapters and verses. Each chapter has many verses
and each verses list the chapter as well as the verse at the top in the form
Book.Chapter.Verse (numbers). Some verses were just one paragraph while other
verses spanned multiple paragraphs.

##### 2-4: Silius, May, Lucan:
The collections that are organizes like a poem where each line is a verse
are the easiest to parse from my experience. I didn't have much trouble parsing
these collections, however sometimes random files would have html mistakes in them
which really throws things off. Even using beautiful soup, if certain tags don't have
closing tags, things get really weird. Edge cases must be coded in order to fix these
these problems. I believe I solved all edge cases with these collections and the
contents of the database seem to be correct.

##### 5: Virgil:
This collection was somewhat similar to the 3 collections above, however the html
files were messed up significantly more. All the files had missing closing tags.
Some files had new lines after each br tag, while others did not which made things
a little more difficult. Again all edge cases were solved in the code and the data
parsed and stored correctly

##### All Collections:
Overall, parsing was very tedious and annoying, but satsifying when completed. The
html that we are dealing with is very sloppy and messed up and is challenging to parse,
but this was sometimes fun to overcome. After I completed everything, I felt that
the parsing was definitely doable and my original complaints I had were largely futile.

### Testing Notes
I created two test functions in my tests.py.

The first test function tests that all the folders downloaded contains the correct
number of files. This ensures that the downloads went correctly barring some really
weird errors where files are downloaded but somehow the contents are corrupted.
This way is better because the sizes vary and the spreadsheet sizes are different than
the actual sizes so testing the number of files is sufficient.

The second test function tests that the database has the correct number of rows
after all the parsing and storing is done. It also confirms that each row has 9
columns which makes sure the schema is correct, and it also checks a random row's
contents to make sure the parsing went as expected.

Overall these tests could definitely be more conclusive.