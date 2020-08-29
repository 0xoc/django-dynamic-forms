import django
from django.contrib import admin
from django.apps import apps
import rest_framework
models = apps.get_models()

for model in models:
    if model == rest_framework.authtoken.models.Token:
        continue
    try:
        admin.site.register(model)
    except:
        pass

