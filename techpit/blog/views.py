from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

# ----ここから追加----


def index(request):
    # TOP画面を表示する関数
    print("index関数を使ってTOP画面を表示します！")  # 追加するコード
    return render(request, 'blog/index.html')
# ----ここまで追加----


class IndexView(TemplateView):
    # OP画面を表示するクラス
    print("IndexView関数を使ってTOP画面を表示します！")  # 追加するコード
    template_name = 'blog/index.html'  # 追加するコード

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print("IndexViewを使ってTOP画面を表示します！")
        return self.render_to_response(context)
