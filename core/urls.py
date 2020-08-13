from django.urls import path

from core.views.form_views import RetrieveSubFormView, CreateRawSubForm, AddFieldToSubForm, AddElementToField, \
    ElementTypesList, FormRetrieveView
from core.views.user_profile_views import CreateUserProfileView, MyUserProfileInfo, UserProfileInfo

urlpatterns = [
    # user profile endpoints
    path('user-profile/create/', CreateUserProfileView.as_view()),
    path('user-profile/my-info/retrieve-update-delete/', MyUserProfileInfo.as_view()),
    path('user-profile/<int:user_profile_id>/retrieve-update-delete/', UserProfileInfo.as_view()),

    # form endpoints
    path('form/<int:form_id>/', FormRetrieveView.as_view()),

    # sub-form endpoints
    path('sub-form/<int:sub_form_id>/', RetrieveSubFormView.as_view()),
    path('sub-form/create/', CreateRawSubForm.as_view()),

    # field/element endpoints
    path('add-field/', AddFieldToSubForm.as_view()),
    path('add-element/<element_type>/', AddElementToField.as_view()),
    path('element-types/list/', ElementTypesList.as_view())

]
