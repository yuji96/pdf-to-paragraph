## 手順

### 1. データの準備

```
wget hoge.zip
unzip hoge
remove img/, html/ and index.html in unzipped dir
```

TODO: データ形式の変換

### 2. label studio の構築

まず環境変数の定義

`LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT` は `./data` への絶対パスを指定

```
LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/path/to/data
```

できたら起動

```
pip install label-studio
label-studio start pdf-to-paragraph --init \
    --username hoge@example.com --password hoge \
    --label-config interface.xml
```

### 3. label studio と local storage を紐付ける

手動で UI をいじる必要がある

https://labelstud.io/guide/storage#Local-storage

## 参考

- task (json) の定義: https://labelstud.io/guide/task_format#Relevant-JSON-property-descriptions
- import pre-annotation: https://labelstud.io/guide/predictions
- zoom の挙動が逆 (open issue): https://github.com/HumanSignal/label-studio-frontend/issues/135
