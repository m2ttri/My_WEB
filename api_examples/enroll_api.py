import requests

base_url = "http://127.0.0.1:8000/api/"

r = requests.get(f'{base_url}albums')
albums = r.json()

publish_albums = ', '.join([album['title'] for album in albums])
print(f'Published albums: {publish_albums}')
