#!/bin/bash
# Script pour tester la connexion SSH et pousser vers GitHub

set -e

cd "$(dirname "$0")"

echo "🔍 Test de la connexion SSH à GitHub..."
echo ""

# Test de la connexion SSH
SSH_TEST=$(ssh -T git@github.com 2>&1)
if echo "$SSH_TEST" | grep -q "successfully authenticated"; then
    echo "✅ Connexion SSH réussie !"
    echo ""
    echo "📦 Push vers GitHub..."
    
    # Essayer le push
    if git push -u origin main 2>&1 | tee /tmp/push_output.txt; then
        echo ""
        echo "✅ Push réussi ! Vérifiez sur : https://github.com/ubntexd/crypto_portfolio_guard"
    else
        if grep -q "Repository not found" /tmp/push_output.txt 2>/dev/null; then
            echo ""
            echo "❌ Le repository n'existe pas encore sur GitHub."
            echo ""
            echo "📋 Pour continuer :"
            echo "1. Créez le repository sur GitHub : https://github.com/new"
            echo "   - Nom : crypto_portfolio_guard"
            echo "   - Ne cochez AUCUNE option (pas de README, .gitignore, etc.)"
            echo "   - Cliquez sur 'Create repository'"
            echo ""
            echo "2. Relancez ce script : ./test_and_push.sh"
            echo ""
            echo "📖 Guide complet : cat CREATE_REPO.md"
            exit 1
        else
            echo ""
            echo "❌ Erreur lors du push. Vérifiez les messages ci-dessus."
            exit 1
        fi
    fi
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
