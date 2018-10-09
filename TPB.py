from requests_html import HTMLSession
session = HTMLSession()

basic_search = 'Masterchef'
advanced_search = 'MasterChef.US.S09'

url = f'https://thepiratebay.org/search/{basic_search}/{{number}}/'

for number in range(10):
    r = session.get(url.format(number=number))
    sr = r.html.find('#searchResult', first=True)
    torrents = [link for link in sr.absolute_links if link.startswith('https://thepiratebay.org/torrent/')]
    ettv_torrents = [tlink for tlink in torrents if tlink.endswith('[ettv]')]
    MS_US_S9_torrents = [link for link in ettv_torrents if advanced_search in link]
    for torrent in MS_US_S9_torrents:
        print(torrent)
