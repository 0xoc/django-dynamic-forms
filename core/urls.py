from django.urls import path
from core.views.form_views import RetrieveSubFormView, CreateRawSubForm, AddFieldToSubForm, AddElementToField, \
    ElementTypesList, TemplateRetrieveView, CreateFormFromTemplate, CreateTemplateView, ListTemplatesView, FormsIFilled, \
    FormsOfTemplate, UpdateElement
from core.views.user_profile_views import CreateUserProfileView, MyUserProfileInfo, UserProfileInfo, UserProfileList

urlpatterns = [
    # user profile endpoints
    path('user-profile/create/', CreateUserProfileView.as_view()),
    path('user-profile/my-info/retrieve-update-delete/', MyUserProfileInfo.as_view()),
    path('user-profile/<int:user_profile_id>/retrieve-update-delete/', UserProfileInfo.as_view()),
    path('user-profile/list/', UserProfileList.as_view()),

    # form endpoints
    path('template/create/', CreateTemplateView.as_view()),
    path('template/<int:template_id>/', TemplateRetrieveView.as_view()),
    path('form/<int:template_id>/', TemplateRetrieveView.as_view()),    # redundant
    path('create-form-from-template/<int:template_id>/', CreateFormFromTemplate.as_view()),
    path('template/list/', ListTemplatesView.as_view()),

    # form lists
    path('forms-of-template/<int:template_id>/', FormsOfTemplate.as_view()),
    path('forms-I-filled/list/', FormsIFilled.as_view()),

    # sub-form endpoints
    path('sub-form/<int:sub_form_id>/', RetrieveSubFormView.as_view()),
    path('sub-form/create/', CreateRawSubForm.as_view()),

    # field/element endpoints
    path('add-field/', AddFieldToSubForm.as_view()),
    path('field/<int:field_id>/', AddFieldToSubForm.as_view()),

    path('add-element/<element_type>/', AddElementToField.as_view()),
    path('element/<element_type>/<int:element_id>/update-retrieve/', UpdateElement.as_view()),
    path('element-types/list/', ElementTypesList.as_view())

]
