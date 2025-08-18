from django.urls import path
from . import views

urlpatterns = [
    path('', views.section_1, name='section_1'),
    # path('example1/', views.employees_data, name='employees_data'),
    # path('example2/', views.save_employees_data, name='save_employees_data'),
    path('data_analysis/', views.display_table, name='display_analysis'),
    path('save_to_db/', views.save_to_db, name='save_to_db'),
]