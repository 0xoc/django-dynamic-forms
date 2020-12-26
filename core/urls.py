from django.urls import path
from core.views.form_views import RetrieveSubFormView, CreateRawSubForm, AddFieldToSubForm, AddElementToField, \
    ElementTypesList, TemplateRetrieveView, CreateFormFromTemplate, CreateTemplateView, ListTemplatesView, FormsIFilled, \
    FormsOfTemplate, UpdateElement, FormRetrieveView, AnswerElementOfForm, DataRUDView, AddDataView, UpdateField, \
    FormsOfUserProfile, FormFilterView, TemplateElementListView, FormsListView, SetElementOrders, SetFieldOrders, \
    ConditionUpdateElement
from core.views.user_profile_views import CreateUserProfileView, MyUserProfileInfo, UserProfileInfo, UserProfileList, \
    AuthToken

urlpatterns = [
    # user profile endpoints
    path('user-profile/create/', CreateUserProfileView.as_view()),
    path('user-profile/my-info/retrieve-update-delete/', MyUserProfileInfo.as_view()),
    path('user-profile/<int:user_profile_id>/retrieve-update-delete/', UserProfileInfo.as_view()),
    path('user-profile/list/', UserProfileList.as_view()),
    path('auth/', AuthToken.as_view()),

    # form endpoints
    path('template/create/', CreateTemplateView.as_view()),
    path('template/<int:template_id>/', TemplateRetrieveView.as_view()),
    path('template/<int:template_id>/elements/list/', TemplateElementListView.as_view()),
    
    path('form/<int:form_id>/', FormRetrieveView.as_view()),
    path('template/<int:template_id>/filter/', FormFilterView.as_view()),

    path('create-form-from-template/', CreateFormFromTemplate.as_view()),
    path('form/<int:form_id>/set-value/<element_type>/<int:element_id>/', AnswerElementOfForm.as_view()),
    path('template/list/', ListTemplatesView.as_view()),

    # form lists
    path('forms-of-template/<int:template_id>/', FormsOfTemplate.as_view()),
    path('forms-of/<int:user_profile_id>/', FormsOfUserProfile.as_view()),
    path('forms-I-filled/list/', FormsIFilled.as_view()),

    # list of all forms
    path('forms/list/', FormsListView.as_view()),

    # sub-form endpoints
    path('sub-form/create/', CreateRawSubForm.as_view()),
    path('sub-form/<int:sub_form_id>/', RetrieveSubFormView.as_view()),

    # field/element endpoints
    path('field/create/', AddFieldToSubForm.as_view()),  # create field for todo: template
    path('field/<int:field_id>/', UpdateField.as_view()),  # update a todo: templates field

    path('element/<element_type>/create/', AddElementToField.as_view()),  # create element for todo: template
    path('element/<element_type>/<int:element_id>/update-retrieve/', UpdateElement.as_view()),
    path('element/<element_type>/<int:element_id>/condition/update/', ConditionUpdateElement.as_view()),
    path('element/<element_type>/<int:element_id>/add/data/', AddDataView.as_view()),
    path('data/<int:data_id>/', DataRUDView.as_view()),
    path('element-types/list/', ElementTypesList.as_view()),

    path('set-element-orders/', SetElementOrders.as_view()),
    path('set-field-orders/', SetFieldOrders.as_view()),



]
