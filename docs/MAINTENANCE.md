# TODO App - 保守運用ガイド

このドキュメントは、TODO アプリの日常的な保守運用方法をまとめたものです。

---

## 目次

1. [ローカル開発](#ローカル開発)
2. [コード変更からデプロイまで](#コード変更からデプロイまで)
3. [Supabase の管理](#supabase-の管理)
4. [無料枠の管理](#無料枠の管理)
5. [新機能の追加](#新機能の追加)
6. [トラブルシューティング](#トラブルシューティング)
7. [バックアップ](#バックアップ)
8. [推奨される運用](#推奨される運用)

---

## ローカル開発

### フロントエンドの起動

```bash
cd frontend
nvm use 20                    # Node 20に切り替え
npm run dev                   # localhost:3000で起動
```

### コードの整形・チェック

```bash
npm run lint                  # Biomeでlint
npm run format                # Biomeでformat
```

**注意:** バックエンド（FastAPI）はもう使っていません。ローカル開発でもSupabaseに直接接続します。

---

## コード変更からデプロイまで

### 基本的な流れ

```bash
# 1. コードを変更する

# 2. 変更をステージング
git add .

# 3. コミット（pre-commitフックが自動実行される）
git commit -m "feat: 新機能の説明"

# 4. pushすると自動的にCI/CDが実行される
git push origin main

# 5. 数分後に https://shogoukawa.github.io/todo-app/ に反映
```

### コミットメッセージの規約

- `feat:` - 新機能追加
- `fix:` - バグ修正
- `docs:` - ドキュメント変更
- `style:` - コードフォーマット
- `refactor:` - リファクタリング
- `test:` - テスト追加・修正
- `chore:` - その他の変更

### デプロイの確認

1. https://github.com/ShogoUkawa/todo-app/actions でCI/CDの実行状況を確認
2. 緑のチェックマークが表示されたら成功
3. https://shogoukawa.github.io/todo-app/ にアクセスして動作確認

---

## Supabase の管理

### ダッシュボードへのアクセス

1. [Supabase Dashboard](https://supabase.com/dashboard) にログイン
2. プロジェクト `todo-app` を開く

### データベースの確認・編集

1. **Table Editor** タブをクリック
2. `todos` テーブルを選択
3. データの閲覧・編集・削除が可能

### SQL の実行

1. **SQL Editor** タブをクリック
2. **New Query** をクリック
3. SQLを入力して実行

**例:**
```sql
-- 全てのTODOを日付順に表示
SELECT * FROM todos ORDER BY created_at DESC;

-- 完了済みのTODOを削除
DELETE FROM todos WHERE completed = true;

-- 特定のTODOを検索
SELECT * FROM todos WHERE title LIKE '%重要%';
```

### テーブル構造の変更

```sql
-- 例: 優先度カラムを追加
ALTER TABLE todos ADD COLUMN priority TEXT DEFAULT 'medium';

-- 例: カラムを削除
ALTER TABLE todos DROP COLUMN description;

-- 例: カラムのデフォルト値を変更
ALTER TABLE todos ALTER COLUMN completed SET DEFAULT false;
```

### API キーの確認

1. **Settings** → **API** タブ
2. `Project URL` と `anon public` キーを確認
3. **注意:** キーを変更した場合は、GitHub Secrets も更新する必要があります

---

## 無料枠の管理

### Supabase の制限

#### 無料プランの上限
- **Database**: 500MB
- **Bandwidth**: 5GB/月
- **Row-level operations**: 50,000リクエスト/月
- **Storage**: 1GB

#### 使用量の確認方法
1. Supabase Dashboard を開く
2. **Settings** → **Usage** タブをクリック
3. 各リソースの使用状況を確認

#### 制限を超えた場合
- **自動課金されません**
- サービスが一時停止します
- 翌月1日にリセットされます

#### 節約のヒント
- 不要なデータは定期的に削除
- 古いTODOをアーカイブ
- 大量のテストデータは避ける

### GitHub の制限

#### GitHub Pages
- 公開リポジトリは**無制限**
- 月間100GBの帯域幅制限（超過することはほぼない）

#### GitHub Actions
- 無料枠: **2,000分/月**（パブリックリポジトリ）
- 1回のデプロイ: 約2-3分
- 1日10回デプロイしても余裕

#### 使用量の確認
1. リポジトリの **Settings** → **Billing** を確認
2. または https://github.com/settings/billing でアカウント全体の使用量を確認

---

## 新機能の追加

### 例: TODOに優先度機能を追加

#### ステップ1: Supabaseでテーブル変更

```sql
-- SQL Editorで実行
ALTER TABLE todos ADD COLUMN priority TEXT DEFAULT 'medium';
```

#### ステップ2: フロントエンドの型定義を更新

```typescript
// frontend/src/features/todos/types.ts
export interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';  // 追加
  created_at: string;
  updated_at: string;
}

export interface CreateTodoPayload {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';  // 追加
}
```

#### ステップ3: UIコンポーネントを更新

```typescript
// frontend/src/features/todos/components/TodoList.tsx
// 優先度の表示・編集機能を追加
```

#### ステップ4: コミット・デプロイ

```bash
git add .
git commit -m "feat: add priority field to todos"
git push origin main
```

---

## トラブルシューティング

### デプロイが失敗する

#### 確認手順
1. https://github.com/ShogoUkawa/todo-app/actions を開く
2. 失敗したワークフローをクリック
3. エラーログを確認

#### よくある原因
- **Supabase の環境変数が未設定**
  - Settings → Secrets → Actions で `SUPABASE_URL` と `SUPABASE_ANON_KEY` を確認
- **ビルドエラー**
  - ローカルで `npm run build` を実行してエラーを再現
- **Lintエラー**
  - ローカルで `npm run lint` を実行して修正

### データが表示されない

#### 確認手順
1. ブラウザで F12 を押して開発者ツールを開く
2. **Console** タブでエラーメッセージを確認
3. **Network** タブでAPI呼び出しを確認

#### よくある原因
- **Supabase への接続エラー**
  - 環境変数が正しく設定されているか確認
  - Supabase プロジェクトが一時停止していないか確認
- **Row Level Security (RLS) の問題**
  - Supabase Dashboard → **Authentication** → **Policies**
  - `todos` テーブルの RLS が無効になっているか確認
  ```sql
  ALTER TABLE todos DISABLE ROW LEVEL SECURITY;
  ```

### ローカルで動かない

#### 環境変数の確認

```bash
# .env.local が存在するか確認
cat frontend/.env.local

# 内容を確認
# NEXT_PUBLIC_SUPABASE_URL=https://...
# NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

#### Node バージョンの確認

```bash
node --version  # v20.x.x であることを確認
nvm use 20      # 違う場合は切り替え
```

#### 依存関係の再インストール

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Supabase への接続が遅い

#### 原因
- 無料プランはリソースが限定的
- リージョンが遠い可能性

#### 対処法
- クエリを最適化
- 必要なデータのみ取得（`select('id, title, completed')`）
- ページネーションを実装

---

## バックアップ

### データのエクスポート

#### CSV形式でエクスポート

1. Supabase Dashboard → **SQL Editor**
2. 以下のSQLを実行:

```sql
COPY (SELECT * FROM todos) TO STDOUT WITH CSV HEADER;
```

3. 結果をコピーしてローカルに保存

#### JSON形式でエクスポート

```sql
SELECT json_agg(todos) FROM todos;
```

### リストア（復元）

#### CSVからインポート

1. Supabase Dashboard → **Table Editor** → `todos`
2. **Import data** をクリック
3. CSV ファイルをアップロード

#### SQLで直接挿入

```sql
INSERT INTO todos (title, description, completed)
VALUES
  ('タスク1', '説明1', false),
  ('タスク2', '説明2', true);
```

### 推奨バックアップ頻度

- **開発中**: 毎週
- **安定運用中**: 毎月
- **大きな変更前**: 必ず実施

---

## 推奨される運用

### 日次
- 特になし（コード変更時のみCI/CDが実行される）

### 週次
- Supabase の使用量をチェック
  - Dashboard → Settings → Usage
- データベースの不要なレコードを削除

### 月次
- GitHub Actions の使用時間をチェック
  - https://github.com/settings/billing
- バックアップの実施
- Supabase の使用量レポートを確認

### 機能追加時
- **必ずローカルで動作確認してからpush**
- テストデータで動作確認
- ブラウザの開発者ツールでエラーがないか確認

### セキュリティ
- Supabase のパスワードは定期的に変更（推奨: 6ヶ月ごと）
- GitHub の SSH キーを定期的に更新
- npm パッケージの脆弱性チェック: `npm audit`

---

## よくある質問

### Q: 複数人で開発できますか？
A: はい。GitHub でコラボレーターを追加し、Supabase Dashboard でチームメンバーを招待してください。

### Q: カスタムドメインを使えますか？
A: はい。GitHub Pages の設定でカスタムドメインを設定できます（DNS設定が必要）。

### Q: モバイルアプリにできますか？
A: Next.js は Web アプリですが、React Native で同じ Supabase バックエンドを使ってモバイルアプリを作ることも可能です。

### Q: 認証機能を追加できますか？
A: はい。Supabase には認証機能（Email、Google、GitHub など）が組み込まれています。フロントエンドに認証UIを追加し、RLS を有効化すればユーザーごとのデータ管理が可能です。

---

## 参考リンク

- **Supabase Documentation**: https://supabase.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **GitHub Actions Documentation**: https://docs.github.com/actions
- **Biome Documentation**: https://biomejs.dev

---

## サポート

問題が解決しない場合:
1. GitHub の Issues で質問
2. Supabase の Discord コミュニティで質問
3. Stack Overflow で検索

---

**最終更新**: 2026年2月6日
