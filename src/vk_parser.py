import requests


def get_posts(token, version, domain):
    token = token
    version = version
    domain = domain

    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': 10
                            }
                            )
    data = response.json()['response']['items']
    return data


posts = get_posts('959d5e65959d5e65959d5e651c968c8f919959d959d5e65f60ec3723e409a0e81b86762', 5.131, 'gbou1357')
if 'attachments' in posts[0] and posts[0]['attachments'][0]['photo']['sizes'][2]['width'] > \
        posts[0]['attachments'][0]['photo']['sizes'][2]['height'] >= 400 and \
        posts[0]['attachments'][0]['photo']['sizes'][2]['width'] >= 600:
    print('yes')
else:
    print('no')
print(1)
