# 概要
AIシステム開発授業_画像生成チームリポジトリ。
<br>

## 構築手順
#### ①こちらのリポジトリをクローンする。

<small>※クローンとは　ネット上のリポジトリの内容を自身のローカルPC内にコピーして持ってくること</small>

```
git clone https://github.com/aohana-AO/Image_Create_Project.git
```
<br>


#### ②ローカルにもってこれたらrequirements.txt内のライブラリをインストールする
requirements.txtとは、使用する追加ライブラリやバージョンの記載場所になります。
これを共有しインストールすることでチームメンバーの使用するライブラリバージョンなどを揃えることができます。

```
pip install -r requirements.txt
```
<br>

#### ③データベースのマイグレート
マイグレーションファイルを作成。modelsに変更がなければNo changes detectedとなるかも
```
python manage.py makemigrations
```

マイグレーションファイルをデータベースに適用
```
python manage.py migrate
```
<br>

#### ④.envを作成
DjangoやAPIを使うとき、key(秘密の鍵)と言うものが必要になったりします。

これは秘密のものなので、公のリポジトリにはあげてはいけません!!
(API keyとかオープンにして漏れると悪用されちゃうよ！)

そのため、チーム内で共有し「.env」というファイルを作成しその中にkeyを入れていきます。
※ここも本来はパラメータストアとかに暗号化して登録するのがよき、、けど授業なので身内内でkey共有するので大丈夫す。
```
ルートディレクトリに.envというファイルを作成。
↓
チームから共有されたkeyをその中に貼り付け。
```
<br>

#### ⑤スーパーユーザー作成
```
python manage.py createsuperuser --noinput --username superuser
```
<br>

#### ⑥以下のコマンドでサーバーを動かす
```
python manage.py runserver
```
<br>

#### ⑦ローカルアクセス
以下にアクセス。するとローカルでサーバーを立ち上げられます
http://127.0.0.1:8000/

<br>

#### ⑧ライブラリなど追加インストールした場合
ライブラリの追加インストールをした場合、他のチームメンバーはまだそのライブラリを入れてないので、requirements.txtを更新し共有する必要が出てきます。
以下のコマンドで現在の環境のライブラリ情報などを出力できます。

※仮想環境などに入ってないと以下コマンドでめちゃくちゃなrequirementsができちゃうかも。venvなどに入っておくのが良きです。

```
pip freeze > requirements.txt

```


# 参考URL
#### チーム開発notion
https://chiseled-firewall-4a8.notion.site/8b240a432b514a5c8ff12b9a6d4fcc03
