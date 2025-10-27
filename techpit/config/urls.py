from django.contrib import admin
from django.urls import path, include  # includeを追加


urlpatterns = [
    path('management/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
