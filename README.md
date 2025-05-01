# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Caveats

### Updated Dependencies

I noticed the repo is over 6 years old, with outdated dependencies that contained severe security vulnerabilities.

Also, Python 3.6 is end of life, and missing key features like F-Strings and other native library functionality.

I updated to use Python 3.12, and I also pinned the dependencies to versions that fix known vulnerabilities, to avoid security holes.

### Bitbucket Missing Fields

Bitbucket is missing several fields in its API, namely watcher/follower and topic counts.

It is possible to get the total watchers count by iterating over all the repos via pagination, and then hitting the watchers endpoint.

This requires further pagination, and is a fairly expensive operation.

However, if needed, I can implement this using ThreadPools and making the calls asyncronous.

### Synchronous API calls

A thread pool can be used to make the calls asynchronous to make the API service calls more performant.

The program, as is, functions well enough, but can be optimized in this way.


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

#### Example for mailchimp:
```
curl -i "http://127.0.0.1:5000/api/mailchimp/repos"
```

#### Response:

```
{
  "bitbucket": {
    "forked_repos": 0,
    "original_repos": 10,
    "repo_language_counts": {
      "dart": 1,
      "javascript": 3,
      "php": 2,
      "python": 2,
      "ruby": 2
    },
    "repo_topic_counts": {}
  },
  "github": {
    "forked_repos": 4,
    "original_repos": 27,
    "repo_language_counts": {
      "CSS": 1,
      "Java": 1,
      "JavaScript": 4,
      "Kotlin": 1,
      "Mustache": 1,
      "None": 2,
      "Objective-C": 2,
      "PHP": 9,
      "Python": 3,
      "Ruby": 6,
      "Swift": 1
    },
    "repo_topic_counts": {
      "android-sdk": 1,
      "ecommerce": 2,
      "email": 1,
      "email-marketing": 2,
      "ios-sdk": 1,
      "kotlin": 1,
      "magento": 2,
      "magento2": 1,
      "mailchimp": 12,
      "mailchimp-api": 5,
      "mailchimp-api-v3": 5,
      "mailchimp-api-wrapper": 5,
      "mailchimp-php": 1,
      "mailchimp-sdk": 11,
      "mandrill": 4,
      "mandrill-api": 4,
      "mandrill-api-wrapper": 4,
      "mandrill-node": 1,
      "marketing": 1,
      "newsletter": 1,
      "node": 1,
      "nodejs": 2,
      "php": 3,
      "python": 2,
      "ruby": 2,
      "sdk": 2,
      "sdk-android": 1,
      "sdk-ios": 1,
      "signup": 1,
      "swift": 1,
      "wordpress": 1,
      "wordpress-p": 1
    }
  },
  "org_name": "mailchimp"
}
```

### Total watcher/follower count
```
curl -i "http://127.0.0.1:5000/api/<username>/followers"
```

#### Example for mailchimp:

```
curl -i "http://127.0.0.1:5000/api/mailchimp/followers"
```

#### Response:

```
{
  "bitbucket": {
    "followers": 0
  },
  "github": {
    "followers": 112
  },
  "org_name": "mailchimp"
}
```
