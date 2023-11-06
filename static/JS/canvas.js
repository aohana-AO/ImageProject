
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var rectSize = 100; // 四角形の初期サイズ
    var zoomFactor = 1.0; // 初期ズーム倍率
    var zoomStep = 0.1; // ズームのステップ
    var isDragging = false; // ドラッグ中かどうかを示すフラグ
    var dragStartX, dragStartY; // ドラッグ開始位置
    var offsetX = 0; // CanvasのX方向オフセット
    var offsetY = 0; // CanvasのY方向オフセット

    // Canvasの初期描画
    drawRectangle();
    drawImageOnCanvas();

    // マウススクロールイベントをキャプチャ
    canvas.addEventListener("wheel", function (event) {
      event.preventDefault();
      if (event.deltaY < 0) {
        // マウスホイールを上にスクロールした場合、拡大
        zoomFactor += zoomStep;
      } else {
        // マウスホイールを下にスクロールした場合、縮小
        zoomFactor -= zoomStep;
        // ズーム倍率が最小値1未満にならないように制約を設ける
        if (zoomFactor < 1.0) {
          zoomFactor = 1.0;
        }
      }
      // 四角形を再描画
      drawRectangle();
    });

    // マウスダウンイベントをキャプチャ
    canvas.addEventListener("mousedown", function (event) {
      isDragging = true;
      dragStartX = event.clientX;
      dragStartY = event.clientY;
    });

    // マウスアップイベントをキャプチャ
    canvas.addEventListener("mouseup", function () {
      isDragging = false;
    });

    // マウスムーブイベントをキャプチャ
    canvas.addEventListener("mousemove", function (event) {
      if (isDragging) {
        var x = event.clientX;
        var y = event.clientY;
        var dx = x - dragStartX;
        var dy = y - dragStartY;

        // Canvasのオフセットを更新
        offsetX += dx;
        offsetY += dy;

        // ドラッグ開始位置を更新
        dragStartX = x;
        dragStartY = y;

        // 四角形を再描画
        drawRectangle();
      }
    });

    function drawRectangle() {
    // Canvasのサイズを更新
    canvas.width = rectSize * zoomFactor;
    canvas.height = rectSize * zoomFactor;

    // チェック柄を描画
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var checkerSize = 10; // チェックのサイズ
    for (var x = 0; x < canvas.width; x += checkerSize) {
      for (var y = 0; y < canvas.height; y += checkerSize) {
        if ((x / checkerSize + y / checkerSize) % 2 === 0) {
          ctx.fillStyle = "#666666"; // 黒色のチェック
        } else {
          ctx.fillStyle = "#333333";  // グレーのチェック
        }
        ctx.fillRect(x, y, checkerSize, checkerSize);
      }
    }
  }
      // イメージをCanvasに描画する関数
    function drawImageOnCanvas() {
        var img = new Image();
        img.onload = function() {
            // 画像をCanvasのサイズに合わせて描画
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        }
        img.src = imageUrl;
    }