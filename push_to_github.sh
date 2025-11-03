#!/bin/bash
# Script pour pousser le code vers GitHub
# Usage: ./push_to_github.sh [token]

set -e

cd "$(dirname "$0")"

echo "🔍 Vérification de la configuration Git..."
git remote -v

echo ""
echo "📦 Tentative de push vers GitHub..."
echo ""

# Si un token est fourni en argument
if [ ! -z "$1" ]; then
    echo "🔑 Utilisation du token fourni..."
    TOKEN="$1"
    git remote set-url origin "https://${TOKEN}@github.com/ubntexd/crypto_portfolio_guard.git"
    git push -u origin main
    echo "✅ Push réussi !"
    exit 0
fi

# Essayer avec credential helper si disponible
if git config --global credential.helper > /dev/null 2>&1; then
    echo "🔐 Tentative avec credential helper..."
    git push -u origin main && echo "✅ Push réussi !" && exit 0
fi

# Si rien ne fonctionne, donner les instructions
echo "❌ Authentification requise. Options disponibles :"
echo ""
echo "Option 1 - Token GitHub (recommandé) :"
echo "  1. Créez un Personal Access Token sur https://github.com/settings/tokens"
echo "  2. Utilisez: ./push_to_github.sh VOTRE_TOKEN"
echo ""
echo "Option 2 - Authentification interactive :"
echo "  git push -u origin main"
echo "  (Entrez votre username GitHub et votre Personal Access Token)"
echo ""
echo "Option 3 - SSH :"
echo "  1. Générez une clé SSH: ssh-keygen -t ed25519 -C 'andoh.ezan1@gmail.com'"
echo "  2. Ajoutez la clé à GitHub: https://github.com/settings/keys"
echo "  3. Changez le remote: git remote set-url origin git@github.com:ubntexd/crypto_portfolio_guard.git"
echo "  4. Poussez: git push -u origin main"
echo ""
echo "Option 4 - GitHub CLI :"
echo "  gh auth login"
echo "  git push -u origin main"
echo ""
exit 1
