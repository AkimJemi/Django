
from django.urls import path
from .views import index, IndexView    # IndexViewを追加
from .views import BlogListView, BlogCreateView, create_done, BlogDetailView, BlogEditView, edit_done  # 修正
from .views import BlogDeleteView, delete_done, CategoryView, SearchPostView  # 修正

app_name = 'blog'  # 追加


urlpatterns = [
    path('index', index, name="index"),
    path('index_class', IndexView.as_view(), name="index_class"),  # 追加するコード
    path('', BlogListView.as_view(), name="blog_list"),  # 追加
    path('create/', BlogCreateView.as_view(), name='create'),  # 追加
    path('create_done/', create_done, name='create_done'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name="detail"),  # 追加
    path('edit/<int:pk>/', BlogEditView.as_view(), name='edit'),  # 追加
    path('edit_done/', edit_done, name='edit_done'),  # 追加
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),  # 追加
    path('delete_done/', delete_done, name='delete_done'),  # 追加
    path('category/<str:category>/', CategoryView.as_view(), name='category'),  # 追加
    path('search_list/', SearchPostView.as_view(), name='search_list'),  # 追加


]
