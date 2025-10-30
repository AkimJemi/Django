
from django.urls import path
from .views import index, IndexView    # IndexViewを追加

urlpatterns = [
    path('index', index, name="index"),
    path('index_class', IndexView.as_view(), name="index_class"),  # 追加するコード
]
