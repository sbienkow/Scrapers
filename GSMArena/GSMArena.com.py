from requests_html import HTMLSession
from itertools import chain
import json
import sys


MAKERS_LIST_URL = "https://www.gsmarena.com/makers.php3"
MAKER_SELECTOR = "div[class=st-text]"
PHONE_PAGE_SELECTOR = "div[class=makers] a"
PHONE_DATA_SELECTOR = "[data-spec]"


def progress(iterable, msg="Used {} elements!"):
    iter_len = len(iterable)
    for index, item in enumerate(iterable, 1):
        progress_bar(index, iter_len, msg.format(index))
        yield item


def progress_bar(count, total, status=''):
    bar_len = 40
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


session = HTMLSession()
makers_list = session.get(MAKERS_LIST_URL).html.find(MAKER_SELECTOR, first=True).absolute_links

print(f'Found {len(makers_list)} phone makers!\n')

phone_page_urls = []

for maker_url in makers_list:
    print(f'Downloading maker page: {maker_url}')
    maker_phones_page = session.get(maker_url)
    maker_phones_urls = list(chain(*map(lambda x: x.absolute_links, maker_phones_page.html.find(PHONE_PAGE_SELECTOR))))
    print(f'Found {len(maker_phones_urls)} phones from this maker\n')
    phone_page_urls.extend(maker_phones_urls)

print(f"\nGot {len(phone_page_urls)} phones total!\n")

phones_data = []
for idx, phone_page_url in enumerate(progress(phone_page_urls, "Downloaded {} elements")):
    phone_page = session.get(phone_page_url)
    phone_table = phone_page.html.find(PHONE_DATA_SELECTOR)
    phone_data = {}
    for element in phone_table:
        phone_data[element.attrs['data-spec']] = element.text
    phones_data.append(phone_data)

with open("GSMArena.com.json", "w") as f:
    json.dump(phones_data, f)

print()
