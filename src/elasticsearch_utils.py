from elasticsearch import Elasticsearch, exceptions as es_exceptions
from elasticsearch.helpers import bulk
import yaml
import logging
import time

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

def create_es_client(retries=3, delay=5):
    for attempt in range(retries):
        try:
            es = Elasticsearch(
                [{'host': config['host'], 'port': config['port'], 'scheme': config['scheme']}]
            )
            if es.ping():
                logger.info("Connected to Elasticsearch")
                return es
            else:
                raise es_exceptions.ConnectionError("Elasticsearch ping failed")
        except es_exceptions.ConnectionError as e:
            logger.error(f"Connection attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise es_exceptions.ConnectionError("All connection attempts to Elasticsearch failed")

es = create_es_client()

def index_document(text, doc_id):
    try:
        es.index(index=config['index'], id=doc_id, document={"text": text})
        logger.info(f"Indexed document {doc_id}")
    except es_exceptions.ElasticsearchException as e:
        logger.error(f"Error indexing document {doc_id}: {e}")
        raise

def index_documents(texts):
    try:
        actions = [
            {
                "_index": config['index'],
                "_id": i,
                "_source": {"text": text},
            }
            for i, text in enumerate(texts)
        ]
        bulk(es, actions)
        logger.info("Bulk indexing completed")
    except es_exceptions.ElasticsearchException as e:
        logger.error(f"Error bulk indexing documents: {e}")
        raise
