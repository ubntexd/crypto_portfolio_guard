# Guide de Push vers GitHub

## 🔐 Authentification GitHub

Pour pousser le code vers GitHub, vous avez besoin d'une authentification. Voici les différentes méthodes disponibles :

## Option 1 : Personal Access Token (Recommandé)

### Étapes :

1. **Créer un Personal Access Token (PAT)**
   - Allez sur : https://github.com/settings/tokens
   - Cliquez sur "Generate new token" > "Generate new token (classic)"
   - Donnez un nom (ex: "crypto_portfolio_guard")
   - Sélectionnez les scopes : `repo` (accès complet aux repositories)
   - Cliquez sur "Generate token"
   - **⚠️ IMPORTANT : Copiez le token immédiatement, vous ne pourrez plus le voir après !**

2. **Utiliser le token pour pousser**
   ```bash
   cd /home/andoh_ezan/crypto_portfolio_guard
   ./push_to_github.sh VOTRE_TOKEN_ICI
   ```

   Ou manuellement :
   ```bash
   git remote set-url origin https://VOTRE_TOKEN@github.com/ubntexd/crypto_portfolio_guard.git
   git push -u origin main
   ```

## Option 2 : Authentification Interactive

```bash
cd /home/andoh_ezan/crypto_portfolio_guard
git push -u origin main
```

Quand Git demande :
- **Username** : `ubntexd` (votre username GitHub)
- **Password** : Votre Personal Access Token (PAS votre mot de passe GitHub)

## Option 3 : SSH (Plus sécurisé pour usage répété)

### Étapes :

1. **Générer une clé SSH** (si vous n'en avez pas)
   ```bash
   ssh-keygen -t ed25519 -C "andoh.ezan1@gmail.com"
   # Appuyez sur Entrée pour les chemins par défaut
   # Choisissez un mot de passe ou laissez vide
   ```

2. **Afficher la clé publique**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. **Ajouter la clé à GitHub**
   - Copiez le contenu de la clé publique
   - Allez sur : https://github.com/settings/keys
   - Cliquez sur "New SSH key"
   - Donnez un titre (ex: "VPS Server")
   - Collez la clé publique
   - Cliquez sur "Add SSH key"

4. **Configurer Git pour utiliser SSH**
   ```bash
   cd /home/andoh_ezan/crypto_portfolio_guard
   git remote set-url origin git@github.com:ubntexd/crypto_portfolio_guard.git
   git push -u origin main
   ```

## Option 4 : GitHub CLI (gh)

1. **Installer GitHub CLI** (si pas déjà installé)
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install gh
   ```

2. **Authentifier**
   ```bash
   gh auth login
   # Suivez les instructions à l'écran
   ```

3. **Pousser**
   ```bash
   cd /home/andoh_ezan/crypto_portfolio_guard
   git push -u origin main
   ```

## 🔍 Vérification

Après un push réussi, vérifiez sur GitHub :
- https://github.com/ubntexd/crypto_portfolio_guard

## ⚠️ Sécurité

- Ne commitez JAMAIS de tokens ou clés API dans le code
- Utilisez `.env` ou `config/secrets.yaml` (déjà dans `.gitignore`)
- Les tokens doivent être gardés secrets

## 📝 Commandes utiles

```bash
# Vérifier le remote
git remote -v

# Vérifier le statut
git status

# Voir les commits
git log --oneline

# Push simple
git push -u origin main

# Push avec le script
./push_to_github.sh [TOKEN]
```
