"""
Post service
"""
import datetime

from pymongo.errors import DuplicateKeyError

from profiles.service import ProfileService
from social.settings import DB


POSTS = DB["posts"]
USERS = DB["auth_user"]


class PostService:
    """
    Post service class
    """

    @staticmethod
    def create_post(author, title, content):
        """

        :param author:
        :param title:
        :param content:
        :return:
        """
        post = {
            "author": author,
            "title": title,
            "content": content,
            "date": datetime.datetime.utcnow(),
            "comments": []
        }
        post_found = POSTS.find_one({"author": author, "title": title})
        if post_found is not None:
            return post_found
        post = POSTS.insert_one(post)
        return post

    @staticmethod
    def add_comment(post_author, post_title, comment_author, comment):
        """

        :param post_author:
        :param post_title:
        :param comment_author:
        :param comment:
        :return:
        """
        post = POSTS.find_one({"author": post_author, "title": post_title})
        if post:
            POSTS.find_one_and_update(
                {"author": post_author, "title": post_title},
                {"$push": {"comments": {"author": comment_author, "comment": comment}}},
                upsert=True)

    @staticmethod
    def get_posts_by_author(username):
        """

        :param username:
        :return:
        """
        result = list(POSTS.find({"author": username}))
        return result

    @staticmethod
    def get_posts_for_user(username):
        """
        get post of all users that current user follows

        :param username:
        :return:
        """
        result = []
        user = ProfileService.get_profile(username)
        follows = user['follows']
        follows.append(username)

        for fol in follows:
            posts = PostService.get_posts_by_author(fol)
            result.extend(posts)
        return result

    @staticmethod
    def get_all_posts():
        result = POSTS.find()
        return result

    @staticmethod
    def get_post(title, author):
        result = POSTS.find_one({'author': author, 'title': title})
        return result
