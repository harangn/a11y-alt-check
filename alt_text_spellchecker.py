#!/usr/bin/python
"""
Given an output file name and a list of links, check image alt text for potential typos.
"""

# Imports
import sys
import argparse
from spellchecker import SpellChecker
from bs4 import BeautifulSoup
import urllib.request
import re
import os

# Global variables
spell = SpellChecker(distance=1)

# Function declarations
def add_title(file: '_io.TextIOWrapper', ext: str, title: str, link: str) -> None:
    """Add title and link of URL to the document. Formatting differs depending on file type.
    @param File file: File to add to.
    @param str ext: File extension (.txt, .html, .htm).
    @param str title: URL title.
    @param str link: URL link.
    @return: Nothing."""
    title_text = title + " " + link
    if (ext == ".html" or ext == ".htm"):
        title_text = "<h1>" + title_text + "</h1>"
    title_text += "\n"
    file.write(title_text)

def check_text(text : str) -> str:
    """Check text for potential typos; if typos are found, return string listing them.
    @param str text: Text to check for typos.
    @return: List of typos and text, or empty string."""
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

def generate_list(file_name : str, ext: str, links : list, ignore_empty : bool):
    """Generate file with each link and their potential alt text typos.
    @param str file_name: Name of output file.
    @param str ext: File extension.
    @param list links: List of links to check.
    @param bool ignore_empty: Flag to ignore empty alt text."""
    # Open the file
    with open(file_name, 'w') as file:
        for link in links:
            # Try to load the page
            try:
                page = urllib.request.urlopen(link)
            except Exception as e:
                print("Error occurred. Page could not be found at " + link + "\n" + e + "\n")
                file.write("Error occurred. Page could not be found at " + link + "\n" + e + "\n")
                continue
            # Get the page and write the title and link to the file
            soup = BeautifulSoup(page, features="lxml")
            add_title(file, ext, soup.find('title').getText(), link)
            # For each img element, get the src and alt attributes
            for img in soup.findAll('img'):
                src = img.get('src')
                alt = img.get('alt')
                # If there is alt text, check for typos and potentially write to file
                if alt:
                    result = check_text(alt)
                    if len(result) > 0:
                        file.write("\t" + result + "\n")
                # If there is empty or missing alt text, note this issue in the file
                if (alt == "" or (alt is None)) and not ignore_empty:
                    file.write("\t" + "Empty or missing alt text!\n\t\tImage source link: " + src + "\n\t\tImage tag: " + str(img) + "\n")

def argparsing():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find potential typos in alt text.')
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
    """Add known words to spell checker.
    @param str file_name: Name of dict file of special known words. File should have 1 word per line."""
    if (file_name):
        with open(file_name, 'r') as file:
            spell.word_frequency.load_words(file.read().splitlines())

def main(argv):
    """Parse args and generate output file."""
    args = argparsing()
    ext = os.path.splitext(args.output)[1].lower()
    add_known_words(args.dict)
    generate_list(args.output, ext, args.links, bool(args.ignore_empty))

if __name__ == '__main__':
    main(sys.argv)