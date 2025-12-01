#!/bin/bash
set -e  # stoppe le script si une commande échoue

# --- Lecture du paramètre version ---
for arg in "$@"; do
    case $arg in
        version=*)
        VERSION="${arg#*=}"
        shift
        ;;
    esac
done

if [ -z "$VERSION" ]; then
    echo "❌ Version non fournie : ./build.sh version=1.4.0"
    exit 1
fi

echo "➡ Lancement du linter Ruff..."
pipenv run ruff check .
echo "✅ Linter OK"

# --- Mise à jour de la version ---
SETTINGS_FILE="./todo/settings.py"
if [ ! -f "$SETTINGS_FILE" ]; then
    echo "❌ Fichier settings.py introuvable : $SETTINGS_FILE"
    exit 1
fi

sed -i "s/^VERSION = .*/VERSION = \"$VERSION\"/" "$SETTINGS_FILE"

# --- Commit et push ---
git add "$SETTINGS_FILE"
git commit -m "v$VERSION: mise à jour version et build"
git push origin main

# --- Création du tag et push si inexistant ---
if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null 2>&1; then
    echo "Tag $VERSION existe déjà, utilisation du tag existant"
else
    git tag "$VERSION"
    git push origin "$VERSION"
    echo "✅ Tag $VERSION créé et poussé"
fi

# --- Lancement des tests ---
echo "➡ Lancement des tests..."
pytest || { echo "❌ Certains tests ont échoué. Build arrêté."; exit 1; }

# --- Génération du rapport visuel ---
if [ -f "test_report.py" ]; then
    python3 test_report.py
fi

# --- Création de la tarball ZIP ---
ZIP_FILE="$PWD/todolist-$VERSION.zip"
echo "DEBUG: VERSION='$VERSION', ZIP_FILE='$ZIP_FILE'"

if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null 2>&1; then
    git archive --format=zip --prefix="todolist-$VERSION/" --output="$ZIP_FILE" "$VERSION" \
        || { echo "❌ Erreur lors de la création de la tarball à partir du tag"; exit 1; }
else
    echo "⚠ Tag $VERSION introuvable, utilisation de HEAD pour la tarball"
    git archive --format=zip --prefix="todolist-$VERSION/" --output="$ZIP_FILE" HEAD \
        || { echo "❌ Erreur lors de la création de la tarball à partir de HEAD"; exit 1; }
fi

echo "✅ Build terminé : $ZIP_FILE"
