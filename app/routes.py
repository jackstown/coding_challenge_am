import logging

import flask
from flask import Response

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)

@app.route("/api/repos", methods=["GET"])
def get_repos():
    """
    Endpoint to get public repos
    """
    return Response("All Good!", status=200)

@app.route("/api/repo/followers", methods=["GET"])
def get_repo_followers():
    """
    Endpoint to get repo followers
    """
    return Response("All Good!", status=200)

@app.route("/api/repo/languages", methods=["GET"])
def get_repo_languages():
    """
    Endpoint to get repo languages
    """
    return Response("All Good!", status=200)

@app.route("/api/repo/topics", methods=["GET"])
def get_repo_topics():
    """
    Endpoint to get repo topics
    """
    return Response("All Good!", status=200)
