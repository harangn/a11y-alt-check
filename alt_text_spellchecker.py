#!/usr/bin/python

# Imports
import sys
import argparse
from spellchecker import SpellChecker
from bs4 import BeautifulSoup
import urllib
import re

# Global variables
spell = SpellChecker(distance=1)
special_known_words = ['github', 'bellingham']
spell.word_frequency.load_words(special_known_words)

# Function declarations

# Check text for suspected typos; if typos are found, return list of them
def check_text(string):
    # Regular expression to remove all punctuation except for apostrophes and dashes
    arr = re.sub("[^\w\d'\-\s]+",'',string).split()
    # Check for misspellings
    misspelled = list(spell.unknown(arr))
    # If we have at least 1 misspelled word, format string to return list of typos
    write = ""
    if len(misspelled) > 0:
        for i in range(0,len(misspelled)):
            write += "\"" + str(misspelled[i]) + "\""
            if i+1 < len(misspelled):
                write += ", "
        return write + " (" + str(len(misspelled)) + " total): \"" + string + "\""

# Generate file with list of alt text of suspected typos for each link
def generate_list(file_name, links, ignore_empty):
    # Open the file
    f = open(file_name, "w")
    for link in links:
        # Try to load the page
        try:
            page = urllib.request.urlopen(link)
        except Exception as e:
            print("Error occurred. Page could not be found at " + link)
            f.write("Error occurred. Page could not be found at " + link)
            continue
        # Get the page and write the title and link to the file
        soup = BeautifulSoup(page, features="lxml")
        f.write(soup.find('title').getText() + " " + link + "\n")
        # For each img element, get the src and alt attributes
        for img in soup.findAll('img'):
            src = img.get('src')
            alt = img.get('alt')
            # If there is alt text, check for typos and potentially write to file
            if alt:
                result = check_text(alt)
                if result and len(result) > 0:
                    f.write("\t" + result + "\n")
                # If there is empty alt text, note this issue in the file
                elif ignore_empty:
                    f.write("\t" + "Empty alt text! Image source link: " + src + "\n")
    f.close()

# Main body
if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Find suspected typos in alt text.')
    parser.add_argument('file_name', type=str, nargs=1,
                        help='file to store output in')
    parser.add_argument('links', type=str, nargs='+',
                        help='links to check alt text on')
    parser.add_argument('--ignore_empty', dest='ignore_empty', action='store_const',
                        const=0, default=1,
                        help='ignore empty alt text; do not record it in output file')
    args = parser.parse_args()

    # Generate list
    generate_list(args.file_name[0], args.links, bool(args.ignore_empty))