DAY_CHOICES = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday")
)

BITWISE_DAY_CHOICES = (
    (1, "Su","Sunday"),
    (2, "M","Monday"),
    (4, "Tu","Tuesday"),
    (8, "W","Wednesday"),
    (16, "Th","Thursday"),
    (32, "F","Friday"),
    (64, "Sa","Saturday"),
)

ADVANCED_DAY_CHOICES = (
    (None, "Any day"),
    ("0,1,2,3,4", "Weekdays"),
    ("5,6", "Weekends"),
) + DAY_CHOICES