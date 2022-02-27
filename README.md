# Accessibility Alt Check

While typos in alt text go unnoticed to sighted individuals, they create a jarring, unpleasant experience for screen reader users. Given one or more URLs, the spellchecker will find potential typos in images' alternative text.

[Resources on Alternative Text for Images (W3C)](https://www.w3.org/WAI/alt/)

## Install

This project requires Python3, beautifulsoup4, pyspellchecker, and lxml.
```
pip install beautifulsoup4
pip install pyspellchecker
pip install lxml
```

## Use

Given a file name and one or more links, `alt_text_spellchecker.py` creates the file and lists the potential typos their respective alt texts. The file name must have the extension included. The recommended file type is a text file (\*.txt).

### Output

When outputting to a text file, tabs are used to indent each typo listed after its page title and URL. This output can be made into an ordered or unordered list in a Word document by:
1. Copy the output from the text file into a Word document.
2. Select all content (`ctrl+a`).
3. Manually format as a list. It can be unordered (`alt h u` then select type) or ordered (`alt h n` then select type).

#### Output List Organization

Word preserves the indentation levels, resulting in a useful formatted list with the following characteristics:
* Top-level list items: Link title and URL.
* Nested list item: Alt text issue.
* Sub-nested list item: `src` attribute value and `img` tag of element with empty or missing alt text.

### Known Words

If there is a potential typo you want `alt_text_spellchecker.py` to ignore, you can create a custom dictionary file with 1 word per line and reference it with the dict flag (see [Usage](#usage) below).

### Usage

```
usage: alt_text_spellchecker.py [-h] [--ignore_empty] [--output OUTPUT] [--dict DICT] links [links ...]

Find potential typos in alt text.

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
#### Content of `dict.txt`:
```
github
changelog
```
