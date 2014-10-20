import autocomplete_light

from models import Artist

class ArtistAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name',]
autocomplete_light.register(Artist, ArtistAutocomplete)