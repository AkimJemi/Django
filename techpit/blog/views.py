from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView  # 追加
from .models import Blog, Category  # 追加
from . forms import BlogForm  # 追加
from django.urls import reverse_lazy  # 追加
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


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    model = Blog
    queryset = Blog.objects.all()
    # ここから下を追加

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class BlogCreateView(CreateView):

    model = Blog
    form_class = BlogForm
    # 登録処理が正常終了した場合の遷移先を指定
    success_url = reverse_lazy('blog:create_done')
    # ここから下を追加

    def get_context_data(self, **kwargs):
        context = super(BlogCreateView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


def create_done(request):
    category_list = Category.objects.all()  # 追加
    return render(request, 'blog/create_done.html', {
        'category_list': category_list})  # category_listを追加
