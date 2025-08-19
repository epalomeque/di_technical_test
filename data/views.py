import pandas as pd
import numpy as np
import re
import hashlib
from data.constants import (COMPANY_ID_MAX_LENGTH, ColumnName, SAMPLE_FILE,
                            DELETE_STR, UNVALID_HEX_STR, DATEFORMAT, DEFAULT_DATE_STR, REMOVE_TIME_STR,
                            REGEX_DATE_FORMAT, STATUS_PAID_ERROR, STATUS_PAID)
from data.models import Sales, Charges, Companies


# Create your views here.
def get_sample_data(data_file: str = SAMPLE_FILE) -> pd.DataFrame:
    return pd.read_csv(data_file)


def get_sample_data_cleaned() -> pd.DataFrame:
    data = get_sample_data()
    return clean_dataframe(data)


def get_columns_values(data: pd.DataFrame):
    return data.columns


def get_name_values(data: pd.DataFrame):
    return data[ColumnName.NAME].unique()


def get_status_values(data: pd.DataFrame):
    return data[ColumnName.STATUS].unique()


def get_company_id_values(data: pd.DataFrame):
    return data[ColumnName.COMPANY_ID].unique()


def get_company_w_id(data: pd.DataFrame) -> pd.DataFrame:
    data_dup = data.copy()
    data_dup.drop(ColumnName.ID, axis=1, inplace=True)
    data_dup.drop(ColumnName.AMOUNT, axis=1, inplace=True)
    data_dup.drop(ColumnName.STATUS, axis=1, inplace=True)
    data_dup.drop(ColumnName.CREATED_AT, axis=1, inplace=True)
    data_dup.drop(ColumnName.PAID_AT, axis=1, inplace=True)
    data_dup.drop_duplicates(inplace=True)
    return data_dup


def get_data_shape(data):
    shape = data.shape
    return {"rows": shape[0], "columns": shape[1]}


def get_info(data):
    return data.info()


def is_valid_company_id(company_id:str) -> bool:
    if company_id is not None and type(company_id) is str:
        valid_len = len(company_id) == COMPANY_ID_MAX_LENGTH
        return valid_len and company_id.isalnum()
    return False

""" 
FILTER FUNCTIONS 
"""
def filter_nan_in_names(data):
    filtered_df = data[data[ColumnName.NAME].isna()]
    return filtered_df


def filter_nan_in_company_id(data):
    filtered_df = data[data[ColumnName.COMPANY_ID].isna()]
    return filtered_df


def filter_nan_in_id(data):
    filtered_df = data[data[ColumnName.ID].isna()]
    return filtered_df


def filter_nan_in_amount(data):
    filtered_df = data[data[ColumnName.AMOUNT].isna()]
    return filtered_df


def filter_nan_in_status(data):
    filtered_df = data[data[ColumnName.STATUS].isna()]
    return filtered_df


def filter_nan_in_created_at(data):
    filtered_df = data[data[ColumnName.CREATED_AT].isna()]
    return filtered_df


def filter_nan_in_paid_at(data):
    filtered_df = data[data[ColumnName.PAID_AT].isna()]
    return filtered_df


""" 
DATA TRANSFORM FUNCTIONS 
"""
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    # Clean name and company_id columns
    new_df = clean_name_and_company_id(new_df)
    # Clean date columns
    new_df = clean_date_columns(new_df)
    # Clean id column
    new_df = clean_id_column(new_df)
    # Clean Status column
    new_df = clean_status_column(new_df)
    # Clean Amount column
    new_df = clean_amount_column(new_df)

    new_df = new_df.astype({
        ColumnName.NAME: str,
        ColumnName.COMPANY_ID: str,
        ColumnName.AMOUNT: np.float32,
    })
    return new_df


def clean_company_id(company_id: str) -> str:
    if is_valid_company_id(company_id):
        return company_id
    return DELETE_STR


def clean_name(name: str) -> str:
    if name is not None and type(name) is str:
        name = name.strip()
        if len(name) == 0:
            return DELETE_STR
        if UNVALID_HEX_STR in name:
            return DELETE_STR
        return name
    return DELETE_STR


def clean_date(date_str: str) -> str:
    if date_str is not None and type(date_str) is str:
        date_str = date_str.replace(REMOVE_TIME_STR, '')
        regex_str = re.search(REGEX_DATE_FORMAT, date_str)
        if regex_str is None:
            if len(date_str) == 8 and date_str.isnumeric():
                return date_str[0:4] + '-' + date_str[4:6] + '-' + date_str[6:]
            return DEFAULT_DATE_STR
        return date_str.strip()
    return DEFAULT_DATE_STR


