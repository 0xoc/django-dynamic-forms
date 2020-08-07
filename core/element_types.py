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

INPUT = "000"
SELECT = "001"
RADIO = "010"
CHECKBOX = "011"
DATE = "100"
TIME = "101"
DATETIME = "110"
RANGE = "111"

element_types = ((INPUT, _("Input")),
                 (SELECT, _("Select")),
                 (RADIO, _("Radio")),
                 (CHECKBOX, _("Checkbox")),
                 (DATE, _("Date")),
                 (TIME, _("Time")),
                 (DATETIME, _("Datetime")),
                 (RANGE, _("Range")))
