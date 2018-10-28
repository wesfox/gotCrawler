from flask_restful import Resource

from src.controllers.EpisodeController import EpisodeController


class EpisodeGet(Resource):
    """
        Get an episode of a season of a show
    """
    def get(self, show_api_id, num_season, num_episode):
        episode = EpisodeController.get_one_ep(show_api_id, num_season, num_episode)
        return episode.to_json()
