#!/bin/bash
set -e

# Lecture du paramètre
for arg in "$@"; do
    case $arg in
        version=*)
        VERSION="${arg#*=}"
        shift
        ;;
    esac
done

if [ -z "$VERSION" ]; then
    echo "Version non fournie : ./build.sh version=1.0.1"
    exit 1
fi

echo "➡ Lancement du linter Ruff..."
pipenv run ruff check .
echo "Linter OK"

# Mise à jour de la version
SETTINGS_FILE="./todo/settings.py"
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "Fichier settings.py introuvable : $SETTINGS_FILE"
    exit 1
fi
sed -i "s/^VERSION = .*/VERSION = \"$VERSION\"/" "$SETTINGS_FILE"

# Commit et tag
git add "$SETTINGS_FILE"
git commit -m "Bump version to $VERSION"
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "Tag $VERSION existe déjà"
else
    git tag "$VERSION"
fi

# Lancement des tests
echo "➡ Lancement des tests..."
pytest || { echo "❌ Tests échoués"; exit 1; }

# Création de la tarball ZIP
git archive --format=zip --prefix=todolist-$VERSION/ --output=todolist-$VERSION.zip "$VERSION"
echo "✅ Build terminé : todolist-$VERSION.zip"
