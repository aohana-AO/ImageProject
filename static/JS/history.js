var savedLabels = {}; // ラベルと入力内容を関連付けて保存するオブジェクト

var saveButton = document.getElementById("save-button");

saveButton.addEventListener("click", function () {
  var userInputPrompt = prompt("ラベルを追加してください");

  if (userInputPrompt !== null) {
    alert("入力されたラベルは: " + userInputPrompt + " です");
    var textAreaContent = document.getElementById("prompt").value;

    // ラベルと入力内容を関連付けて保存
    savedLabels[userInputPrompt] = textAreaContent;

    var listItem = document.createElement("li");
    listItem.textContent = userInputPrompt; // ラベルをリストに追加

    contentList.appendChild(listItem);
    document.getElementById("prompt").value = "";
  } else {
    alert("変更は保存されませんでした。");
  }
});

// choose styleボタンのイベントリスナー
var chooseStyleButton = document.getElementById("choose-style-button");
var contentList = document.getElementById("content-list");
var sidebarPromptTextArea = document.getElementById("prompt");

chooseStyleButton.addEventListener("click", function () {
  var contentList = document.getElementById("content-list");
  contentList.style.display = contentList.style.display === "none" || contentList.style.display === "" ? "block" : "none";

  // 保存されたラベルのみを表示する
  contentList.innerHTML = ""; // リストをクリアして再描画
  for (var label in savedLabels) {
    var listItem = document.createElement("li");
    listItem.textContent = label;
    listItem.addEventListener("click", function (event) {
      var label = event.target.textContent;
      var relatedText = savedLabels[label];

      if (relatedText !== undefined) {
        sidebarPromptTextArea.value = relatedText; // 関連するテキストをサイドバーのpromptのテキストエリアにセット
      }
    });
    contentList.appendChild(listItem);
  }
});