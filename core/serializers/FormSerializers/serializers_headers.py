abstract_base_fields = ['pk', 'title', 'type', 'filters', 'order']
base_fields = abstract_base_fields + ['value', ]
base_field_fields = ['pk', 'title', 'elements', 'order', 'is_grid']
abstract_element_fields = ['pk', 'title', 'type', 'order', 'field', 'data', 'disabled']
