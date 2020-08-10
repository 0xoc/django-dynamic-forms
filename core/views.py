from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import SubForm
from core.serializers.create_serializers import SubFormRawCreateSerializer
from .serializers.retreive_serializers import SubFormRetrieveSerializer


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
