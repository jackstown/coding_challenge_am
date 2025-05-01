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

### Get metadata from public repositories (separated by original and forked repos)
```
curl -i "http://127.0.0.1:5000/api/<username>/repos"
```

Example:
```
curl -i "http://127.0.0.1:5000/api/mailchimp/repos"
```

### Total watcher/follower count
```
curl -i "http://127.0.0.1:5000/api/<username>/followers"
```
