document.addEventListener('DOMContentLoaded', function () {
    var items = document.querySelectorAll('.dropdown-item');
    var dropdownButton = document.getElementById('dropdownButton'); // ボタン要素を取得
    items.forEach(function (item) {
        item.addEventListener('click', function () {
            var value = this.getAttribute('data-value');
            console.log(value)
            var text = this.textContent; // テキスト内容を取得
            console.log(text)
            document.getElementById('hiddenNumberField').value = value;
            dropdownButton.textContent = text; // ボタンのテキストを更新
            console.log(text)
        });
    });
});
