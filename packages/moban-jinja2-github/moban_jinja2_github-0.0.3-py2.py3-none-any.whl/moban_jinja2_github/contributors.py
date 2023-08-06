from gease.exceptions import UrlNotFound
from gease.contributors import EndPoint


def get_contributors(user, repo, author):
    repo = EndPoint(user, repo)
    try:
        user_list = repo.get_all_contributors()

        user_list = [
            detail for detail in user_list if author not in detail["url"]
        ]
        return user_list
    except UrlNotFound:
        return []
