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
TEXTAREA = "textarea"
BOOLEAN = "Boolean"
FILE_INPUT = "file_input"


element_types = ((INPUT, _("Input")),
                 (SELECT, _("Select")),
                 (RADIO, _("Radio")),
                 (CHECKBOX, _("Checkbox")),
                 (DATE, _("Date")),
                 (TIME, _("Time")),
                 (DATETIME, _("Datetime")),
                 (INT, _("int")),
                 (FLOAT, _("FLOAT")),
                 (TEXTAREA, _("text area")),
                 (BOOLEAN, _("boolean")),
                 (FILE_INPUT, _("file_input"))
                 )


element_types_list = [e[0] for e in element_types]
