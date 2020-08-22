from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.element_types import element_types
from core.permissions import IsLoggedIn, IsSuperuser
from core.serializers.FormSerializers.common_serializers import CharFieldSerializer
from core.serializers.FormSerializers.create_serializers import SubFormRawCreateSerializer, FieldRawCreateSerializer, \
    TemplateRawCreateSerializer, FormCreateSerializer, get_create_serializer, get_update_serializer, \
    get_set_value_serializer
from core.serializers.FormSerializers.retreive_serializers import SubFormRetrieveSerializer, TemplateRetrieveSerializer, \
    FormRetrieveSerializer, get_retrieve_serializer, FormSimpleRetrieveSerializer
from core.models import SubForm, Template, elements, Form, Field
from django_filters.rest_framework import DjangoFilterBackend

from core.sub_form_fields import get_related_attrs


class RetrieveSubFormView(RetrieveAPIView):
    """Retrieve basic sub form info with fields data"""
    serializer_class = SubFormRetrieveSerializer
    queryset = SubForm.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'sub_form_id'


class TemplateRetrieveView(RetrieveUpdateDestroyAPIView):
    """RUD template"""
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = TemplateRetrieveSerializer
    queryset = Template.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'template_id'


class FormRetrieveView(RetrieveUpdateDestroyAPIView):
    """RUD Form"""
    permission_classes = [IsLoggedIn, ]
    serializer_class = FormRetrieveSerializer
    queryset = Form.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'form_id'


class CreateFormFromTemplate(CreateAPIView):
    """Create a new form from the given template form,
    and set the filler to the currently logged in user"""
    permission_classes = [IsLoggedIn, ]

    serializer_class = FormCreateSerializer

    def perform_create(self, serializer):
        serializer.save(filler=self.request.user.user_profile)


class AnswerElementOfForm(UpdateAPIView):
    """Create a new form from the given template form,
    and set the filler to the currently logged in user"""

    permission_classes = [IsLoggedIn, ]  # todo: add filler

    def get_serializer_class(self):
        """Get serializer based on filed type"""
        return get_set_value_serializer(self.kwargs.get('element_type'))

    def get_object(self):
        kwargs = self.kwargs

        form = get_object_or_404(Form, pk=kwargs.get('form_id'))
        element_id = kwargs.get('element_id')
        element_type = kwargs.get('element_type')

        template = form.template

        # if the given element id refers to the template's element,
        # create an answer for it

        element = elements.get(element_type).objects.get(pk=element_id)

        if not element.answer_of:
            # it is the base base template field

            # element must belong to the same template as forms template
            if element.field.sub_form.template != template:
                return Response({'detail': ['invalid element id']}, status=400)

            # check if there is an answer for this element
            answer_element = elements.get(element_type).objects.filter(form=form, answer_of=element)
            if not answer_element.exists():
                return elements.get(element_type).objects.create(
                    answer_of=element,
                    form=form
                )
            else:
                return answer_element.first()
        else:
            # element itself is the answer
            return element


class CreateTemplateView(CreateAPIView):
    """Create Raw Form As Template"""

    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = TemplateRawCreateSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.user_profile)


class ListTemplatesView(ListAPIView):
    """List All Template Forms"""
    permission_classes = [IsLoggedIn, ]
    serializer_class = TemplateRetrieveSerializer
    queryset = Template.objects.all()


class FormsOfTemplate(ListAPIView):
    """List All Forms from the given template"""
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = FormSimpleRetrieveSerializer
    filter_backends = [DjangoFilterBackend, ]

    filterset_fields = ['filler', ]

    def get_queryset(self):
        return Form.objects.filter(template__pk=self.kwargs.get('template_id'))


class FormsOfUserProfile(ListAPIView):
    """List All Forms from the given template"""
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = FormSimpleRetrieveSerializer
    filter_backends = [DjangoFilterBackend, ]

    filterset_fields = ['filler', ]

    def get_queryset(self):
        return Form.objects.filter(filler__pk=self.kwargs.get('user_profile_id'))


class FormsIFilled(ListAPIView):
    """List All Forms that the currently logged in user filled"""
    permission_classes = [IsLoggedIn, ]
    serializer_class = TemplateRetrieveSerializer
    filter_backends = [DjangoFilterBackend, ]

    filterset_fields = ['base_template', ]

    def get_queryset(self):
        return Template.objects.filter(filler=self.request.user.user_profile)


class CreateRawSubForm(CreateAPIView):
    """Create a new sub form with fields"""
    permission_classes = [IsLoggedIn, ]
    serializer_class = SubFormRawCreateSerializer


class AddFieldToSubForm(CreateAPIView):
    """ Add a field to sub form """
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = FieldRawCreateSerializer


class UpdateField(RetrieveUpdateDestroyAPIView):
    """ Add a field to sub form """
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = FieldRawCreateSerializer
    queryset = Field.objects.all()

    lookup_url_kwarg = 'field_id'
    lookup_field = 'pk'


class AddElementToField(CreateAPIView):
    """ Add a field to sub form """
    permission_classes = [IsLoggedIn, IsSuperuser]

    def get_serializer_class(self):
        """Get serializer based on filed type"""
        return get_create_serializer(self.kwargs.get('element_type'))


class UpdateElement(RetrieveUpdateDestroyAPIView):
    """ Add a field to sub form """
    permission_classes = [IsLoggedIn, IsSuperuser]

    def get_serializer_class(self):
        """Get serializer based on filed type"""
        return get_update_serializer(self.kwargs.get('element_type'))

    def get_object(self):
        return get_object_or_404(elements.get(self.kwargs.get('element_type')),
                                 pk=self.kwargs.get('element_id'))


class AddDataView(CreateAPIView):
    """ Add a data to element"""
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = CharFieldSerializer

    def perform_create(self, serializer):
        data = serializer.save()

        # add to element
        element = get_object_or_404(elements.get(self.kwargs.get('element_type')),
                                    pk=self.kwargs.get('element_id'))
        element.data.add(data)


class DataRUDView(RetrieveUpdateAPIView):
    """RUD data"""
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = CharFieldSerializer


class ElementTypesList(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        return Response(element_types)
