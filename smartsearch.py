# Install elastic from https://www.elastic.co/downloads/elasticsearch
# and ``pip install elasticsearch==2.3.0``

from elasticsearch import Elasticsearch

es = Elasticsearch()


def index(id, body, index='test-index', refresh=False):
    """Add document to index

    :param id: document id
    :param body: document body
    :param index: index to use
    :param refresh: flush changes so it will be available immediately
    """
    es.index(index, doc_type='test', refresh=refresh,
             id=id, body={'text': body})


def search(query, index='test-index'):
    """Search document in index

    :param query: some text to find
    :param index: index to use
    :return: list of document ids
    """
    result = es.search(index=index, body={'query': {'match': {'text': query}}}, fields=['_id'])
    return [r['_id'] for r in result['hits']['hits']]


def get(ids, index='test-index'):
    """Check if index contains particular ids

    :param ids: list of document ids
    :param index: index to use
    :return: dict of {'id': found}
    """
    if not ids:
        return {}

    return {r['_id']: r.get('found')
            for r in es.mget(index=index, body={'ids': ids})['docs']}


def delete_all(index='test-index'):
    """Delete all documents

    :param index: index to use
    """
    es.indices.delete(index, ignore=404)


def test_simple_usage():
    delete_all(index='test-test')
    index('one', 'quick brown fox jumps over the lazy dog', 'test-test', refresh=True)
    index('two', 'slow purple rabbit crawls under the industrious cat', 'test-test', refresh=True)

    assert search('slow pussy', 'test-test') == ['two'] 
    assert search('brown jump', 'test-test') == ['one']
    assert not search('red carpet', 'test-test')

    assert get([], 'test-test') == {}
    assert get(['one', 'garbage'], 'test-test') == {'one': True, 'garbage': False}
