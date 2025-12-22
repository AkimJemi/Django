# [tst/regex_executor.py]

import re

import subprocess


def execute_regex_code(replace_before, replace_after, content, output_type):
    sed_command = f"echo {content} | sed 's/{replace_before}/{replace_after}/g'"
    try:
        result = subprocess.run(sed_command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = result.stdout.decode('utf-8').strip()
        print(f"result:", result)
        return {
            "success": True,
            "type": "REGEX",
            "message": "正規表現が正常に実行されました。",
            "data": result,
            "columns": ["Match Result"],
            "executed_query": result
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "type": "REGEX",
            "message": "sed 実行エラーが発生しました: {e.stderr.decode()}",
            "data": result.stdout.decode(),
            "columns": ["Match Result"],
            "executed_query": f"sed 実行エラーが発生しました: {e.stderr.decode()}"
        }
