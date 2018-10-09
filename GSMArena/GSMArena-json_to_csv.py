import json
import re
YEAR = re.compile(r'\b\d{4}\b')
DS = re.compile(r'\b(\d{3,4}\s?x\s?\d{3,4})\b\s?pixels')
DR = re.compile(r'\b(\d{1,2}:\d{1,2})\s?ratio')
BC = re.compile(r'\b(\d{3,4})\s?mAh')
WEIGHT = re.compile(r'\b(\d{2,3})\s?g\b')
RAM = re.compile(r'\b(\d{1,4}\s?\wB)\s?RAM')
OSV = re.compile(r'^(\D+)(?:\s\d|$)')
CAM = re.compile(r'\b(\d{1,3}(?:\.\d{1,2})?)\s?MP')
VIDRES = re.compile(r'\b(\d{3,4})p')
BT = re.compile(r'\b(\d{1,3}(?:\.\d{1,2})?)\b')
PPI = re.compile(r'\b(\d{2,4})\s?ppi')

with open("GSMArena.com.json") as f:
    phones_data = json.load(f)


def get_year(string):
    year = YEAR.search(string)
    if year and '1990' < year.group() < '2020':
        return year.group()
    else:
        return None


def get_pln_price(price):
    if not price:
        return None
    conv = {"INR": 19.83,
            "USD": 0.27,
            "EUR": 0.23}
    _, amount, currency = price.split()
    return str(int(int(amount)*conv[currency]))


def search_or_none(pattern, value):
    search = pattern.search(value)
    return search and (search.groups() and search.groups()[0] or search.group()) or None


data_parser = {
    'Manufacturer': lambda x: x['modelname'].split()[0],
    'Model Name': lambda x: x['modelname'],
    'LTE': lambda x: 'YES' if 'LTE' in x['nettech'].upper() else 'NO',
    'GSM': lambda x: 'YES' if 'GSM' in x['nettech'].upper() else 'NO',
    'HSPA': lambda x: 'YES' if 'HSPA' in x['nettech'].upper() else 'NO',
    'Accelerometer': lambda x: 'YES' if 'ACCELEROMETER' in x['nettech'].upper() else 'NO',
    'Proximity': lambda x: 'YES' if 'PROXIMITY' in x['nettech'].upper() else 'NO',
    'Year': lambda x: get_year(x['released-hl']),
    'Screen Resolution': lambda x: search_or_none(DS, x['displayresolution']),
    'Screen Ratio': lambda x: search_or_none(DR, x['displayresolution']),
    'PPI': lambda x: search_or_none(PPI, x['displayresolution']),
    'Capacity': lambda x: search_or_none(BC, x['batdescription1']),
    'Weight': lambda x: search_or_none(WEIGHT, x['weight']),
    'Price': lambda x: get_pln_price(x.get('price')),
    'RAM': lambda x: search_or_none(RAM, x.get('internalmemory', '')),
    'OS': lambda x: search_or_none(OSV, x['os']) if 'os' in x else None,
    'Back Camera Resolution': lambda x: search_or_none(CAM, x.get('cam1modules', '')),
    'Back Camera Video Resolution': lambda x: search_or_none(VIDRES, x.get('cam1video', '')),
    'Front Camera Resolution': lambda x: search_or_none(CAM, x.get('cam2modules', '')),
    'Front Camera Video Resolution': lambda x: search_or_none(VIDRES, x.get('cam2video', '')),
    'Bluetooth': lambda x: search_or_none(BT, x.get('bluetooth', '')),
}

with open('GSMArena.csv', 'w') as f:
    order = list(data_parser.keys())
    f.write(';'.join(order))
    for phone in phones_data:
        parsed_phone = {name: parser(phone) for name, parser in data_parser.items()}
        if not any(v is None for v in parsed_phone.values()):
            f.write('\n')
            f.write(';'.join(parsed_phone[x] for x in order))
