from django.shortcuts import render
import pandas as pd

# Create your views here.
def get_sample_data():
    SAMPLE_FILE = "assets/data_prueba_tecnica 1.csv"
    return pd.read_csv(SAMPLE_FILE)


def get_name_values(data):
    return data['name'].unique()


def get_status_values(data):
    return data['status'].unique()


def get_company_id_values(data):
    return data['company_id'].unique()


def get_company_w_id(data):
    data_dup = data.copy()
    data_dup.drop("id", axis=1, inplace=True)
    data_dup.drop("amount", axis=1, inplace=True)
    data_dup.drop("status", axis=1, inplace=True)
    data_dup.drop("created_at", axis=1, inplace=True)
    data_dup.drop("paid_at", axis=1, inplace=True)
    data_dup.drop_duplicates(inplace=True)
    return data_dup

