
from django.urls import path
from .views import index, IndexView    # IndexViewを追加
from .views import BlogListView, BlogCreateView, create_done  #修正
app_name = 'blog'  # 追加


urlpatterns = [
    path('index', index, name="index"),
    path('index_class', IndexView.as_view(), name="index_class"),  # 追加するコード
    path('', BlogListView.as_view(), name="blog_list"),  # 追加
    path('create/', BlogCreateView.as_view(), name='create'),  # 追加
    path('create_done/', create_done, name='create_done'),
]
