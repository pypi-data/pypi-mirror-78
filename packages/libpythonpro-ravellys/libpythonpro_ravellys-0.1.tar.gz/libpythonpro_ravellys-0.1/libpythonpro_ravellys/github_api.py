import requests


def buscar_avatar(usuario):
    """
    Busca o avatar do usu´rio no github
    :param usuario: str com o nome do usuário
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{usuario}'
    rep = requests.get(url)
    return rep.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('ravellys'))
