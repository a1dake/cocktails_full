from django.urls import path

from api.v1.main.main import template_views

urlpatterns = [
    path('legal', template_views.legal_page, name='legal_page'),
    path('offer', template_views.offer_page, name='offer_page'),
]
