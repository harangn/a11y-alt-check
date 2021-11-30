#!/usr/bin/python
"""
Given an output file name and a list of links, check image alt text for potential typos.
"""

# Imports
import sys
import argparse
from spellchecker import SpellChecker
from bs4 import BeautifulSoup
import urllib
import re

# Global variables
spell = SpellChecker(distance=1)

# Function declarations
def check_text(text : str) -> str:
    """Check text for suspected typos; if typos are found, return string listing them.
    @param str text: Text to check for typos
    @return: List of typos and text, or empty string"""
    # Regular expression to remove all punctuation except for apostrophes and dashes
    arr = re.sub("[^\w\d'\-\s]+",'',text).split()
    # Check for misspellings
    misspelled = list(spell.unknown(arr))
    # If we have at least 1 misspelled word, format text list of typos
    ret = ""
    if len(misspelled) > 0:
        for i in range(0,len(misspelled)):
            ret += "\"" + str(misspelled[i]) + "\""
            if i+1 < len(misspelled):
                ret += ", "
        ret += " (" + str(len(misspelled)) + " total): \"" + text + "\""
    return ret

def generate_list(file_name : str, links : list, ignore_empty : bool):
    """Generate file with each link and their potential alt text typos.
    @param str file_name: Name of output file.
    @param list links: List of links to check.
    @param bool ignore_empty: Flag to ignore empty alt text."""
    # Open the file
    with open(file_name, 'w') as file:
        for link in links:
            # Try to load the page
            try:
                page = urllib.request.urlopen(link)
            except Exception as e:
                print("Error occurred. Page could not be found at " + link)
                file.write("Error occurred. Page could not be found at " + link)
                continue
            # Get the page and write the title and link to the file
            soup = BeautifulSoup(page, features="lxml")
            file.write(soup.find('title').getText() + " " + link + "\n")
            # For each img element, get the src and alt attributes
            for img in soup.findAll('img'):
                src = img.get('src')
                alt = img.get('alt')
                # If there is alt text, check for typos and potentially write to file
                if alt:
                    result = check_text(alt)
                    if len(result) > 0:
                        file.write("\t" + result + "\n")
                    # If there is empty alt text, note this issue in the file
                    elif not ignore_empty:
                        file.write("\t" + "Empty alt text! Image source link: " + src + "\n")

def argparsing():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find suspected typos in alt text.')
    parser.add_argument('links', type=str, nargs='+',
                        help='links to check alt text on')
    parser.add_argument('--ignore_empty', dest='ignore_empty', action='store_const',
                        const=1, default=0,
                        help='ignore empty alt text; do not record it in output file')
    parser.add_argument("--output", type=str, default="output.txt",
                        help="file to store output in; default output.txt")
    parser.add_argument("--dict", type=str, default=None,
                        help="dictionary file of typos to ignore")
    return parser.parse_args()

def add_known_words(file_name : str):
    """Add known words to spell checker
    @param str file_name: Name of dict file of special known words. File should have 1 word per line."""
    with open(file_name, 'r') as file:
        spell.word_frequency.load_words(file.read().splitlines())

def main(argv):
    """Parse args and generate output file."""
    args = argparsing()
    add_known_words(args.dict)
    generate_list(args.output, args.links, bool(args.ignore_empty))

if __name__ == '__main__':
    main(sys.argv)