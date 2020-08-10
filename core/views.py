from rest_framework.exceptions import APIException, ValidationError, ParseError
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext as _
from core.serializers.create_serializers import SubFormRawCreateSerializer
from .serializers.retreive_serializers import SubFormRetrieveSerializer
from .serializers.create_serializers import create_serializers
from .models import SubForm
from rest_framework import serializers

class RetrieveSubFormView(RetrieveAPIView):
    """Retrieve basic sub form info with fields data"""
    serializer_class = SubFormRetrieveSerializer
    queryset = SubForm.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'sub_form_id'


class CreateRawSubForm(CreateAPIView):
    """Create a new sub form with fields"""
    permission_classes = [IsAuthenticated, ]
    serializer_class = SubFormRawCreateSerializer


class AddFieldToSubForm(CreateAPIView):
    """ Add a field to sub form """
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        """Get serializer based on filed type"""
        _element_type = self.kwargs.get('element_type')

        return create_serializers.get(_element_type, None)
