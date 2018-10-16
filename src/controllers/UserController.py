from src.models.User import *
from src.models.Show import *
from src.models.Notification import *

class UserController:

    """
        This controller manages the User model
    """

    @classmethod
    def get_one(cls, id_user : int):
        #TODO
        pass

    @classmethod
    def add_user(cls,firstname: str, surname: str, login: str, pwd: str, poster: str,
                 list_preferences: List[Show]=None):
        user= User(firstname,surname, login, pwd, poster, list_preferences)
        user.create_user_in_bdd()

    @classmethod
    def update_user(cls,user : User, firstname: str=None, surname: str=None, login: str=None, pwd: str=None, poster: str=None,
                 list_preferences: List[Show]=None):
        user.update_user_in_bdd(firstname, surname, login, pwd, poster, list_preferences)

    @classmethod
    def del_user(cls, user: User):
        user.delete_user_in_bdd()

    @classmethod
    def get_user_notification(cls, user : User):
        Notification.get_notification_from_user_id(user.id)
