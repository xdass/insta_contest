import os
import re
from collections import namedtuple
import argparse
from dotenv import load_dotenv
from instabot import Bot


def get_users_from_comment(comment):
    # https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
    name_regex = re.compile(r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)")
    users_name = re.findall(name_regex, comment)
    return users_name


def get_users_id(users_name):
    users_id = [bot.get_user_id_from_username(username) for username in users_name]
    return users_id


def is_user_friend(user, target_users):
    if target_users is None:
        return False
    user_friends = bot.get_user_followers(user)
    if not user_friends:
        return False
    return any([user in user_friends for user in target_users])


def prepare_user_info(comments_list):
    comments_data = []
    exists_names = set()
    for comment in comments_list:
        if comment['user']['username'] not in exists_names:
            comments_data.append(
                (comment['user']['username'],
                 comment['user']['pk'],
                 get_users_id(get_users_from_comment(comment['text']))
                 )
            )
            exists_names.add(comment['user']['username'])
    return comments_data


def convert_data(users_data):
    User = namedtuple('User', 'name id friends')
    converted_data = [User(name=username, id=_id, friends=friends) for username, _id, friends in users_data]
    return converted_data


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='This app help to determine winner of Instagram contests',
    )
    parser.add_argument('url', help='Enter link to the page with contest')
    args = parser.parse_args()
    post_url = args.url
    bot = Bot()
    bot.login(username=os.getenv('login'), password=os.getenv('password'))
    media_id = bot.get_media_id_from_link(post_url)
    media_owner_id = bot.get_media_owner(media_id)
    media_likers = bot.get_media_likers(media_id)
    owner_followers = bot.get_user_followers(media_owner_id)
    all_comments = bot.get_media_comments_all(media_id)
    users_data = prepare_user_info(all_comments)
    unique_users = convert_data(users_data)
    who_tagged_friend = [user for user in unique_users if is_user_friend(user.name, user.friends)]
    who_liked_post = [user for user in who_tagged_friend if str(user.id) in media_likers]
    follow_to_owner = [user for user in who_liked_post if str(user.id) in owner_followers]
    potential_winners = [user.name for user in follow_to_owner]
    print(potential_winners)

