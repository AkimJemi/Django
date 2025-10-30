from django.db import models

# Create your models here.
# ここから下を追加


class Category(models.Model):
    class Meta:
        # テーブル名を指定
        db_table = "category"
        verbose_name = "カテゴリ名"  # 追加
        verbose_name_plural = "カテゴリ名"  # 追加

    # ここから下はテーブルのフィールド名の定義
    category_name = models.CharField(
        verbose_name="カテゴリ名", max_length=100, unique=True)
    category_image = models.ImageField(
        verbose_name="カテゴリ画像", upload_to="images/")
    # ここから下を追加

    def __str__(self):
        return self.category_name
    # ここまでを追加


class Blog(models.Model):
    class Meta:
        db_table = "blog"
        verbose_name = "ブログ記事"  # 追加
        verbose_name_plural = "ブログ記事"  # 追加

    title = models.CharField(verbose_name="タイトル", max_length=100)
    content = models.TextField(verbose_name="内容")
    postdate = models.DateField(verbose_name="投稿日", auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="カテゴリ")

    # ここから下を追加

    def __str__(self):
        return self.title
    # ここまでを追加
