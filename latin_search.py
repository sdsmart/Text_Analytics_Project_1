#!/usr/bin/env python3

###########################
##   PROJECT 1 PHASE 2   ##
##  NAME: STEPHEN SMART  ##
###########################

# ---------------
# --- Imports ---
# ---------------
import sqlite3
import sys
import subprocess
import os
import re
import numpy as np
import matplotlib.pyplot as plt

# -----------------
# --- Functions ---
# -----------------
def get_selected_option():
	# Prompts the user to choose an option:
	# Searching the latin text based on a give latin or english word
	# or displaying a usage chart for the collections based on a latin
	# or english word.
	print('\n------------------------ Options ------------------------')
	print('1: SEARCH (latin)')
	print('   - Search the latin text for a latin word or phrase')
	print('2: SEARCH (english)')
	print('   - Search the latin text for an english word or phrase')
	print('     using translation services')
	print('3: USAGE CHART (latin)')
	print('   - Display a bar chart of the documents that use a')
	print('     given latin word or phrase')
	print('4: USAGE CHART (english)')
	print('   - Display a bar chart of the documents that use a')
	print('     given english word or phrase using trasnlation')
	print('     services')
	print('5: EXIT')
	print('---------------------------------------------------------')
	print('Enter a number corresponding to one of the above options')

	# Grabs the selected option from the user and returns it
	selected_option = input('> ')
	return selected_option

# --------------- End get_selected_option() ---------------

def search(search_term):
	# Connecting to the latin_text.db database in sqlite3
	db = sqlite3.connect('latin_text.db')
	db_cursor = db.cursor()

	# Grabbing all the matches for the given search term
	matches = db_cursor.execute("SELECT * FROM passages_fts WHERE passage MATCH '" + search_term + "'").fetchall()
	
	# Printing the matches' information to the user
	if len(matches) == 0:
		print('No Matches Found')
	else:
		for i, match in enumerate(matches):
			if match[0] != 'null':
				print('Title: ' + match[0])
			if match[1] != 'null':
				print('Book: ' + match[1])
			if match[3] != 'null':
				print('Author: ' + match[3])
			if match[4] != 'null':
				print('Dates: ' + match[4])
			if match[5] != 'null':
				print('Chapter: ' + match[5])
			if match[6] != 'null':
				print('Verse: ' + str(match[6]))
			if match[7] != 'null':
				print('Passage: ' + match[7])
			if match[8] != 'null':
				print('Link: ' + match[8])
			if i < len(matches) - 1:
				print('--------------------')

	# Closing the database connection
	db.close()

# --------------- End search(search_term) ---------------

def translate(english_search_term):
	# Executes the api call to mymemory.translated.net storing the json result in a temp file
	os.system("wget -q -O temp.json 'http://mymemory.translated.net/api/get?q=" + english_search_term + "&langpair=en|la'")
	# Grabbing the contents of the temp file
	cmd = ['cat', 'temp.json']
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
	# Cleaning up
	os.system('rm temp.json')

	# Getting all of the translations from the english word to latin and returning them
	search_terms = re.findall(re.compile(r'\"translation\":\"(\w+)\"'), output)
	return search_terms

# --------------- End translate(english_search_term) ---------------

def display_usage_chart(search_terms):
	# Connecting to the latin_text.db database in sqlite3
	db = sqlite3.connect('latin_text.db')
	db_cursor = db.cursor()

	# Building a select statement query based on the given search terms
	match_string = ''
	for i, st in enumerate(search_terms):
		match_string += st
		if i < len(search_terms) - 1:
			match_string += ' OR '
	select_statement = "SELECT title, COUNT(*) FROM passages_fts WHERE passage MATCH '" + match_string + "' GROUP BY title"
	# Grabbing all the counts (occurences of each term) for each collection
	data = db_cursor.execute(select_statement).fetchall()

	# If no occurences exist, letting the user know
	if len(data) == 0:
		print('\nNot Displaying Chart - No Matches Found')
		db.close()
		return

	# Closing the database connection
	db.close()

	# Setting up a couple lists for X and Y values to plot
	collections = []
	for i, c in enumerate(data):
		collections.append(data[i][0])
	values = []
	for i, v in enumerate(data):
		values.append(int(data[i][1]))

	# Getting the figure from matplotlib
	fig = plt.figure()

	# Setting up the bar chart
	width = .35
	ind = np.arange(len(data))
	plt.bar(ind, values, width=width, align='center')
	plt.xticks(ind + width / 2, collections, fontsize='8', ha='center', rotation='vertical')
	plt.xlabel('Collection Title')
	plt.ylabel('Number of Occurences')
	plt.title('Occurences Based On Collection')
	plt.gcf().tight_layout()

	# Displaying the chart
	print('\nDisplaying Chart... (Exit chart to continue with application)')
	plt.show()

# --------------- End display_usage_chart(search_terms) ---------------

# --------------
# --- Script ---
# --------------
if __name__ == '__main__':
	print('====== Latin Text Search / Visualtion Application ======')

	# Getting the selected option from the user
	selected_option = get_selected_option()

	# Starting the menu-based interface that loops until the user
	# chooses to exit the program
	while True:
		# Searching the database for a given latin search term
		if selected_option == '1':
			print('Enter the latin word or phrase')
			search_term = input('> ')
			print('\n==================== SEARCH RESULTS ====================\n')
			search(search_term)
			print('\n========================================================')

		# Searching the database for a given english search term
		elif selected_option == '2':
			print('Enter the english word or phrase')
			english_search_term = input('> ')
			search_terms = translate(english_search_term)
			print('\n==================== SEARCH RESULTS ====================\n')
			if len(search_terms) == 0:
				print('No Translation Found')
			else:
				# Since there are many translations, it is better to show results for
				# all translations to really get good information
				for i, st in enumerate(search_terms):
					if i > 0:
						print()
					print('--------------------------------------------------------')
					print('Using Translation: ' + english_search_term + ' --> ' + st)
					print('--------------------------------------------------------\n')
					search(st)
			print('\n========================================================')

		# Displaying usage chart for a given latin search term
		elif selected_option == '3':
			print('Enter the latin word or phrase')
			search_terms = []
			search_terms.append(input('> '))
			display_usage_chart(search_terms)

		# Displaying usage chart for a given english search term
		elif selected_option == '4':
			print('Enter the english word or phrase')
			english_search_term = input('> ')
			search_terms = translate(english_search_term)
			if len(search_terms) == 0:
				print('\nNo Translation Found')
			else:
				display_usage_chart(search_terms)

		# Exiting program
		elif selected_option == '5':
			print('Exiting Program')
			break

		# Letting the user know they gave an invalid choice
		else:
			print('Invalid Choice')

		# Prompting the user for another option after the previous selected option
		# has been completed.
		selected_option = get_selected_option()
