import requests

items = [
    "Spider-Man: Homecoming",
    "Ant-man and the Wasp",
    "Avengers: Infinity War Part 2",
    "Captain Marvel",
    "Black Panther",
    "Avengers: Infinity War",
    "Thor: Ragnarok",
    "Guardians of the Galaxy Vol 2",
    "Doctor Strange",
    "Captain America: Civil War",
    "Ant-Man",
    "Avengers: Age of Ultron",
    "Guardians of the Galaxy",
    "Captain America: The Winter Soldier",
    "Thor: The Dark World",
    "Iron Man 3",
    "Marvel's The Avengers",
    "Captain America: The First Avenger",
    "Thor",
    "Iron Man 2",
    "The Incredible Hulk",
    "Iron Man",
]


def format_field_for_suggestion(text):
    text_list = text.split(" ")
    l = len(text_list)
    final_text_list = [text_list[x:l] for x in range(l)]
    final_text = [" ".join(x).lower() for x in final_text_list]
    return final_text


r = requests.delete("http://localhost:9201/movies")

payload = {
    "settings": {
        "index": {
            "analysis": {
                "filter": {},
                "analyzer": {
                    "keyword_analyzer": {
                        "filter": ["lowercase", "asciifolding", "trim"],
                        "char_filter": [],
                        "type": "custom",
                        "tokenizer": "keyword",
                    },
                    "edge_ngram_analyzer": {
                        "filter": ["lowercase"],
                        "tokenizer": "edge_ngram_tokenizer",
                    },
                    "edge_ngram_search_analyzer": {"tokenizer": "lowercase"},
                },
                "tokenizer": {
                    "edge_ngram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 5,
                        "token_chars": ["letter"],
                    }
                },
            }
        }
    },
    "mappings": {
        "marvels": {
            "properties": {
                "name": {
                    "type": "text",
                    "fields": {
                        "keywordstring": {
                            "type": "text",
                            "analyzer": "keyword_analyzer",
                        },
                        "edgengram": {
                            "type": "text",
                            "analyzer": "edge_ngram_analyzer",
                            "search_analyzer": "edge_ngram_search_analyzer",
                        },
                        "completion": {"type": "completion"},
                    },
                    "analyzer": "standard",
                }
            }
        }
    },
}

r = requests.put("http://localhost:9201/movies", json=payload)

for item in items:
    url = "http://localhost:9201/movies/marvels"

    payload = {
        #'name': format_field_for_suggestion(item),
        "name": item,
        #'foo': 'bar'
    }

    r = requests.post(url, json=payload)
