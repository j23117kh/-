# レポート課題 II 仕様書（report2.md）

東京情報大学 情報システム学系  
システムプログラミング（2025後期）

学籍番号： j23117 
氏名：  亀田 颯人
提出日：  2026年1月4日

---

# 1. アプリ名
TaskCanvas
---

# 2. アプリ概要（1〜3行）
このアプリは、大学の講義における課題を管理・可視化するための Web アプリである 。授業名、期限、優先度を記録することで、学生が自身のタスクの優先順位を一目で把握し、計画的に課題をこなすことを目的とする 。

---

# 3. 機能一覧
本アプリで提供する機能を箇条書きで記述。

- **一覧表示（GET /items）**: 保存されている全課題のリスト表示。
- **新規追加（POST /items）**: 授業名、課題名、期限、優先度を指定して登録。
- **詳細表示（GET /items/{id}）**: ID ごとの詳細情報の個別表示。
- **更新（PUT /items/{id}）**: 課題内容およびステータス（未完了/完了）の編集。
- **削除（DELETE /items/{id}）**: データベースからの物理削除。
- **画面遷移（Vue Router）**: 一覧ページと詳細ページの切り替え。
- **検索・ソート**: 授業名や課題名でのフィルタリング、項目ごとの並び替え（フロントエンド実装）。

---

# 4. データ構造（Pydantic & DBモデル）

## 4.1 JSONスキーマ（1件分の例）
```json
{
  "id": 1,
  "subject": "システムプログラミング",
  "title": "レポート課題II",
  "due_date": "2026-01-04",
  "priority": "高",
  "status": "未完了"
}
---
```
## 4.2 Pydanticモデル（schemas/item.py）
```python
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class ItemBase(BaseModel):
    subject: str
    title: str
    due_date: date
    priority: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    subject: Optional[str] = None
    title: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class ItemResponse(ItemBase):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)

```

## 4.3 DBモデル（models/item.py）※SQLite
```python
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    title = Column(String)
    due_date = Column(Date)
    priority = Column(String)
    status = Column(String, default="未完了")
```

# 5. 画面構成（UI仕様）
## 5.1 一覧画面（ItemsPage.vue）
データ一覧: task-table による課題リストの表示。

新規追加フォーム: 最上部の form-section から課題を即座に追加。

検索・フィルタ: 検索ボックスによりリアルタイムで表示内容を絞り込み。

画面遷移: 各行の「詳細・編集」リンク、またはタイトルをクリックして詳細画面へ。

## 5.2 詳細画面（ItemDetail.vue）
個別データの取得: id に基づいた最新情報を API から取得。

更新フォーム: 状態（未完了/完了）やその他の項目を編集可能。

削除ボタン: 削除確認ダイアログ表示後、削除を実行し一覧へ遷移。

戻るボタン: 変更を行わずに一覧へ戻るリンク。

# 6. API 仕様（FastAPI）
## 6.1 GET /items
概要：全件一覧取得。 レスポンス：ItemResponse[]

## 6.2 GET /items/{id}
概要：指定した ID のアイテムを 1 件取得。 エラー：404 Not Found

## 6.3 POST /items
概要：新規課題の追加。 リクエスト：ItemCreate レスポンス：作成された ItemResponse

## 6.4 PUT /items/{id}
概要：既存課題の更新。 エラー：404 (不在) / 422 (バリデーションエラー)

## 6.5 DELETE /items/{id}
概要：課題の削除。 レスポンス：{"result": "ok"}

# 7. 保存方式（SQLite）
本アプリでは SQLiteを使用している。

理由：本アプリでは「授業名」「期限」「優先度」といった項目が全てのデータで共通しており、データ構造が固定されている 。また、期限が近い順や優先度の高い順といったソート（並び替え）を効率的に行う必要があるため、リレーショナルデータベースである SQLite が最も適切であると判断した 。SQLite は軽量でありながら SQL による高度なデータ操作が可能であり、個人向けの管理アプリとして最適なバランスを持っているため採用した。

## 8. セットアップ手順（環境構築）
## 8.1 フロント（Vue）
```
cd api-demo
npm install
npm run serve
```
## 8.2 バックエンド（FastAPI）
```
cd fastapi-app
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```
## 8.3 ブラウザ
```
http://localhost:8080/
```

# 9. 動作確認テスト（自己確認）
- [x] 一覧が表示される

- [x] 新規追加後に一覧が更新される

- [x] 詳細画面に遷移できる

- [x] 更新が反映される

- [x] 削除後に一覧へ戻る

- [x] 404/422 が正しく表示される

- [x] FastAPI のデータが SQLite に永続化される

## 10. 既知の問題
更新完了後にアラートが出るが、画面上のデータ同期タイミングが環境によりわずかに遅れる場合がある。

エラー時のメッセージ表示が簡素である。

## 11. 今後の改善点
カレンダー表示: 期限（due_date）をカレンダー形式で視覚化する。

通知機能: 期限が近い課題を強調表示する。


認証機能: ユーザーログイン機能の実装。
