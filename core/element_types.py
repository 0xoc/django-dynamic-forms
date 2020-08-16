from django.utils.translation import gettext as _

"""
INPUT -> {}
SELECT -> {
 [ { VALUE, DISPLAY}, ...  ]
}
RADIO -> {
    [ { VALUE, DISPLAY } ]
}
CHECKBOX -> {
 [ { VALUE, DISPLAY } ]
}
DATE
TIME
DATETIME
RANGE
"""

INPUT = "input"
SELECT = "select"
RADIO = "radio"
CHECKBOX = "checkbox"
DATE = "date"
INT = "int"
FLOAT = "float"
TIME = "time"
DATETIME = "datetime"
RANGE = "range"

element_types = ((INPUT, _("Input")),
                 (SELECT, _("Select")),
                 (RADIO, _("Radio")),
                 (CHECKBOX, _("Checkbox")),
                 (DATE, _("Date")),
                 (TIME, _("Time")),
                 (DATETIME, _("Datetime")),
                 (RANGE, _("Range")),
                 (INT, _("int")),
                 (FLOAT, _("FLOAT")))


element_types_list = [e[0] for e in element_types]
