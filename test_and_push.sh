#!/bin/bash
# Script pour tester la connexion SSH et pousser vers GitHub

set -e

cd "$(dirname "$0")"

echo "🔍 Test de la connexion SSH à GitHub..."
echo ""

# Test de la connexion SSH
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ Connexion SSH réussie !"
    echo ""
    echo "📦 Push vers GitHub..."
    git push -u origin main
    echo ""
    echo "✅ Push réussi ! Vérifiez sur : https://github.com/ubntexd/crypto_portfolio_guard"
else
    echo "❌ La clé SSH n'est pas encore ajoutée à GitHub."
    echo ""
    echo "📋 Pour continuer :"
    echo "1. Copiez votre clé publique :"
    echo ""
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "2. Ajoutez-la sur GitHub : https://github.com/settings/keys"
    echo "3. Relancez ce script : ./test_and_push.sh"
    echo ""
    echo "📖 Guide complet : cat add_ssh_to_github.md"
    exit 1
fi
