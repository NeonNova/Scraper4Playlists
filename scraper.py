import requests
from bs4 import BeautifulSoup

# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/Apple_Music_100_Best_Albums'

def get_album_list(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    albums = []
    # Find the table containing the albums
    table = soup.find('table', class_='wikitable')
    if table:
        # Iterate over each row in the table
        for row in table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) >= 3:
                rank = columns[0].text.strip()
                title = columns[1].text.strip()
                artist = columns[2].text.strip()
                albums.append({'rank': rank, 'name': title, 'artist': artist})

    return albums

def save_albums_to_file(album_list, filename='albums.txt'):
    with open(filename, 'w') as file:
        for album in album_list:
            file.write(f"Rank: {album['rank']}, Name: {album['name']}, Artist: {album['artist']}\n")

if __name__ == '__main__':
    album_list = get_album_list(url)
    save_albums_to_file(album_list)
    print("Albums saved to 'albums.txt' file.")
