document.addEventListener("DOMContentLoaded", function () {
  // CSRFトークンを取得
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  const executeButtons = document.querySelectorAll(".btn-execute");

  executeButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const lineNo = this.getAttribute("data-no");
      const container = document.getElementById(`result-container-${lineNo}`);
      const form = document.getElementById(`form-${lineNo}`);
      const formData = new FormData(form);

      // 実行ボタンを無効化
      this.disabled = true;
      this.textContent = "実行中...";
      // CSSクラスを使用
      container.innerHTML = `<div class="result-running">実行中...</div>`;

      try {
        const response = await fetch(form.action || window.location.href, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
          },
          body: formData,
        });

        const result = await response.json();

        if (response.ok) {
          container.innerHTML = generateResultHtml(result);
        } else {
          container.innerHTML = generateErrorHtml(
            result.error || "サーバー処理エラーが発生しました。",
            result
          );
        }
      } catch (error) {
        container.innerHTML = generateErrorHtml(
          "通信エラー: " + error.message,
          {}
        );
      } finally {
        // 実行ボタンを再度有効化
        this.disabled = false;
        this.textContent = "実行";
      }
    });
  });

  // 実行結果をHTMLに変換する関数
  function generateResultHtml(result) {
    // 成功/失敗に応じてクラス名を設定
    const resultClass = result.success ? "result-success" : "result-failure";

    let html = `
        <div class="result-box ${resultClass}"> 
            <h4 class="result-title">
                ${result.success ? "✅ 実行成功" : "❌ 実行失敗"} (${
      result.type
    })
            </h4>
            
            <p class="query-label">実行クエリ:</p>
            <pre class="executed-query">${result.executed_query}</pre>
        `;

    if (result.type === "SELECT" && result.data && result.data.length > 0) {
      // SELECT結果のテーブル生成
      html += `<h5 class="result-count">取得結果 (${result.count}件)</h5>
                     <div class="table-container"> 
                     <table>
                         <thead>
                             <tr>`;
      result.columns.forEach((col) => {
        html += `<th>${col}</th>`;
      });
      html += `        </tr>
                         </thead>
                         <tbody>`;
      result.data.slice(0, 5).forEach((row) => {
        // 最大5行表示に制限
        html += `<tr>`;
        row.forEach((cell) => {
          // NULL表示とtd要素はそのまま
          html += `<td>${cell === null ? "NULL" : cell}</td>`;
        });
        html += `</tr>`;
      });
      html += `        </tbody>
                     </table>
                     </div>`;
      if (result.count > 5) {
        // クラスを使用
        html += `<p class="omission-note">... 他 ${
          result.count - 5
        } 件は省略されました。</p>`;
      }
    } else if (result.type === "DML/DDL") {
      html += `<p class="query-label">変更クエリ結果:</p>
                     <p>${result.count} 行が影響を受けました。</p>`;
    }

    html += `</div>`;
    return html;
  }

  // エラーメッセージをHTMLに変換する関数
  function generateErrorHtml(errorMessage, fullResult = {}) {
    let errorDetails =
      fullResult.error || "詳細なエラー情報はサーバーログを確認してください。";
    return `
            <div class="result-box result-failure"> 
                <h4 class="result-title">❌ 実行失敗</h4>
                <p class="query-label">エラー:</p>
                <pre class="error-message">${errorMessage}</pre>
            </div>`;
  }
});
