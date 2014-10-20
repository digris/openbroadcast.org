#-*- coding: utf-8 -*-
from filer.fields.file import AdminFileWidget, AdminFileFormField, FilerFileField
from filer.models import Audio

class AdminAudioWidget(AdminFileWidget):
    pass


class AdminAudioFormField(AdminFileFormField):
    widget = AdminAudioWidget


class FilerAudioField(FilerFileField):
    default_form_class = AdminAudioFormField
    default_model_class = Audio
