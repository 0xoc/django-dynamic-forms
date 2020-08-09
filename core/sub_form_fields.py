
def get_related_fields(sub_form):

    """ return a list of related fields (inputs, selects, ...) of the given sub_form """
    _fields = []
    for attr in sub_form.__dir__():
        if attr.startswith("fields"):
            _fields += getattr(sub_form, attr).all()

    return _fields
