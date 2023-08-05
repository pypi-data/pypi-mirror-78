import requests


def search_avatar(user):
    """
    Search for github user's avatar.
    :param user: str with user's name
    :return: str with relative avatar link
    """
    url = f'https://api.github.com/users/{user}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(search_avatar('dougfraga'))
