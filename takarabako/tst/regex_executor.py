# [tst/regex_executor.py]

import re


def execute_regex_code(replace_before, replace_after, content, output_type):

    result = re.sub(replace_before, replace_after, content, flags=re.MULTILINE)
    return {
        "success": True,
        "type": "REGEX",
        "message": "正規表現が正常に実行されました。",
        "data": result,
        "columns": ["Match Result"],
        "executed_query": result
    }
