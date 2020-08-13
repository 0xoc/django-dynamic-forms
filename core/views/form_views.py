from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsLoggedIn
from core.serializers.FormSerializers.create_serializers import SubFormRawCreateSerializer, FieldRawCreateSerializer
from core.serializers.FormSerializers.retreive_serializers import SubFormRetrieveSerializer
from core.serializers.FormSerializers.create_serializers import create_serializers
from core.models import SubForm


class RetrieveSubFormView(RetrieveAPIView):
    """Retrieve basic sub form info with fields data"""
    serializer_class = SubFormRetrieveSerializer
    queryset = SubForm.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'sub_form_id'


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
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        """Get serializer based on filed type"""
        _element_type = self.kwargs.get('element_type')

        return create_serializers.get(_element_type, None)
