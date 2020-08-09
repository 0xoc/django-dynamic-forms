from rest_framework.generics import RetrieveAPIView

from .models import SubForm
from .serializers import SubFormRetrieveSerializer


class RetrieveSubFormView(RetrieveAPIView):
    """Retrieve basic sub form info with fields data"""
    serializer_class = SubFormRetrieveSerializer
    queryset = SubForm.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'sub_form_id'
