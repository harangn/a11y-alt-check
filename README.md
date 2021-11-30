# Alt Text Spellchecker

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

When outputting to a text file, tabs are used to indent the typo list beneath the page title and URL. This means that the output can be copied from the text file into a word document, selected, and formatted as a list and the indentation levels will be preserved.

[Resources on Alternative Text for Images (W3C)](https://www.w3.org/WAI/alt/)

### Known Words

If there is a potential typo you want `alt_text_spellchecker.py` to ignore, you can add it to the list stored in `special_known_words`.

### Usage

```
usage: alt_text_spellchecker.py [-h] [--ignore_empty] file_name links [links ...]

Find suspected typos in alt text.

positional arguments:
  file_name       file to store output in
  links           links to check alt text on

optional arguments:
  -h, --help      show this help message and exit
  --ignore_empty  ignore empty alt text; do not record it in output file
```

#### Examples

Checking the GitHub home and explore pages:
```
python ./alt_text_spellchecker.py output.txt https://github.com/ https://github.com/explore
```

Ignoring empty alt text:
```
python ./alt_text_spellchecker.py --ignore_empty output.txt https://github.com/ https://github.com/explore
```
