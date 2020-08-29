def get_related_attrs(field, base_name="elements"):
    """ return a list of related fields (inputs, selects, ...) of the given sub_form """
    attrs = []
    for attr in field.__dir__():
        if attr.startswith(base_name):
            attrs += getattr(field, attr).all()

    return sorted(attrs, key=lambda x: x.order)
