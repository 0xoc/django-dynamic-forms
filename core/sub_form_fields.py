
def get_related_elements(field):

    """ return a list of related fields (inputs, selects, ...) of the given sub_form """
    _elements = []
    for attr in field.__dir__():
        if attr.startswith("elements"):
            _elements += getattr(field, attr).all()

    return _elements
