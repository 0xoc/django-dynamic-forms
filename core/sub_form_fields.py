from .models import Input, SelectElement, DateTimeElement


class SubFormFields:
    """ Field types and their related names
     used to get all fields of a subForm
     """

    def __init__(self):
        self._fields = []

    def register(self, filedData):
        """
        :param filedData: { 'related_name', FieldType }
        :return: none
        """

        self._fields.append(filedData)

    @property
    def fields(self):
        return self._fields


sub_form_fields = SubFormFields()

# register form fields
sub_form_fields.register({'inputs': Input})
sub_form_fields.register({'date_times': DateTimeElement})
sub_form_fields.register({'selects': SelectElement})
