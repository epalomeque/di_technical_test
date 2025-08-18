import pandas as pd
from django.shortcuts import render
from data.models import Sales
from data.views import (get_sample_data, get_name_values,
                        get_status_values, get_company_id_values,
                        get_company_w_id, get_columns_values, get_data_shape,
                        filter_nan_in_names, save_full_dataset,
                        filter_nan_in_created_at, filter_nan_in_paid_at,
                        clean_dataframe, save_full_dataset_bulk)

# Create your views here.
def home(request):
    return render(request, 'indice.html', {})


def section_1(request):
    return render(request, 'section_1.html',{})


def display_table(request):
    sales_df = get_sample_data()
    df_context = create_df_context(sales_df)

    return render(request,
                  'display_table.html',
                  df_context)


def save_to_db(request):
    total_in_db = Sales.objects.count()
    sales_df = get_sample_data()
    clean_sales = clean_dataframe(sales_df)
    total_in_csv = get_data_shape(clean_sales).get('rows')
    if not(total_in_db == total_in_csv):
        Sales.objects.all().delete()
        save_full_dataset_bulk(clean_sales)

    list_status = Sales.objects.values_list('status', flat=True)
    list_company = Sales.objects.values_list('company_name', 'company_id')
    print(list_company)

    df_context = {
        "total_records": total_in_db,
        "column_names": Sales._meta.get_fields(),
        "status_values": set(list_status),
        "company_w_id": set(list_company),
    }
    return render(request,
                  'display_db_raw.html',
                  df_context)


def save_new_tables(request):
    sales_df = get_sample_data()
    pass

"""
context_functions
"""
def create_df_context(df: pd.DataFrame) -> dict :
    return dict(
        html_table = df.head().to_html(),
        name_values = get_name_values(df),
        status_values = get_status_values(df),
        column_names = get_columns_values(df),
        company_id_values = get_company_id_values(df),
        company_w_id = get_company_w_id(df),
        company_w_id_table = get_company_w_id(df).to_html(),
        nan_in_names = filter_nan_in_names(df).to_html(),
        nan_in_created = filter_nan_in_created_at(df).to_html(),
        nan_in_paid = filter_nan_in_paid_at(df).to_html(),
        shape_data = get_data_shape(df),
        # column_types = df.dtypes
    )
