# PyJMA - 日本気象庁災害データ抽出ライブラリ

## 機能紹介

PyJMA は[日本気象庁](https://www.jma.go.jp/jma/index.html)から公開した[気象・災害データ](https://www.data.jma.go.jp/developer/index.html)を抽出するための Python ライブラリです。

主要機能：
- 地震データの抽出

Todo:
- 台風データの抽出
- 火山データの抽出

## 利用開始

- pip でのインストール（おすすめ）

```
$ pip install pyjam
```

- ソースからインストール

```
$ git clone https://github.com/liaocyintl/pyjma
$ cd pyjam
$ python setup.py install
```

## 利用方法

- 災害データ取得
data_typesで取得するデータタイプを指定します。
```python
import pyjma as pg
data_types = ["earthquake"]
data = pg.disaster_data(data_types)
```

- 取得可能のデータタイプ
  - earthquake : 地震


- 取得したデータ
```text
{
    'status': 'OK',
    'results': [{
        'type': 'earthquake', // 地震情報
        'uuid': 'urn:uuid:a8c35460-1b3e-3f99-ad8a-053ae2a2006f', // データ識別し
        'link': 'http://www.data.jma.go.jp/developer/xml/data/a8c35460-1b3e-3f99-ad8a-053ae2a2006f.xml', // データリンク
        'magnitude': 4.1, // 震強
        'location': {'lon': 140.4, 'lat': 35.4}, // 震央緯度経度
        'depth': 30000, // 深さ
        'origin_time': datetime.datetime(2020, 3, 30, 17, 15, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))), // 発生日時
        'epicenter': '千葉県東方沖', // 震央
        'comment': 'この地震による津波の心配はありません。' // コメント
    }]
}
```

## リンク
- PyPI: https://pypi.org/project/pyjma/
- Github: https://github.com/liaocyintl/pyjma

## 更新履歴

- 1.0.3
  - 地震情報の取得
  - ライブラリ初期化

- 1.0.4
  - イベントIDを取得
  - 台風情報の取得

- 1.0.5
  - Proxy設定を追加

- 1.0.6
  - 台風情報を修正

- 1.0.8
  - proxyを修正


- 1.0.13
  - 大雨危険度通知情報追加