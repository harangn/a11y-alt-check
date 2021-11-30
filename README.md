# Accessibility Alt Check

While typos in alt text go unnoticed to sighted individuals, they create a jarring, unpleasant experience to screen reader users. Given one or more URLs, this alt text spellchecker will find potential typos in images' alternative text.

## Install

This project requires Python3, beautifulsoup4, and pyspellchecker.
```
pip install beautifulsoup4
pip install pyspellchecker
```

## Use

Given a file name and one or more links, `alt_text_spellchecker.py` creates the file and lists the potential typos their respective alt texts. The file name must have the extension included. The recommended file type is a text file (\*.txt).

### Accessibility

When outputting to a text file, tabs are used to indent the typo list beneath the page title and URL. The output can be copied from the text file into a word document, selected, and formatted as a list and the indentation levels will be preserved.

[Resources on Alternative Text for Images (W3C)](https://www.w3.org/WAI/alt/)

### Known Words

If there is a potential typo you want `alt_text_spellchecker.py` to ignore, you can create a custom dictionary file with 1 word per line and reference it with the dict flag (see [Usage](#usage) below).

### Usage

```
usage: alt_text_spellchecker.py [-h] [--ignore_empty] [--output OUTPUT] [--dict DICT] links [links ...]

Find suspected typos in alt text.

positional arguments:
  links            links to check alt text on

optional arguments:
  -h, --help       show this help message and exit
  --ignore_empty   ignore empty alt text; do not record it in output file
  --output OUTPUT  file to store output in; default output.txt
  --dict DICT      dictionary file of typos to ignore
```

### Example

Checking the GitHub home and explore pages:
```
python ./alt_text_spellchecker.py https://github.com/ https://github.com/explore
```
Checking the Github home and explore pages, saving to a custom output file github.txt, and adding a dict.txt (shown below) to add "github" and "changelog" as correct words:
```
python ./alt_text_spellchecker.py --output github.txt --dict dict.txt --ignore_empty https://github.com/ https://github.com/explore
```
*Content of `dict.txt`:*
```
github
changelog
```
