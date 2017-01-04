##########################
##  PROJECT 1 PHASE 1   ##
##     UNIT TESTS       ##
##########################

# ---------------
# --- Imports ---
# ---------------
import pytest
import sqlite3
import os
import data_extraction

# ----------------------
# --- Test Functions ---
# ----------------------
def test_download_files():
	data_extraction.download_files();

	base_dir = 'www.thelatinlibrary.com/'

	# Getting the number of files in each folder of interest
	num_files_in_main_folder = len(os.listdir(base_dir))
	num_files_in_theodosius = len(os.listdir(base_dir + 'theodosius'))
	num_files_in_silius = len(os.listdir(base_dir + 'silius'))
	num_files_in_may = len(os.listdir(base_dir + 'may'))
	num_files_in_lucan = len(os.listdir(base_dir + 'lucan'))
	num_files_in_virgil = len(os.listdir(base_dir + 'vergil'))

	# Checking to make sure the correct number of files were downloaded
	assert num_files_in_main_folder == 17
	assert num_files_in_theodosius == 16
	assert num_files_in_silius == 17
	assert num_files_in_may == 8
	assert num_files_in_lucan == 10
	assert num_files_in_virgil == 26

def test_parse_and_store_data():
	data_extraction.parse_files()
	data_extraction.store_data('test.db')

	db = sqlite3.connect('test.db')
	db_cursor = db.cursor()

	# Getting the number of total rows in the passages table
	num_rows_in_database = db_cursor.execute('SELECT count(passage) FROM passages').fetchall()[0][0]

	# Getting the number of columns in each row
	num_columns = len(db_cursor.execute('SELECT * FROM passages LIMIT 1').fetchall()[0])

	# Doing a random check on some of the contents to see if the parsing went as expected
	verse_check = db_cursor.execute('''SELECT verse FROM passages
										WHERE book=\'P. VERGILI MARONIS AENEIDOS LIBER TERTIVS\'
										AND passage=\'incerti quo fata ferant, ubi sistere detur,\'''').fetchall()[0][0]

	# Removing the test database
	os.system('rm test.db')

	# Checking to see if the parsing and storage worked correctly
	assert num_rows_in_database == 37252
	assert num_columns == 9
	assert verse_check == 7

