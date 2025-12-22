from django.db import connection, transaction
from django.db.utils import Error as DBError
from .models import ExecuteLine
from django.shortcuts import get_object_or_404


def execute_code_in_file(code_content, output_type, **kwargs):
    """
    Djangoのデータベース接続機能を使用してSQLコードを実行する。

    :param code_content: 実行するSQL文 (str)
    :param output_type: 出力の種類 (int) - 1:出力, 2:実行, 3:出力+実行
    :param kwargs: その他の引数
    :return: 実行結果データまたはエラー情報を含む辞書
    """

    line = code_content

    is_select = line.strip().upper().startswith('SELECT')

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(line)

                if is_select:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()

                    if output_type in [1, 3]:
                        print("\n--- SQL実行結果 (SELECT) ---")
                        print(f"カラム: {columns}")
                        print(f"レコード数: {len(results)}")
                        return {"success": True, "type": "SELECT", "count": len(results), "columns": columns, "data": results, "executed_query": line}

                    return {"success": True, "type": "SELECT", "count": len(results), "executed_query": line}

                else:
                    row_count = cursor.rowcount

                    if output_type in [2, 3]:
                        print(f"--- SQL実行結果 (変更): {row_count} 行が影響を受けました。---")

                    return {"success": True, "type": "DML/DDL", "count": row_count, "executed_query": line}

    except DBError as e:
        print(f"\n--- データベースエラーが発生しました: {e} ---")
        return {"success": False, "error": str(e), "executed_query": line}

    except Exception as e:
        print(f"\n--- 予期せぬエラー: {e} ---")
        return {"success": False, "error": str(e), "executed_query": line}


def retrieve_and_clean_session_result(request, result_key):
    """
    セッションから指定されたキーの結果を取得し、そのキーをセッションから削除する。

    :param request: HttpRequestオブジェクト
    :param result_key: セッションに保存されているキー名
    :return: 実行結果データ（辞書）、存在しない場合はNone
    """
    result = None
    if result_key in request.session:
        result = request.session.pop(result_key)
    return result


def update_execute_line(line_id: int, content1: str, content2: str = None):
    """
    指定されたIDのExecuteLineレコードを更新します。

    Args:
        line_id (int): 更新対象の ExecuteLine のID (views.py で取得した line_id)。
        content1 (str): 更新後の主要なコード内容 (line フィールドに対応)。
        content2 (str, optional): 更新後の補足的なコード内容 (line2 フィールドに対応)。
                                   Noneの場合は line2 の更新を行いません。

    Returns:
        bool: 更新が成功したかどうか。
    """
    try:
        with transaction.atomic():
            line_instance = get_object_or_404(ExecuteLine, no=line_id)

            line_instance.line = content1.strip()

            if content2 is not None:
                line_instance.line2 = content2.strip() if content2 else ""

            line_instance.save()

            print(f"ExecuteLine No.{line_id} が正常に更新されました。")
            return True

    except ExecuteLine.DoesNotExist:
        print(f"エラー: ExecuteLine No.{line_id} が見つかりませんでした。")
        return False
    except Exception as e:
        print(f"エラー: ExecuteLine No.{line_id} の更新中に予期せぬエラーが発生しました: {e}")
        return False
