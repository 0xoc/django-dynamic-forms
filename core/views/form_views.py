from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    ListAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.element_types import element_types
from core.permissions import IsLoggedIn, IsSuperuser
from core.serializers.FormSerializers.create_serializers import SubFormRawCreateSerializer, FieldRawCreateSerializer, \
    TemplateRawCreateSerializer
from core.serializers.FormSerializers.retreive_serializers import SubFormRetrieveSerializer, TemplateRetrieveSerializer, \
    FormRetrieveSerializer
from core.serializers.FormSerializers.create_serializers import create_serializers
from core.models import SubForm, Template, elements, Form
from django_filters.rest_framework import DjangoFilterBackend


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


class CreateFormFromTemplate(CreateModelMixin, APIView):
    """Create a new form from the given template form,
    and set the filler to the currently logged in user"""
    permission_classes = [IsLoggedIn, ]

    def create(self, request, *args, **kwargs):
        # get template form
        template = get_object_or_404(Template, pk=kwargs.get('template_id'))
        user_profile = request.user.user_profile

        # create a new form and set filler
        form = template.create_filling_form()
        form.filler = user_profile
        form.save()

        form_data = TemplateRetrieveSerializer(instance=form).data

        return Response(form_data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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

    def get_queryset(self):
        return Template.objects.filter(base_template=None)


class FormsOfTemplate(ListAPIView):
    """List All Forms from the given template"""
    permission_classes = [IsLoggedIn, IsSuperuser]
    serializer_class = TemplateRetrieveSerializer
    filter_backends = [DjangoFilterBackend, ]

    filterset_fields = ['filler', ]

    def get_queryset(self):
        return Template.objects.filter(base_template__pk=self.kwargs.get('template_id'))


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
    permission_classes = [IsAuthenticated, ]
    serializer_class = FieldRawCreateSerializer


class AddElementToField(CreateAPIView):
    """ Add a field to sub form """
    permission_classes = [IsLoggedIn, ]

    def get_serializer_class(self):
        """Get serializer based on filed type"""
        _element_type = self.kwargs.get('element_type')
        return create_serializers.get(_element_type, None)


class UpdateElement(RetrieveUpdateDestroyAPIView):
    """ Add a field to sub form """
    permission_classes = [IsLoggedIn, ]

    def get_serializer_class(self):
        """Get serializer based on filed type"""
        _element_type = self.kwargs.get('element_type')

        return create_serializers.get(_element_type, None)

    def get_object(self):
        return get_object_or_404(elements.get(self.kwargs.get('element_type')),
                                 pk=self.kwargs.get('element_id'))


class ElementTypesList(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        return Response(element_types)
