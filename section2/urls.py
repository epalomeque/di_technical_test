from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_section_2, name='display_section_2'),
    path('<int:num_to_extract>', views.display_section_2, name='display_section_2_extract'),
]