from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('execute/', ExecuteLineProcessView.as_view(), name='process_line'),
]