def clean_name_and_company_id(df: pd.DataFrame) -> pd.DataFrame:
    df[ColumnName.COMPANY_ID] = df[ColumnName.COMPANY_ID].apply(lambda x: clean_company_id(x))
    df[ColumnName.NAME] = df[ColumnName.NAME].apply(lambda x: clean_name(x))
    company_name_pairs = get_company_w_id(df)
    company_name_pairs = company_name_pairs[company_name_pairs.name != DELETE_STR]
    company_name_pairs = company_name_pairs[company_name_pairs.company_id != DELETE_STR]

    for data in company_name_pairs.values:
        pairs_name, pairs_company_id = data[0], data[1]
        df.loc[(df[ColumnName.NAME] == DELETE_STR) & (df[ColumnName.COMPANY_ID] == pairs_company_id),
            ColumnName.NAME] = pairs_name
        df.loc[(df[ColumnName.NAME] == pairs_name) & (df[ColumnName.COMPANY_ID] == DELETE_STR),
            ColumnName.COMPANY_ID] = pairs_company_id

    return df


def clean_date_columns(df:pd.DataFrame) -> pd.DataFrame:
    df[ColumnName.CREATED_AT] = df[ColumnName.CREATED_AT].apply(lambda x: clean_date(x))
    df[ColumnName.CREATED_AT] = pd.to_datetime(df[ColumnName.CREATED_AT], format=DATEFORMAT)

    df[ColumnName.PAID_AT] = df[ColumnName.PAID_AT].apply(lambda x: clean_date(x))
    df[ColumnName.PAID_AT] = pd.to_datetime(df[ColumnName.PAID_AT], format=DATEFORMAT)
    return df


def create_new_id() -> str:
    import uuid
    new_UUID_str = str(uuid.uuid4())
    return hashlib.sha1(new_UUID_str.encode("UTF-8")).hexdigest()[:25]


def clean_id(id: str) -> str:
    if id is not None and type(id) is str:
        return id
    return create_new_id()


def clean_id_column(df: pd.DataFrame) -> pd.DataFrame:
    df[ColumnName.ID] = df[ColumnName.ID].apply(lambda x: clean_id(x))
    return df


def clean_status(status: str) -> str:
    if status is not None and type(status) is str:
        if status == STATUS_PAID_ERROR:
            return STATUS_PAID
    return status


def clean_status_column(df: pd.DataFrame) -> pd.DataFrame:
    df[ColumnName.STATUS] = df[ColumnName.STATUS].apply(lambda x: clean_status(x))
    return df


def clean_amount(amount: float) -> float:
    if amount is not None and type(amount) is float:
        formated_amount = "%.2f" % amount
        return float(formated_amount)
    return 0.0


def clean_amount_column(df: pd.DataFrame) -> pd.DataFrame:
    df[ColumnName.AMOUNT] = df[ColumnName.AMOUNT].apply(lambda x: clean_amount(x))
    return df

"""
DB FUNCTIONS
"""

def save_full_dataset(data: pd.DataFrame):
    # Convert the DataFrame to Django Model instances and save them
    for index, row in data.iterrows():
        Sales.objects.create(
            id = row[ColumnName.ID],
            company_name = row[ColumnName.NAME],
            company_id = row[ColumnName.COMPANY_ID],
            amount = row[ColumnName.AMOUNT],
            status = row[ColumnName.STATUS],
            created_at = row[ColumnName.CREATED_AT],
            updated_at = row[ColumnName.PAID_AT]
        )


def save_full_dataset_bulk(data: pd.DataFrame):
    # Convert the DataFrame to Django Model instances and save them in one step
    Sales.objects.bulk_create([
        Sales(
            id=row[ColumnName.ID],
            company_name=row[ColumnName.NAME],
            company_id=row[ColumnName.COMPANY_ID],
            amount=row[ColumnName.AMOUNT],
            status=row[ColumnName.STATUS],
            created_at=row[ColumnName.CREATED_AT],
            updated_at=row[ColumnName.PAID_AT]
        ) for _, row in data.iterrows()
    ])


def save_companies(data: set) -> None:
    if len(data) > 0:
        Companies.objects.all().delete()
        # Convert the DataFrame to Companies Model instances and save them
        for row in data:
            Companies.objects.create(
                    id = row[1],
                    company_name = row[0]
            )


def save_charges(data:pd.DataFrame) -> None:
    total_in_charges = Charges.objects.all().count()
    if total_in_charges <= 0:
        Charges.objects.bulk_create([
            Charges(
                id=row[ColumnName.ID],
                company_id=row[ColumnName.COMPANY_ID],
                amount=row[ColumnName.AMOUNT],
                status=row[ColumnName.STATUS],
                created_at=row[ColumnName.CREATED_AT],
                updated_at=row[ColumnName.PAID_AT]
            ) for _, row in data.iterrows()
        ])


def create_db_views() -> None:
    from django.db import connection
    from data.sql_raw import SQL_DAYLI_CHARGES_VIEW, DROP_DAYLI_CHARGES_VIEW

    with connection.cursor() as cursor:
        cursor.execute(DROP_DAYLI_CHARGES_VIEW)
        cursor.execute(SQL_DAYLI_CHARGES_VIEW)
