from src.models.Show import *
from src.db.MyDBConnection import MyDBConnection
from src.models.Notification import Notification
from src.controllers.NotificationController import NotificationController
from src.api_helper.ApiHelperTMDB import ApiHelperTMDB

class ShowController:
    """
        This controller manages the Show model
    """

    @classmethod
    def get_one_minimal_info(cls, api_id: int, my_db: MyDBConnection):
        """
            This method creates a show object with attributes title, pict, api_id, season_next_episode_num,
            next_episode_num, date_next_episode. If the show already exists in the database, the object is created from
            the database and, depending on the date of last update, updated from API. Il the show doesn't exist in
            database, the object is created thanks to an API request, but is not created in DB (the show will be
            created in DB when the User add a preference).
        """
        show = Show.retrieve_show_from_bdd(api_id, my_db)
        if show is not None:
            # the show is in DB
            ShowController.check_for_update(my_db, show)
        else:
            api = ApiHelperTMDB()
            show = api.get_show(api_id)
        return show

    @classmethod
    def get_one_all_info(cls, show_api_id: int, my_db: MyDBConnection):
        """
            This method returns a show with complete info : in addition to title, pict, api_id, season_next_episode_num,
            next_episode_num, date_next_episode, the show object also has season_list, number_of_episodes,
            number_of_seasons attributes.
        """
        api = ApiHelperTMDB()
        api_show = api.get_show(show_api_id)
        # if the show is in database, we retrieve the db_id and update the show
        db_show = Show.retrieve_show_from_bdd(api_show.api_id, my_db)
        if db_show is not None:
            ShowController.check_for_update(my_db, db_show)
            api_show.db_id = db_show.db_id
        return api_show

    @classmethod
    def check_for_update(cls, my_db: MyDBConnection, show: Show):
        if (datetime.now() - show.last_maj).seconds > 3600:
            # the last update is too old, we update the show in API in DB.
            updated_show = ApiHelperTMDB().get_show(show.api_id)
            cls.update_show(my_db, show, updated_show.pict, updated_show.season_next_episode_num,
                            updated_show.next_episode_num, updated_show.date_next_episode)

    @classmethod
    def list_all_seasons(cls, show: Show):
        return show.season_list

    @classmethod
    def add_show(cls, my_db: MyDBConnection, title: str, pict: str, api_id: int, season_next_episode_num: int,
                 next_episode_num: int, date_next_episode:datetime):
        show = Show.retrieve_show_from_bdd(api_id, my_db)
        if show is None:
            show = Show(title, pict, api_id, season_next_episode_num, next_episode_num, date_next_episode)
            show.create_show_in_bdd(my_db)

    @classmethod
    def update_show(cls, my_db: MyDBConnection, show: Show, pict: str = None, season_next_episode_num: int = None,
                    next_episode_num: int = None, date_next_episode: datetime = None, season_list: List[Season] = None,
                    number_of_episodes: int = None, number_of_seasons: int = None):
        show.update_show(my_db=my_db, pict=pict, season_next_episode_num=season_next_episode_num,
                         next_episode_num=next_episode_num, date_next_episode=date_next_episode,
                         season_list=season_list, number_of_episodes=number_of_episodes,
                         number_of_seasons=number_of_seasons)
        for notification in Notification.get_notification_from_show(show, my_db):
            new_seen_flag = False
            if (notification.seen_flag or show.next_episode_num != notification.num_ep
                    or show.date_next_episode != notification.date_ep):
                new_seen_flag = True
            NotificationController.update_notification(my_db, notification, show, seen_flag=new_seen_flag)
