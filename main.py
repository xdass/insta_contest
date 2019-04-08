import os
import re
from collections import namedtuple
import argparse
from dotenv import load_dotenv
from instabot import Bot


User = namedtuple('User', 'name id friends')


def get_users_from_comment(comment):
    # https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
    name_regex = re.compile(r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)")
    users_names = re.findall(name_regex, comment)
    return users_names


def is_user_friend(user, target_users):
    if target_users is None:
        return False
    user_friends = bot.get_user_followers(user)
    if not user_friends:
        return False
    return any([user in user_friends for user in target_users])


def collect_participants_info(comments_list):
    users_info = dict()
    for comment in comments_list:
        if comment['user']['username'] not in users_info:
            users_ids_from_comment = [
                bot.get_user_id_from_username(username) for username in get_users_from_comment(comment['text'])
            ]
            users_info[comment['user']['username']] = (
                comment['user']['pk'],
                users_ids_from_comment
            )
    return users_info


def convert_to_namedtuple(users):
    id_idx = 0
    friends_idx = 1
    converted = [User(name=username, id=users[username][id_idx], friends=users[username][friends_idx])
                 for username in users.keys()]
    return converted


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
    participants_info = collect_participants_info(all_comments)
    unique_users = convert_to_namedtuple(participants_info)
    who_tagged_friend = [user for user in unique_users if is_user_friend(user.name, user.friends)]
    who_liked_post = [user for user in who_tagged_friend if str(user.id) in media_likers]
    follow_to_owner = [user for user in who_liked_post if str(user.id) in owner_followers]
    potential_winners = [user.name for user in follow_to_owner]
    print(potential_winners)

