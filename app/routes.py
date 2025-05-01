import logging

import flask
from flask import Response

from app.api_service import GetRepos, GetFollowers

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

@app.route("/api/<username>/followers", methods=["GET"])
def get_repo_followers(username):
    """
    Endpoint to get followers
    """
    response = GetFollowers.call(org_name=username).to_dict()
    return response, 200

@app.route("/api/<username>/repos", methods=["GET"])
def get_repos(username):
    """
    Endpoint to get public repos
    """
    response = GetRepos.call(org_name=username).to_dict()
    return response, 200
