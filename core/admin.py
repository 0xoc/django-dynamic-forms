from django.contrib import admin
from .models import *
from .sub_form_fields import get_related_elements
from .element_types import SELECT

admin.site.register(Form)
admin.site.register(SubForm)
admin.site.register(DateTimeElement)
admin.site.register(SelectElement)
admin.site.register(Input)
admin.site.register(Data)
