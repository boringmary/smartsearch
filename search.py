#!/usr/bin/python
# -*- coding: utf-8-*-
import os
import sys
from unidecode import unidecode


import base
import smartsearch as ss


def index_file(items, index):
    all = ss.get([i[0] for i in items])
    items = {x: y for x, y in all.iteritems() if y}
    for id, body in items.iteritems():
        try:
            body = unicode(body, encoding='utf-8')
        except TypeError:
            pass
        ss.index(id, unidecode(body), index='test-index')
    return


def index_dir(dir, index='test-index'):
    sequence = base.create_list_of_dirs(dir, 100)
    for items in sequence:
        index_file(items, index)
    return

def index_url(url, index='test-index'):
    sequence = base.get_packages(url, limit=10)
    for i in sequence:
        a = list(sequence)
        index_file(i, index)

def search(query, index='test-index'):
    query = unicode(query, encoding='utf-8')
    ids = ss.search(unidecode(query), index)
    return ids or 'Sorry, but nothing matched your search criteria'


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'index-dir':
        index_dir(*args[1:])
        print 'Done!'
    elif args[0] == 'search':
        print search(*args[1:])
    elif args[0] == 'delete-all':
        ss.delete_all()
