#!/bin/bash
# Script pour installer GitHub CLI et créer le repository automatiquement

echo "🔧 Installation de GitHub CLI..."
echo ""

# Vérifier si gh est déjà installé
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI est déjà installé"
    gh --version | head -1
else
    echo "📦 Installation de GitHub CLI..."
    
    # Détecter le système
    if [ -f /etc/debian_version ]; then
        # Ubuntu/Debian
        echo "Détection: Ubuntu/Debian"
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
        && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
        && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
        && sudo apt update \
        && sudo apt install gh -y
    else
        echo "❌ Système non supporté pour l'installation automatique"
        echo "Installez GitHub CLI manuellement : https://cli.github.com/manual/installation"
        exit 1
    fi
fi

echo ""
echo "🔐 Authentification GitHub..."
gh auth login

echo ""
echo "📦 Création du repository..."
gh repo create ubntexd/crypto_portfolio_guard --public --source=. --remote=origin --push

echo ""
echo "✅ Repository créé et code poussé !"
echo "Vérifiez sur : https://github.com/ubntexd/crypto_portfolio_guard"
