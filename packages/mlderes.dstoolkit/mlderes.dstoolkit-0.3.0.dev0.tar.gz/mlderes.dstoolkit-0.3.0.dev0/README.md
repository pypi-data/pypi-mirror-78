[![Known Vulnerabilities](https://snyk.io/test/github/MLDERES/dstoolkit/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/MLDERES/dstoolkit?targetFile=requirements.txt)

# DSToolkit - utilities for better analytics projects
A library of tools that I use to manage files, clean datasets and do exploratory data analysis

## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Usage](#usage)
* [Contributions](#contributions)
* [Todo](#todo)
* [License](#license)

## General Info
This library is a set of tools for managing files, cleaning data and doing exploratory data analysis.

This all started because I found myself creating lots and lots of versions of data files in various states of completeness.  I would scrape some data, write it a file (in the data/raw folder) then work on it some and save it to the data/processed folder.  After a few iterations, I couldn't remember if it was data/raw/scraped_page1.csv or data/raw/scraped_page101.csv that was the latest.  So I started to name the files with a timestamp appendage scraped_page_01011850.csv (for a file that was created on Jan 1 at 6:50pm).  So I needed a utility to create the timestamps and then get the lastest version of the file.  I copied this code so much that I decided to use it as a way to learn about creating real Python projects, GitHub hooks, Visual Studio Code, Docker Containers and more.

## Technologies
* Python 3.7
* [Pandas](https://pandas.pydata.org)

## Usage
`pip install -U mlderes.dstoolkit`

In your module:
``` 
from mlderes.dstoolkit import get_latest_data_filename, DataFolder, make_ts_filename, write_data

data_folder = DataFolder('./data') # root data folder
DATA_RAW = data_folder.RAW
DATA_EXTERNAL = data_folder/'external'

# Get the filename (path) of the file like foo* in the ./data/raw directory
fp = get_latest_data_filename(DATA_RAW, 'foo')
```

## Contributions
This project was developed using [Visual Studio Code](https://code.visualstudio.com/Download) and leverages the support the platform has for developing in containers, so if you have [Docker Desktop](https://hub.docker.com) installed, you should be able to fork this repo, download a copy to locally and open the folder in a container.  All the dependencies are there, nothing to install, no need to worry about specific versions of libraries, creating venvs on your machine.  Heck you don't even need Python installed!

Contributions to documentation, utilities and issues are welcome.  All pull requests must include unittests and all existing tests must pass before being considered.

## Todo
* Make documentation as part of build
* Add more samples to documentation

## License
This work is licensed under the [GPL](license), which guarentees end users the freedom to study, share, and modify the software for your own use.

