from django.urls import path

from core.views import RetrieveSubFormView, CreateRawSubForm, AddFieldToSubFormView

urlpatterns = [
    path('sub-form/<int:sub_form_id>/', RetrieveSubFormView.as_view()),
    path('sub-form/create/', CreateRawSubForm.as_view()),
    path('add-field/', AddFieldToSubFormView.as_view())
]