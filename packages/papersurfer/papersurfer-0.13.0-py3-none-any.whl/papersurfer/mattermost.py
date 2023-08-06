"""Simplified mattermost interface."""
import logging
import time
import json
import requests
import mattermostdriver
from .exceptions import ConfigError
from .dtos import PostDTO
from .doi import Doi
from . import config


class Mattermost:
    """Provide a simplified interaction w/ mattermost api."""
    def __init__(self, url, channelname, username, password):
        self.posts = []
        self._mattermost = mattermostdriver.Driver({
            'url': url,
            'login_id': username,
            'password': password,
            'port': 443
        })

        self._loggedin = False
        self._reporters = {}
        self._channelname = channelname
        self._channel = None

    def _login(self):
        try:
            self._mattermost.login()
        except (mattermostdriver.exceptions.NoAccessTokenProvided,
                requests.exceptions.InvalidURL,
                requests.exceptions.HTTPError):
            print("Failed to log into Mattermost.")
            raise ConfigError

        try:
            self._channel = self._get_channel(self._channelname)
        except ConfigError:
            print("Couldn't find Mattermost channel.")
            raise ConfigError

        self._loggedin = True

    def _get_channel(self, channelname):
        """Try to find the paper channel by display name."""
        teamapi = self._mattermost.teams
        channelapi = self._mattermost.channels
        teams = [team["id"] for team in teamapi.get_user_teams("me")]
        channels = []
        for team in teams:
            teamchannels = [channel for channel
                            in channelapi.get_channels_for_user("me", team)
                            if channel["display_name"] == channelname]
            channels.extend(teamchannels)

        # lets just hope no-one has the same channel name in multiple teams
        if len(channels) == 0:
            print(f"Channel {channelname} does not exits")
            raise ConfigError
        return channels[0]["id"]

    def _get_reporter(self, userid):
        """Load user from mattermost api and cache."""
        userapi = self._mattermost.users
        if userid not in self._reporters:
            self._reporters[userid] = userapi.get_user(userid)["username"]

        return self._reporters[userid]

    def _retrieve_all_posts(self, since):
        """Retrieve all posts from mattermost, unfiltered for papers."""
        posts = []
        params = {"since": since} if since else {}

        start = time.perf_counter()

        while True:
            resp = self._mattermost.posts.get_posts_for_channel(
                self._channel, params)
            posts.extend(resp['posts'].values())
            if resp["prev_post_id"]:
                params["before"] = resp["prev_post_id"]
            else:
                break

        if config.debug:
            with open("all_posts.json", "w") as filehandle:
                json.dump(posts, filehandle, indent=4)

        dtos = [PostDTO(
                        id=m['id'],
                        create_at=m['create_at'],
                        message=m['message'],
                        reporter=self._get_reporter(m['user_id']),
                        doi=Doi().extract_doi(m['message']),)
                for m in posts]

        logging.debug("retrieving and processing %i mattermost posts took %f",
                      len(posts), time.perf_counter() - start)

        return dtos

    def _filter_incoming(self, posts):
        """Filter posts from mattermost to only papers."""
        return [p for p in posts if "doi" in p.message]

    def retrieve(self, since=None):
        """Retrieve papers from mattermost channel."""
        if not self._loggedin:
            self._login()
        posts = self._retrieve_all_posts(since)
        self.posts = self._filter_incoming(posts)
        return self.posts

    def check_doi_exits(self, doi):
        """Check for doi in current paper list."""
        doi_needle = Doi().extract_doi(doi)
        posts_found = [posts for posts in self.posts
                       if Doi().extract_doi(posts.doi) == doi_needle]
        return bool(posts_found)

    def post(self, message):
        """Post message to thread."""
        self._mattermost.posts.create_post({"channel_id": self._channel,
                                            "message": message})
