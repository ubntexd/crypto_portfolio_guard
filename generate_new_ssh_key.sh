#!/bin/bash
# Script pour générer une nouvelle clé SSH et la configurer

set -e

cd "$(dirname "$0")"

NEW_KEY_NAME="id_ed25519_crypto_portfolio"
NEW_KEY_PATH="$HOME/.ssh/$NEW_KEY_NAME"

echo "🔑 Génération d'une nouvelle clé SSH pour ce projet..."
echo ""

# Générer la nouvelle clé
ssh-keygen -t ed25519 -C "andoh.ezan1@gmail.com" -f "$NEW_KEY_PATH" -N ""

echo ""
echo "✅ Nouvelle clé générée : $NEW_KEY_PATH"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Votre nouvelle clé publique :"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "${NEW_KEY_PATH}.pub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Prochaines étapes :"
echo ""
echo "1. Copiez la clé publique ci-dessus"
echo ""
echo "2. Ajoutez-la sur GitHub :"
echo "   https://github.com/settings/keys"
echo "   - Cliquez sur 'New SSH key'"
echo "   - Title : 'VPS Server - Crypto Portfolio Guard'"
echo "   - Collez la clé publique"
echo ""
echo "3. Configurez Git pour utiliser cette clé :"
echo "   git config core.sshCommand 'ssh -i $NEW_KEY_PATH'"
echo ""
echo "4. Testez la connexion :"
echo "   ssh -i $NEW_KEY_PATH -T git@github.com"
echo ""
echo "5. Poussez le code :"
echo "   ./test_and_push.sh"
echo ""

# Proposer de configurer automatiquement
read -p "Voulez-vous que je configure Git pour utiliser cette nouvelle clé maintenant ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[OoYy]$ ]]; then
    git config core.sshCommand "ssh -i $NEW_KEY_PATH"
    echo ""
    echo "✅ Git configuré pour utiliser la nouvelle clé SSH"
    echo ""
    echo "Test de la connexion..."
    ssh -i "$NEW_KEY_PATH" -T git@github.com 2>&1 || echo "⚠️  Vous devez d'abord ajouter la clé sur GitHub"
fi
