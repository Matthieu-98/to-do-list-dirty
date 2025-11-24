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
    echo "Version non fournie : utilisez ./build.sh version=1.0.1"
    exit 1
fi

echo "➡ Mise à jour de la version : $VERSION"

# --- Met à jour le settings.py ---
sed -i "s/^VERSION = .*/VERSION = \"$VERSION\"/" todo/settings.py

# --- Commit de la mise à jour ---
git add todo/settings.py
git commit -m "Bump version to $VERSION"

# --- Tag ---
git tag "$VERSION"

# --- Création de la tarball ZIP ---
git archive \
    --format=zip \
    --prefix=todolist-$VERSION/ \
    --output=todolist-$VERSION.zip \
    "$VERSION"

echo "Build terminé : todolist-$VERSION.zip"
