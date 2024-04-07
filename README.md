# Overview
A list of utilities written in python to search filter and classify job postings from linkedin.
The search results are saved , essentially cached , in a sqlite file and should be periodically invalidated.

## search
A sample script that uses selenium to search for job postings and save them.
So far , it seems that to get best results we should search using multiple similar terms , with overlapping results then use other tools to search on those curated results 

## filter
Apply regex text filters to the results cached using the previous tools


# How to run

Assuming you have python installed , you need to do the following to run these scripts :
## First time installation

1. Create a virtual environment 

```bash
python -m venv venv
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Setup db
to create required tables run 

```bash
py ./db/init_db.py
```


## To use utils

Activate the virtual environment

```bash
.\venv\Scripts\activate
```

### search.py

### filter.py