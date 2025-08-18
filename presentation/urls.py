from django.urls import path
from . import views

urlpatterns = [
    path('', views.section_1, name='section_1'),
    path('data_analysis/', views.display_table, name='display_analysis'),
    path('save_to_db/', views.save_to_db, name='save_to_db'),
    path('create_tables/', views.save_new_tables, name='create_tables'),
    path('create_views/', views.create_views, name='create_views'),

]