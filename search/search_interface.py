from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

app = Flask(__name__)

es = Elasticsearch([{'host': Config.ELASTICSEARCH_HOST, 'port': Config.ELASTICSEARCH_PORT}])

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = perform_search(query)
        return render_template('search_results.html', query=query, results=results)
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search_api():
    query = request.json['query']
    results = perform_search(query)
    return jsonify(results)

def perform_search(query):
    search_body = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title', 'content']
            }
        },
        'highlight': {
            'fields': {
                'title': {},
                'content': {}
            }
        }
    }

    search_results = es.search(index=Config.ELASTICSEARCH_INDEX, body=search_body)

    results = []
    for hit in search_results['hits']['hits']:
        result = {
            'id': hit['_id'],
            'title': hit['_source']['title'],
            'content': hit['_source']['content'],
            'highlights': hit['highlight'] if 'highlight' in hit else None
        }
        results.append(result)

    return results

@app.route('/index', methods=['POST'])
def index_data():
    data = request.json
    for item in data:
        es.index(index=Config.ELASTICSEARCH_INDEX, body=item)
    return jsonify({'message': 'Data indexed successfully'})

@app.route('/delete_index', methods=['POST'])
def delete_index():
    es.indices.delete(index=Config.ELASTICSEARCH_INDEX, ignore=[400, 404])
    return jsonify({'message': 'Index deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)