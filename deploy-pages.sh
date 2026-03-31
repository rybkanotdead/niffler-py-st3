#!/usr/bin/env bash
# ============================================================
# deploy-pages.sh
# Деплоит allure-report в ветку gh-pages для GitHub Pages
# Использование: bash deploy-pages.sh
# ============================================================
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_DIR="$REPO_DIR/allure-report"

cd "$REPO_DIR"

echo "🧹 Очищаю git-кэш для игнорируемых директорий..."
git rm -r --cached allure-report/ 2>/dev/null && echo "  ✓ allure-report удалён из кэша" || echo "  ℹ allure-report не был в кэше"
git rm -r --cached allure-results/ 2>/dev/null && echo "  ✓ allure-results удалён из кэша" || echo "  ℹ allure-results не был в кэше"

# Коммитим изменения .gitignore / кэша если есть
if ! git diff --cached --quiet; then
  git commit -m "chore: remove cached report files from git index"
  git push origin main
fi

echo ""
echo "📊 Деплою Allure report в ветку gh-pages..."

# Чистим зависшие worktree от предыдущих прерванных запусков
git worktree prune 2>/dev/null || true

WORKTREE_DIR=$(mktemp -d)

# Убираем существующий worktree если вдруг остался
git worktree remove --force "$WORKTREE_DIR" 2>/dev/null || true

# Создаём или чекаутим gh-pages — всегда берём актуальное состояние remote
if git ls-remote --exit-code --heads origin gh-pages &>/dev/null; then
  echo "  ✓ Ветка gh-pages существует, синхронизирую с remote..."
  git fetch origin gh-pages
  # Принудительно обновляем локальную ветку до remote
  git branch -f gh-pages origin/gh-pages 2>/dev/null || true
  git worktree add "$WORKTREE_DIR" gh-pages
else
  echo "  📌 Ветка gh-pages не найдена, создаю orphan..."
  git worktree add --orphan -b gh-pages "$WORKTREE_DIR"
fi

# Очищаем старое содержимое
rm -rf "${WORKTREE_DIR:?}"/*

# Копируем свежий отчёт
cp -r "$REPORT_DIR/." "$WORKTREE_DIR/"

# Добавляем .nojekyll (обязательно для Allure на GitHub Pages)
touch "$WORKTREE_DIR/.nojekyll"

# Коммитим и пушим
cd "$WORKTREE_DIR"
git add -A

if git diff --staged --quiet; then
  echo "  ℹ Нечего коммитить, отчёт актуален"
else
  git commit -m "deploy: Allure report $(date '+%Y-%m-%d %H:%M:%S')"
  git push --force origin gh-pages
  echo ""
  echo "✅ Готово! Отчёт доступен по адресу:"
  echo "   https://rybkanotdead.github.io/niffler-py-st3/"
fi

# Чистим worktree
cd "$REPO_DIR"
git worktree remove "$WORKTREE_DIR" --force

