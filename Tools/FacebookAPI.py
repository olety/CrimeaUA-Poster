import requests


class FacebookAPI:

    token = ''

    def __init__(self, token=''):
        self.token = token