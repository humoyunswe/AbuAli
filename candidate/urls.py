from django.urls import path
from .views import contact_to_us, joing_to_us

urlpatterns = [
    path('contact_to_us/', contact_to_us, name='contact_to_us'),
    path('join/', joing_to_us, name='joing_to_us'),
]