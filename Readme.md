# CLI Tool for Scanning Browser Extensions
This CLI tool is designed to process Excel files, specifically focusing on Google Chrome and Mozilla Firefox Extensions IDs. It fetches permissions and other details from the Crxcavator API and writes the processed data to Excel files.

Credit for the API and platform belongs to CRXcavator by DUO Security (https://crxcavator.io/). I have just made a script automating stuff around their API

## Installation

1. Clone the repository:
   Clone the repository using '''git clone https://github.com/Ephemaral/Extension_Scanner/tree/master.git'''

2. Arguments needed for this are '''python3 scanner.py <file_name.xlsx>'''
   There is a test file in the repo, if you want to test the scanner just run '''python3 scanner.py test.xlsx'''

## Prerequisites

1. Make sure you have an excel file prepared with extensions IDs in it and nothing else. It could be either in a single cell seperated by commas or multiple cells just make sure there is nothing else other than extension IDs in that excel sheet.
2. If you only want to scan a single extension ID just head to https://crxcavator.io/ they have support for Google Chrome, Firefox AND Opera as well.


