"""
profiles service
"""
from django.core.exceptions import ObjectDoesNotExist
from djongo.sql2mongo import SQLDecodeError
from django.contrib.auth.models import User

from social.settings import DB



USERS = DB["auth_user"]


class ProfileService:
    """
    profile service class
    """

    @staticmethod
    def get_profile(username):
        """
        get profile by username

        :param username: string
        :return: profile instance if found, else None
        """
        profile = USERS.find_one({'username': username})
        return profile

    @staticmethod
    def follow_user(follower_name, user_name):
        """

        :param follower_name:
        :param user_name:
        :return: True if Updated, else False
        """
        if follower_name == user_name:
            return False

        user = ProfileService.get_profile(user_name)
        follower = ProfileService.get_profile(follower_name)
        if follower_name in user['followers']:
            return True
        if user and follower:
            # add follower to user
            USERS.find_one_and_update(
                {"username": user_name},
                {"$push": {"followers": follower_name}},
                upsert=True)
            # add follows to follower
            USERS.find_one_and_update(
                {"username": follower_name},
                {"$push": {"follows": user_name}},
                upsert=True)
            return True
        return False

    @staticmethod
    def unfollow_user(follower_name, user_name):
        """

        :param follower_name:
        :param user_name:
        :return: True if Updated, else False
        """
        if follower_name == user_name:
            return False

        user = ProfileService.get_profile(user_name)
        follower = ProfileService.get_profile(follower_name)
        if follower_name not in user['followers']:
            return True

        if user and follower:
            USERS.find_one_and_update(
                {"username": user_name},
                {"$pull": {"followers": follower_name}},
                upsert=True)

            USERS.find_one_and_update(
                {"username": follower_name},
                {"$pull": {"follows": user_name}},
                upsert=True)
            return True
        return False

    @staticmethod
    def get_all_profiles():
        """

        :return:
        """
        result = list(USERS.find({}))
        return result

    @staticmethod
    def create_user(username, password, email):
        """
        Creates user instance and tries to add it into database.
        Returns:
            user instance if added successfully,
            None otherwise.
        """

        try:
            found = USERS.find_one({"username": username})
            if found:
                return None
            user = User.objects.create_user(username=username, email=email, password=password)
            #user.id = len([USERS.find({})]) + 1 
            # USERS.insert_one({
            #     "id": USERS.count({}) + 1,
            #     "password": user.password,
            #     "username" : user.username,
            #     "email" : user.email,
            #     "is_active" : True,
            #     })
            user.save()
            return user
        except TypeError:
            USERS.find_one_and_update(
                {"username": username},
                {"$set": {"followers": [], "follows": [], "id": USERS.count({}) + 1}},  
                upsert=True)
            return user


    @staticmethod
    def get_by_username(username):
        """
        Returns:
            user instance if found,
            None otherwise.
        """
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None


    @staticmethod
    def change_password(username, new_password):
        """
        Method to change user password.
        Returns:
            user instance if password was changed,
            None otherwise.
        """
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
        user.set_password(new_password)
        try:
            user.save()
            return user
        except SQLDecodeError:
            return None
