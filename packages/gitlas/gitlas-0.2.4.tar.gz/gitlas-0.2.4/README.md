# GitLas :The minimalist Git Log Statistics library
 [![Build Status](https://travis-ci.org/Abhi-1U/gitlas.svg?branch=master)](https://travis-ci.org/Abhi-1U/gitlas)
  [![PyPI version](https://badge.fury.io/py/gitlas.svg)](https://badge.fury.io/py/gitlas)  ![GitHub](https://img.shields.io/github/license/Abhi-1U/gitlas) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitlas?color=red)
 [![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
## Meta Data of Git
Often times we have a ton of Meta Data ,but we really don't have much of tools to make useful
analysis from it.
Git Logs are one of the best sources from which we can actually understand and analyse some of the trends in our Project workings.

The commits and merges can be tracked easily with git, but to make useful charts and analysis we need to convert these data into a useful data type.

GitLas is a simple Library that filters out gitlogs with regular expression pattern matching and applies useful analytic filters to get more out of the data. JSON data type is highly preferred and widely used, hence the library convert the git log into a simple JSON format which can be exported as well. 

These statistics can be useful or not really useful at all depending on the size of your project and the collaborators associated with it.
## Getting GitLog as text
To get the git log in a text format
   
```
$ git log > gitlog.txt
```

or copy it to the clipboard using some tool like xclip and later paste it in a new file.  

## Requirements
### Python 3  
## Installing gitlas 
using pip

```
$ pip install gitlas
``` 
or pip3 in some systems  

```
$ pip3 install gitlas
```
## Usage 
This library is designed to be used alongside data analysis and visualization libraries. additionaly you can also export git log data and or stat reports in JSON format.