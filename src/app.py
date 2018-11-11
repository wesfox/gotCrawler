from flask import Flask

from flask_restful import Resource, Api
from flask_cors import CORS

from src.ressources import UserGet, UserAdd, UserPref, UserPrefDelPut, SeasonGet, EpisodeGet, ShowGet, ShowSearch, AuthUser, AuthRenew
from src.ressources.show import ShowTrending
class GotCrawlerApp:
    """
        This is the flask app 
    """
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.api = Api(self.app)

    def _initialize(self):
        self.api.add_resource(AuthUser, '/auth')
        self.api.add_resource(AuthRenew, '/auth/renew')

        self.api.add_resource(UserGet, '/user/<user_id>')
        self.api.add_resource(UserAdd, '/user')
        self.api.add_resource(UserPref, '/user/<user_id>/pref')
        self.api.add_resource(UserPrefDelPut, '/user/<user_id>/pref/<show_id>')

        self.api.add_resource(ShowGet, '/show/<api_id>')
        self.api.add_resource(ShowSearch, '/show/search')
        self.api.add_resource(ShowTrending, '/show/trending')
        self.api.add_resource(SeasonGet, '/show/<show_api_id>/season/<num_season>')
        self.api.add_resource(EpisodeGet, '/show/<show_api_id>/season/<num_season>/episode/<num_episode>')

    def start(self):
        self._initialize()
        self.app.run(debug=1)
