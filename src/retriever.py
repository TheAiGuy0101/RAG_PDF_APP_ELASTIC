from elasticsearch import Elasticsearch
import yaml
import logging

logger = logging.getLogger(__name__)

def get_elasticsearch_config():
    try:
        with open("config/elasticsearch.yml", 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Error loading Elasticsearch config: {e}")
        raise

config = get_elasticsearch_config()

def create_es_client():
    es = Elasticsearch(
        [{'host': config['host'], 'port': config['port'], 'scheme': config['scheme']}]
    )
    return es

es = create_es_client()

def search_documents(query, index=config['index'], size=5):
    try:
        logger.info(f"Searching documents for query: {query}")
        response = es.search(
            index=index,
            body={
                "query": {
                    "match": {
                        "text": query
                    }
                },
                "size": size
            }
        )
        documents = [hit['_source']['text'] for hit in response['hits']['hits']]
        logger.info(f"Found {len(documents)} documents for query: {query}")
        return documents
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise
