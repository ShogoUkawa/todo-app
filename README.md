# TODO App

シンプルなTODO管理アプリケーション。Next.js + Supabase で構築されています。

🌐 **Live Demo**: https://shogoukawa.github.io/todo-app/

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 (App Router), TypeScript |
| Backend | Supabase (PostgreSQL + REST API) |
| Deployment | GitHub Pages (frontend) |
| Styling | CSS Modules |
| Linting/Formatting | Biome |

---

## Prerequisites

- **Node.js 20+** — `.nvmrc` で管理。[nvm](https://github.com/nvm-sh/nvm) 使用時は `nvm use` を実行
- **[just](https://github.com/casey/just)** (optional) — タスクランナー

---

## Quick Start

### 1. リポジトリのクローン

```bash
git clone https://github.com/ShogoUkawa/todo-app.git
cd todo-app
```

### 2. Supabase プロジェクトのセットアップ

1. [Supabase](https://supabase.com) でアカウント作成
2. 新しいプロジェクトを作成
3. SQL Editor で以下を実行:

```sql
CREATE TABLE todos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

ALTER TABLE todos DISABLE ROW LEVEL SECURITY;
```

4. Settings → API から以下をコピー:
   - Project URL
   - anon public key

### 3. 環境変数の設定

```bash
cd frontend
cp .env.example .env.local
```

`.env.local` を編集:

```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 4. 起動

```bash
# just を使う場合
just bootstrap
just dev

# 手動の場合
cd frontend
npm install
npm run dev
```

アプリは http://localhost:3000 で起動します。

---

## Available Commands

### just を使用

| Command | 説明 |
|---|---|
| `just dev` | 開発サーバー起動 |
| `just build` | プロダクションビルド |
| `just lint` | コードのlint |
| `just format` | コードのフォーマット |
| `just install` | 依存関係のインストール |
| `just bootstrap` | 初回セットアップ |

### npm を直接使用

```bash
cd frontend
npm run dev         # 開発サーバー
npm run build       # プロダクションビルド
npm run lint        # lint
npm run format      # format
```

---

## Deployment

### GitHub Pages

`main` ブランチへのpush時に自動デプロイされます（[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)）。

**セットアップ:**

1. **Settings → Pages → Source** を **GitHub Actions** に設定
2. **Settings → Secrets → Actions** で以下を追加:
   - `SUPABASE_URL`: Supabase の Project URL
   - `SUPABASE_ANON_KEY`: Supabase の anon public key

デプロイ後、`https://YOUR_USERNAME.github.io/todo-app/` でアクセス可能。

---

## CI/CD

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) が自動実行されます:

- **Lint** - Biome でコード品質チェック
- **Build** - プロダクションビルドの検証

---

## 料金

完全無料で運用可能:

- **Supabase**: 無料プラン（500MB DB、5GB帯域/月）
- **GitHub Pages**: 無料（公開リポジトリ）
- **GitHub Actions**: 2,000分/月（公開リポジトリ）

---

## Documentation

- **[保守運用ガイド](docs/MAINTENANCE.md)** - 日常的な運用方法、トラブルシューティング
- **[開発ガイド](docs/CLAUDE.md)** - アーキテクチャ、コーディング規約

---

## License

MIT
