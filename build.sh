#!/bin/bash

# --- Lecture du paramètre ---
for arg in "$@"; do
    case $arg in
        version=*)
        VERSION="${arg#*=}"
        shift
        ;;
    esac
done

if [ -z "$VERSION" ]; then
    echo "❌ Version non fournie : ./build.sh version=1.0.1"
    exit 1
fi

echo "➡ Mise à jour de la version : $VERSION"

# --- Chemin correct vers settings.py ---
SETTINGS_FILE="./todo/settings.py"

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "❌ Fichier settings.py introuvable : $SETTINGS_FILE"
    exit 1
fi

# --- Met à jour la variable VERSION ---
sed -i "s/^VERSION = .*/VERSION = \"$VERSION\"/" "$SETTINGS_FILE"

# --- Commit ---
git add "$SETTINGS_FILE"
git commit -m "Bump version to $VERSION"

# --- Tag (si inexistant) ---
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "⚠️ Tag $VERSION existe déjà, utilisation du tag existant"
else
    git tag "$VERSION"
fi

# --- Création de la tarball ZIP ---
git archive --format=zip --prefix=todolist-$VERSION/ --output=todolist-$VERSION.zip "$VERSION"

echo "🎉 Build terminé : todolist-$VERSION.zip"
