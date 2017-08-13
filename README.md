[![Build Status](https://travis-ci.org/Incorrectlyspelt/tracker.svg?branch=master)](https://travis-ci.org/Incorrectlyspelt/tracker)
# tracker
A basic system statistics tracker written in python using Flask,Peewee and Pygal

Includes its own API for some reason

## Running
How to run: `python3 runp.py`  
Then go to `localhost:5000` for graphs

## API
Api is on `/api/v1/<name>`  
it returns Peewee Generated json objects separated by commas
 