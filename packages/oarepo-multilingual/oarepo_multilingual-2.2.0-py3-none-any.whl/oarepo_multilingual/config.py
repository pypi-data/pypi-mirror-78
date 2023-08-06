"""Multilingual extension default configuration."""


ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE = {
    "type": "text",
    "fields": {
        "keywords": {
            "type": "keyword"
        }
    }
}
