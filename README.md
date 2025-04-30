# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
```


## Endpoints

### Total watcher/follower count
```
curl -i "http://127.0.0.1:5000/api/<username>/followers"
```

### Total number of public repositories (separated by original and forked repos)
```
curl -i "http://127.0.0.1:5000/api/<username>/repos"
```

### List/Count of languages used across all public repos
```
curl -i "http://127.0.0.1:5000/api/<username>/repo/languages"
```

### List/Count of repository topics
```
curl -i "http://127.0.0.1:5000/api/<username>/repo/topics"
```