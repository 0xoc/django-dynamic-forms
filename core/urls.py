from django.urls import path

from core.views import RetrieveSubFormView

urlpatterns = [
    path('sub-form/<int:sub_form_id>/', RetrieveSubFormView.as_view()),
]