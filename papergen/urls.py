from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_paper_view, name='generate_paper'),
    path('download-pdf/', views.download_paper_pdf, name='download_paper_pdf'),
]