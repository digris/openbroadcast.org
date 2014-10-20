from modeltranslation.translator import translator, TranslationOptions
from alibrary.models import Season, Weather

class SeasonTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Season, SeasonTranslationOptions)

class WeatherTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Weather, WeatherTranslationOptions)