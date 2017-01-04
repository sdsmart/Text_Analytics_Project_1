About This Repository
=====================
This project was assigned to me in my Text Analytics class at the University of Oklahoma.

The purpose of this project was to be able to extract, process, and manage latin text data
as well as provide translation services and visualize the data.

Part A: Data Extraction
-----------------------
Process Description:
In order to extract the required data for the application, I just ran a bunch of wget
commands (using python code) that went to www.thelatinlibrary.com/mycollection and
downloaded all of the html files that I needed. This part was very straight forward.

Replication Steps:
This can easily be replicated by simply running my data_extraction.py script from
the terminal. It should result in a directory titled www.thelatinlibrary.com/ to be
created in the same place that contains all of the relavent html documents that will
be processed in further parts.

Test Cases:
To test the data extraction, I made a test function in my tests.py that makes sure
the correct number of directories are downloaded after running the script and that the
correct number of files in each directory exist. This sufficiently tests this part.
To run this test, simply type py.test tests.py into the terminal and both
test functions that exist in the file will be run.

For more information on Part A, see the README contents that I submitted for phase 1 only
(Located at the bottom of this README.txt)

Part B: Database Population
---------------------------
Process Description:
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

Replication Steps:
This can easily be repicated by simply running my data_extraction.py script from
the terminal. It should result in a latin-text.db file being created with two tables
inside. A regular sqlite3 table called passages that holes all of the actual data parsed
from the html files, and a virtual fts4 table that holds the same data in order to
perform fast text searches.

Test Cases:
To test the database population worked correctly I wrote a test function in my tests.py
that makes sure there are the correct number of rows in the database table after population, that
each row has the correct number of columns, and that a few random rows have the desired contents.
This sufficiently tests this part. To run this test, simply type py.test tests.py into
the terminal and both test functions that exist in the file will be run.

For more information on Part B, see the README contents that I submitted for phase 1 only
(Located at the bottom of this README.txt)

Part C: Translation Services
----------------------------
Process Description:
To complete the translation services part, All that needed to be done was to write a python
function that accepted an english term (word or phrase) and execute an api call to the
mymemory.translated.net website. This returned a json object containing multiple translations.

	IMPORTANT DIFFERENCE: The project rubric mentions using the "best" translation which I could
	have done with ease. All that needed to be done was a quick check on the quality value of the
	different translation options returned by translated.net, however, this often produced results
	that were not good. I found it MUCH better to use all translations given and inform the user of
	the search results for each one. The search results are handed back in sections
	(described in Part D) labeled by their translation. This produced much better results because
	often times, the highest quality translation was not actually the translation used in the texts

After matches were grabbed from the json object, they were simply returned and used for searching
just like the latin searh.

Replication Steps:
This process can be seen clearly by running my latin_search.py (after data_extraction.py has been
executed) script and selecting option 2 from the menu. It will prompt you for an english word or
phrase, after that, it will execute the function described above and display search results to
the terminal.

Test Cases:
In a perfect world, I would have written a unit test for this function that tests every line
of code etc. But I simply tested this the old fashioned way by running it a bunch of times with
various data and made sure that it handed me back the expected result. When the given english term
cannot be translated, then no matches are found and the program gracefully lets the user know
that a tranlsation could not be found for their given term.

Part D: Search Results and Visualization
----------------------------------------
Process Description:
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

Replication Steps:
To replicate this simply run my latin_search.py script (after data_extraction.py has been executed) and
give options corresponding the those described above. Each option is described in detail above so simply
follow those guidelines. The options are also described in the terminal upon running of course.

	IMPORTANT NOTE: When the program is run when the terminal is in full screen on a mac, it shifts focus to the
	desktop instead of staying on the terminal. The program is still running though so you just have to go back
	to the terminal and everything will work fine from there. I am not sure why this focus shift is happening. It
	only happened after I implemented the usage charts using matplotlib.

Test Cases:
Nothing to really test here other than the usage charts. I displayed usage charts for various data to make sure
that they were being created correctly. For the most part they looked great, but sometimes when only a couple
matches are found, the visualized data looks bad. For example if only one collection uses the given term
only once, then it is just one big fat bar that goes from 0 to 1 (doesn't look very good)

Collections Chosen
------------------
Name			Size
1. Theodosius   3.6 MB<br/>
2. Silius		0.9 MB<br/>
3. May			0.212 MB<br/>
4. Lucan		0.640 MB<br/>
5. Virgil		4.3 MB<br/>

Total Size: 9.65 MB

Note:
I am taking the spreadsheet sizes as truth here, even though the actual sizes are
different. This was stated to be okay to do.

Parsing Notes
-------------
1. Theodosius:

This collection was not too bad to parse but it is definitely
much more difficult to parse than many other collections.
Each book is laid out with chapters and verses. Each chapter has many verses
and each verses list the chapter as well as the verse at the top in the form
Book.Chapter.Verse (numbers). Some verses were just one paragraph while other
verses spanned multiple paragraphs.

  2-4. Silius, May, Lucan:

The collections that are organizes like a poem where each line is a verse
are the easiest to parse from my experience. I didn't have much trouble parsing
these collections, however sometimes random files would have html mistakes in them
which really throws things off. Even using beautiful soup, if certain tags don't have
closing tags, things get really weird. Edge cases must be coded in order to fix these
these problems. I believe I solved all edge cases with these collections and the
contents of the database seem to be correct.

5. Virgil:

This collection was somewhat similar to the 3 collections above, however the html
files were messed up significantly more. All the files had missing closing tags.
Some files had new lines after each br tag, while others did not which made things
a little more difficult. Again all edge cases were solved in the code and the data
parsed and stored correctly

All Collections:

Overall, parsing was very tedious and annoying, but satsifying when completed. The
html that we are dealing with is very sloppy and messed up and is challenging to parse,
but this was sometimes fun to overcome. After I completed everything, I felt that
the parsing was definitely doable and my original complaints I had were largely futile.

Testing Notes
-------------
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

Overall these tests could definitely be more conclusive, but I talked with Dr. Grant
and he mentioned that our tests aren't meant to be like that of a software engineering
class, but mainly sanity tests. Tests that make sure things are behaving as expected.
I believe these tests do that.