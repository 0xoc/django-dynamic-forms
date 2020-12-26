abstract_base_fields = ['pk', 'title', 'type', 'filters', 'order']
base_fields = abstract_base_fields + ['value', ]
base_field_fields_simple = ['pk', 'title', 'order', 'is_grid',
                            'condition_element_type',
                            'condition_element_pk',
                            'condition_element_value',
                            ]
base_field_fields = base_field_fields_simple + ['elements', ]
abstract_element_fields = ['pk', 'title', 'type', 'order',
                           'condition_element_type',
                           'condition_element_pk',
                           'condition_element_value',
                           'field', 'data', 'disabled']
