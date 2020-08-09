from django.urls import path

from core.views import RetrieveSubFormView, CreateRawSubForm

urlpatterns = [
    path('sub-form/<int:sub_form_id>/', RetrieveSubFormView.as_view()),
    path('sub-form/create/', CreateRawSubForm.as_view())
]