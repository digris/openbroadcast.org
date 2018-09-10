# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from elasticsearch_dsl import analyzer, tokenizer

# autocomplete tokenizer
edge_ngram_tokenizer = tokenizer(
    'edge_ngram_tokenizer',
    type='edge_ngram',
    min_gram=1,
    max_gram=12,
    # TODO: investigate
    token_chars=['letter', 'digit']
)

# keyword_analyzer = analyzer(
#     'keyword_analyzer',
#     tokenizer="keyword",
#     filter=["lowercase", "asciifolding", "trim"],
#     type='custom',
#     char_filter=[]
# )

# autocomplete analyzer
edge_ngram_analyzer = analyzer(
    'edge_ngram_analyzer',
    tokenizer=edge_ngram_tokenizer,
    filter=['lowercase', 'asciifolding'],
)

# autocomplete *search* analyzer
edge_ngram_search_analyzer = analyzer(
    'edge_ngram_search_analyzer',
    tokenizer='lowercase',
)

# asciifolding analyzer
asciifolding_analyzer = analyzer(
    'asciifolding_analyzer',
    tokenizer='standard',
    filter=['lowercase', 'asciifolding'],
)
