# search index + mapping

reference: https://hackernoon.com/elasticsearch-building-autocomplete-functionality-494fcf81a7cf



    edge_ngram_tokenizer = tokenizer(
        'edge_ngram_tokenizer',
        type='edge_ngram',
        min_gram=1,
        max_gram=12,
        token_chars=['letter']
    )


    keyword_analyzer = analyzer(
        'keyword_analyzer',
        tokenizer="keyword",
        filter=["lowercase", "asciifolding", "trim"],
        type='custom',
        char_filter=[]
    )

    edge_ngram_analyzer = analyzer(
        'edge_ngram_analyzer',
        tokenizer=edge_ngram_tokenizer,
        filter=["lowercase"],
    )

    edge_ngram_search_analyzer = analyzer(
        'edge_ngram_search_analyzer',
        tokenizer="lowercase",
    )



    def format_field_for_suggestion(text):
        text_list = text.split(' ')
        l = len(text_list)
        final_text_list = [text_list[x:l] for x in range(l)]
        final_text = [' '.join(x).lower() for x in final_text_list]
        return final_text




    # class BaseDocType(DocType):
    #     pass
    #


    @label_index.doc_type
    class LabelDocument(DocType):

        class Meta:
            model = Label
            queryset_pagination = 1000
            doc_type = 'alibrary.label'

        name = fields.TextField(
            analyzer='standard',
            fields={
                'keywordstring': {
                    'type': 'text',
                    'analyzer': keyword_analyzer
                },
                'edgengram': {
                    'type': 'text',
                    'analyzer': edge_ngram_analyzer,
                    'search_analyzer': edge_ngram_search_analyzer,
                },
                'completion': {
                    'type': 'completion',
                },
            }
        )

        country = KeywordField(
            attr='country.iso2_code'
        )

        def prepare_name(self, instance):
            return instance.name.strip()
    #        return format_field_for_suggestion(instance.name.strip())

        def get_queryset(self):
            return super(LabelDocument, self).get_queryset().select_related(
                'country'
            )
