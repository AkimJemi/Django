from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
# JsonResponse を追加し、HttpResponse は不要
from django.http import JsonResponse
from .models import ExecuteLine
from .utils import execute_code_in_file, update_execute_line
# Ajax化により retrieve_and_clean_session_result は不要になりましたが、
# 必要に応じて utils.py のクリーンアップを行うため、execute_code_in_file のみ残します。
# なお、retrieve_and_clean_session_result は現在の utils.py に存在するので、インポート文には残します。
from .utils import retrieve_and_clean_session_result

from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template import Template, Context
from .models import ExecuteLine
# utils.py のインポート（SQL実行用）
from .utils import execute_code_in_file
# ★★★ 新しい正規表現実行ファイルをインポート ★★★
from .regex_executor import execute_regex_code

# Create your views here.

# シンプルな index 関数は、クラスベースビューに一本化するため削除しました。
# (urls.py で IndexView.as_view() を使用してください)


class IndexView(ListView):
    template_name = 'tst/index.html'
    model = ExecuteLine
    queryset = ExecuteLine.objects.all()

    def post(self, request, *args, **kwargs):
        model = ExecuteLine
        queryset = ExecuteLine.objects.filter(type='1')
        print("test: ", queryset)
        single_value = request.GET.get('single')
        print("single_value:", single_value)
        line_id = request.POST.get('no')
        print("line_id:", line_id)
        if line_id is None:
            print(11)
            return JsonResponse({"success": True})

        print(22)
        content = request.POST.get(f"content_input_no_{line_id}")
        modification_flag = (request.POST.get('modification_flag') == '1')
        if (modification_flag):
            edited_content1 = request.POST.get(
                f"edited_content_no_{line_id}")
            edited_content2 = request.POST.get(
                f"edited_content2_no_{line_id}")
            update_execute_line(line_id, edited_content1, edited_content2)

        try:
            execute_line = get_object_or_404(ExecuteLine, pk=line_id)
            print(2231)
            line = execute_line.line
            line2 = execute_line.line2
            print(2232)
            line_type = str(execute_line.type)
            print(2233)
            output_type = execute_line.output_type
            result = None
            print(223)
            if line_type == '1':  # SQL
                result = self.execute_Makuro(line, output_type)
            elif line_type == '2':  # マクロ
                result = self.execute_SQL(line, output_type)
            elif line_type == '3':  # 正規表現
                result = self.execute_RegEx(
                    line, line2, content, output_type)
            else:
                result = {"success": False,
                          "error": f"未定義のタイプ: {line_type}"}

            if result and result.get('success') is not False:
                return JsonResponse(result)
            else:
                return JsonResponse(result, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": f"サーバー側で予期せぬエラーが発生しました: {str(e)}"}, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['executeline_list'] = context['object_list']
        return context

    def execute_SQL(self, line, output_type):
        print("SQL実行:", line, "出力タイプ:", output_type)
        return execute_code_in_file(line, output_type)

    def execute_Makuro(self, line, output_type):
        print("マクロ実行:", line, "出力タイプ:", output_type)
        file_name = r"C:\Users\wowp1\AppData\Roaming\sakura\RecKey.mac"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(line)
        return {"success": True, "type": "MACRO", "message": "マクロが実行されました", "executed_query": "マクロ実行モード"}

    def execute_RegEx(self, line, line2, content, output_type):
        print("正規表現実行:", line, "出力タイプ:", output_type)

        return execute_regex_code(line, line2, content, output_type)
