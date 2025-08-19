from dataclasses import dataclass
from unittest.mock import DEFAULT

SAMPLE_FILE = "assets/data_prueba_tecnica 1.csv"

@dataclass(frozen=True)
class ColumnName:
    ID = "id"
    NAME = "name"
    COMPANY_ID = "company_id"
    AMOUNT = "amount"
    STATUS = "status"
    CREATED_AT = "created_at"
    PAID_AT = "paid_at"

DELETE_STR = "to_delete"

DEFAULT_DATE_STR = "1900-01-01"

REMOVE_TIME_STR = "T00:00:00"

UNVALID_HEX_STR = "0xFFFF"

COMPANY_ID_MAX_LENGTH = 40

REGEX_DATE_FORMAT = r"^\d{4}-\d{2}-\d{2}$"

# 2019-03-19
DATEFORMAT = "%Y-%m-%d"

# status
STATUS_PAID_ERROR ="p&0x3fid"

STATUS_PAID = "paid"