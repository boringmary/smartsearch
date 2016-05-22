import os
import json
import xmlrpclib
import requests

from itertools import islice

import smartsearch as ss


def unpack_packages(packages):
    url = 'https://pypi.python.org/pypi'
    print packages
    dict_of_urls = {package: url + '/' + package + '/json' for package in packages}
    result = []
    for key, value in dict_of_urls.iteritems():
        get = requests.get(value)
        if not get:
            break
        body = json.loads(get.text)
        result.extend([(key, u'{} {}'.format(body['info']['description'], body['info']['summary']))])
    return result


def get_packages(url, limit=10):
    client = xmlrpclib.ServerProxy(url)
    list_of_packs = client.list_packages()
    for i in iter_chunks(list_of_packs, limit):
        yield unpack_packages(i)


def iter_chunks(seq, chunk_size):
    it = iter(seq)
    while True:
        chunk = list(islice(it, chunk_size))
        if chunk:
            yield chunk
        else:
            break

def create_list_of_dirs(obj, chunk_size):
    sequence = os.walk(obj)
    for root, dirs, files in iter_chunks(sequence, chunk_size):
        yield [(x, ss.get(os.path.join(root, x))) for x in files]