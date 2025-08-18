import pandas as pd
from django.shortcuts import render
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
    clean_sales = clean_dataframe(sales_df)
    df_context = create_df_context(clean_sales)

    return render(request,
                  'display_table.html',
                  df_context)

def save_to_db(request):
    sales_df = get_sample_data()
    clean_sales = clean_dataframe(sales_df)
    save_full_dataset_bulk(clean_sales)
    df_context = create_df_context(clean_sales)
    return render(request,
                  'display_table.html',
                  df_context)


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
