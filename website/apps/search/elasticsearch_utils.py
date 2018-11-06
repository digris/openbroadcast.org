# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from elasticsearch_dsl import analyzer, tokenizer

# autocomplete tokenizer
edge_ngram_tokenizer = tokenizer(
    'edge_ngram_tokenizer',
    type='edge_ngram',
    min_gram=1,
    max_gram=20,
    token_chars=['letter', 'digit']
)

# autocomplete analyzer
edge_ngram_analyzer = analyzer(
    'edge_ngram_analyzer',
    tokenizer=edge_ngram_tokenizer,
    filter=['lowercase', 'asciifolding'],
)

# autocomplete *search*  tokenizer
edge_ngram_search_tokenizer = tokenizer(
    'edge_ngram_search_tokenizer',
    type='edge_ngram',
    token_chars=['letter', 'digit']
)

search_tokenizer = tokenizer(
    'search_tokenizer',
    type='standard',
    token_chars=['letter', 'digit']
)

# autocomplete *search* analyzer
edge_ngram_search_analyzer = analyzer(
    'edge_ngram_search_analyzer',
    #tokenizer=edge_ngram_search_tokenizer,
    tokenizer=search_tokenizer,
    filter=['lowercase', 'asciifolding'],
    #tokenizer='lowercase',
)
