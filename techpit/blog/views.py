from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

# ----ここから追加----


def index(request):
    # TOP画面を表示する関数
    return render(request, 'index.html')
# ----ここまで追加----
