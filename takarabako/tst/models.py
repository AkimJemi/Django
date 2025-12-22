from django.db import models


class ExecuteLine(models.Model):
    TYPE_MACRO = 1
    TYPE_SQL = 2
    TYPE_REGEX = 3
    TYPE_CHOICES = [
        (TYPE_MACRO, 'マクロ'),
        (TYPE_SQL, 'SQL'),
        (TYPE_REGEX, '正規表現'),
    ]

    OUTPUT_TYPE_OUTPUT = 1
    OUTPUT_TYPE_EXECUTE = 2
    OUTPUT_TYPE_BOTH = 3
    OUTPUT_TYPE_CHOICES = [
        (OUTPUT_TYPE_OUTPUT, '出力のみ'),
        (OUTPUT_TYPE_EXECUTE, '実行のみ'),
        (OUTPUT_TYPE_BOTH, '出力と実行'),
    ]

    USER_ADMIN = 1
    USER_GENERAL = 2
    USER_PUBLIC = 3
    USER_CHOICES = [
        (USER_ADMIN, '管理者'),
        (USER_GENERAL, 'ユーザー'),
        (USER_PUBLIC, '公開'),
    ]

    no = models.AutoField(
        verbose_name="番号",
        primary_key=True
    )

    type = models.IntegerField(
        verbose_name="タイプ",
        choices=TYPE_CHOICES,
        default=TYPE_MACRO
    )

    output_type = models.IntegerField(
        verbose_name="出力タイプ",
        choices=OUTPUT_TYPE_CHOICES,
        default=OUTPUT_TYPE_OUTPUT
    )

    is_available = models.BooleanField(
        verbose_name="利用可能フラグ",
        default=True
    )

    available_user = models.IntegerField(
        verbose_name="利用可能ユーザー区分",
        choices=USER_CHOICES,
        default=USER_GENERAL
    )

    line = models.TextField(
        verbose_name="実行内容"
    )

    line2 = models.TextField(
        verbose_name="実行内容2"
    )
    create_date = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True
    )

    update_date = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True
    )

    class Meta:
        db_table = "execute_line"
        verbose_name = "実行ライン"
        verbose_name_plural = "実行ライン"
        ordering = ['-create_date']

    def __str__(self):
        return f"Line #{self.no}: {self.get_type_display()} - {self.line[:50]}..."
