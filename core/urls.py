from django.urls import path

from core.views.form_views import RetrieveSubFormView, CreateRawSubForm, AddFieldToSubForm, AddElementToField, \
    ElementTypesList
from core.views.user_profile_views import CreateUserProfileView

urlpatterns = [
    path('user-profile/create/', CreateUserProfileView.as_view()),
    path('sub-form/<int:sub_form_id>/', RetrieveSubFormView.as_view()),
    path('sub-form/create/', CreateRawSubForm.as_view()),
    path('add-field/', AddFieldToSubForm.as_view()),
    path('add-element/<element_type>/', AddElementToField.as_view()),
    path('element-types/list/', ElementTypesList.as_view())

]
