import os
import re
from collections import namedtuple
import argparse
from dotenv import load_dotenv
from instabot import Bot


def get_users_from_comment(comment):
    name_regex = re.compile(r"(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)")
    result = re.findall(name_regex, comment)
    return result


def get_users_id(users_name):
    users_id = []
    for username in users_name:
        user_id = bot.get_user_id_from_username(username)
        if user_id:
            users_id.append(user_id)
    if users_id:
        return users_id
    return None


def is_user_friend(user, target_users):
    if target_users is None:
        return False
    user_friends = bot.get_user_followers(user)
    if user_friends:
        for user in target_users:
            if user in user_friends:
                return True
    return False


def prepare_user_info(comments_list):
    comments_data = []
    for comment in comments_list:
        comments_data.append(
            (comment['user']['username'],
             comment['user']['pk'],
             get_users_id(get_users_from_comment(comment['text']))
             )
        )
    return comments_data


def unique_users(users_data):
    unique_names = set()
    User = namedtuple('User', 'name id friends')
    unique_users_data = [User(name=username, id=_id, friends=friends) for username, _id, friends in users_data
                         if not (username in unique_names or unique_names.add(username))]
    return unique_users_data


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
    unique_users_data = unique_users(users_data)
    tagged_friend = [item for item in unique_users_data if is_user_friend(item.name, item.friends)]
    liked_post = [item for item in tagged_friend if str(item.id) in media_likers]
    follow_to_owner = [item for item in liked_post if str(item.id) in owner_followers]
    potential_winners = [user.name for user in follow_to_owner]
    print(potential_winners)

