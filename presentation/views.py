from django.shortcuts import render
from data.views import (get_sample_data, get_name_values,
                        get_status_values, get_company_id_values,
                        get_company_w_id)

# Create your views here.
def display_table(request):
    sales_df = get_sample_data()

    return render(request,
                  'display_table.html',
                  {'html_table': sales_df.to_html(),
                   'name_values': get_name_values(sales_df),
                   "status_values": get_status_values(sales_df),
                   "company_id_values": get_company_id_values(sales_df),
                   "company_w_id": get_company_w_id(sales_df),
                   "company_w_id_table": get_company_w_id(sales_df).to_html(),
                   })