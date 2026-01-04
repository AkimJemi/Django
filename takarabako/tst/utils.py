from django.db import connection, transaction
from django.db.utils import Error as DBError
from .models import ExecuteLine
from django.shortcuts import get_object_or_404


def execute_code_in_file(code_content, output_type, **kwargs):
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
                        return {"success": True, "type": "SELECT", "count": len(results), "columns": columns, "data": results, "executed_query": line}

                    return {"success": True, "type": "SELECT", "count": len(results), "executed_query": line}
                else:
                    row_count = cursor.rowcount
                    return {"success": True, "type": "DML/DDL", "count": row_count, "executed_query": line}

    except DBError as e:
        return {"success": False, "error": str(e), "executed_query": line}

    except Exception as e:
        return {"success": False, "error": str(e), "executed_query": line}


def retrieve_and_clean_session_result(request, result_key):
    result = None
    if result_key in request.session:
        result = request.session.pop(result_key)
    return result


def update_execute_line(line_id: int, content1: str, content2: str = None):
    try:
        with transaction.atomic():
            line_instance = get_object_or_404(ExecuteLine, no=line_id)
            line_instance.line = content1.strip()
            if content2 is not None:
                line_instance.line2 = content2.strip() if content2 else ""

            line_instance.save()
            return True

    except ExecuteLine.DoesNotExist:
        return False
    except Exception as e:
        return False
