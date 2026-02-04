# 📄 report2.md — レポート課題 II 仕様書テンプレート

# レポート課題 II 仕様書（report2.md）

東京情報大学 情報システム学系  
システムプログラミング（2025後期）

---

# 1. アプリ名
（例：シンプルToDo管理アプリ）

---

# 2. アプリ概要（1〜3行）
アプリの目的・対象ユーザなどを簡潔に説明してください。

**例：**  
個人のタスクを一覧・追加・更新・削除できる、最小構成のWebアプリ。  
FastAPI（SQLite）でデータを永続化し、Vue で操作する構成。

---

# 3. 機能一覧
本アプリで提供する機能を箇条書きで記述。

- 一覧表示（GET /items）
- 新規追加（POST /items）
- 詳細表示（GET /items/{id}）
- 更新（PUT /items/{id}）
- 削除（DELETE /items/{id}）
- 画面遷移（Vue Router）
- エラーメッセージ表示（404/422）

必要に応じて追記可。

---

# 4. データ構造（Pydantic & DBモデル）

## 4.1 JSONスキーマ（1件分の例）
```json
{
  "id": 1,
  "title": "サンプル",
  "memo": "任意の補足（任意）"
}
````

## 4.2 Pydantic モデル（schemas/item.py）

```python
class ItemBase(BaseModel):
    title: str = Field(..., min_length=1)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    class Config:
        from_attributes = True
```

## 4.3 DBモデル（models/item.py）※SQLite

```python
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
```

必要に応じてフィールドを追加してよい。

---

# 5. 画面構成（UI仕様）

## 5.1 一覧画面（ItemsPage.vue）

* データ一覧を表示
* 新規追加フォーム
* 各行をクリック → `/items/:id` に遷移
* エラー表示（取得失敗など）
* ボタンの disabled 制御（送信中など）

## 5.2 詳細画面（ItemDetail.vue）

* 個別データの取得
* 更新フォーム
* 削除ボタン（削除後は一覧に戻る）
* エラー表示（404/422）
* 戻るボタン（任意）

---

# 6. API 仕様（FastAPI）

## 6.1 GET /items

**概要**：全件一覧
**レスポンス**：`ItemResponse[]`

## 6.2 GET /items/{id}

**概要**：1件取得
**エラー**：404 Not Found

## 6.3 POST /items

**概要**：新規追加
**リクエスト**：`ItemCreate`
**レスポンス**：作成された `ItemResponse`

## 6.4 PUT /items/{id}

**概要**：既存の更新
**エラー**：404 / 422

## 6.5 DELETE /items/{id}

**概要**：削除
**レスポンス**：`{"result": "ok"}`
**エラー**：404

---

# 7. 保存方式（SQLite）

本アプリでは **SQLite（RDB）** を使用している。
理由を記述すること。

**記述例：**
データ構造が固定（id・title など）であり、整合性が保ちやすい。
また件数も少なく、学習目的としてSQLiteが最も適しているため。

---

# 8. セットアップ手順（環境構築）

## 8.1 フロント（Vue）

```
cd api-demo
npm install
npm run serve
```

## 8.2 バックエンド（FastAPI）

```
cd fastapi-app
pip install -r requirements.txt（作成していれば）
uvicorn main:app --reload --port 8000
```

## 8.3 ブラウザ

```
http://localhost:8080/
```

---

# 9. 動作確認テスト（自己確認）

* [ ] 一覧が表示される
* [ ] 新規追加後に一覧が更新される
* [ ] 詳細画面に遷移できる
* [ ] 更新が反映される
* [ ] 削除後に一覧へ戻る
* [ ] 404/422 が正しく表示される
* [ ] FastAPI のデータが SQLite に永続化される

---

# 10. 既知の問題（あれば記述）

例：

* 更新後にフォームが初期化されない
* デザインが最低限
* 入力チェックが未実装（改善予定）

---

# 11. 今後の改善点（任意）

例：

* タグ機能の追加
* 完了フラグ（done）
* 並び替え機能
* スマホレイアウト

---

# 12. 参考資料

* 授業資料（第7〜11回）
* FastAPI ドキュメント
* Vue.js ドキュメント

---

© Tokyo University of Information Sciences, System Programming 2025

---
