# 🔧 Corriger les permissions SSH - Deploy Key vs SSH Key

## ❌ Problème détecté

Votre clé SSH a été ajoutée comme **"Deploy Key"** au lieu d'une **"SSH Key"** de compte utilisateur.

Les Deploy Keys sont en **lecture seule** et ne permettent pas de pousser du code.

## ✅ Solution : Ajouter la clé comme SSH Key utilisateur

### Étape 1 : Retirer la Deploy Key (si nécessaire)

1. Allez sur : https://github.com/ubntexd/crypto_portfolio_guard/settings/keys
2. Trouvez votre clé SSH dans la section "Deploy keys"
3. Supprimez-la (bouton "Delete")

### Étape 2 : Ajouter la clé comme SSH Key utilisateur

1. **Allez sur les paramètres SSH de votre compte** :
   - https://github.com/settings/keys
   - (Note : PAS dans les paramètres du repository, mais dans les paramètres de votre compte)

2. **Cliquez sur "New SSH key"**

3. **Remplissez le formulaire** :
   - **Title** : `VPS Server - Crypto Portfolio Guard`
   - **Key type** : `Authentication Key` (option par défaut)
   - **Key** : Collez votre clé publique ci-dessous

4. **Cliquez sur "Add SSH key"**

### Votre clé publique SSH :

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ8oy/Kbi87yt4ua564dJGvWnST0FButv6d2WAwZe3MI andoh.ezan1@gmail.com
```

### Étape 3 : Tester et pousser

Une fois la clé ajoutée comme SSH Key utilisateur :

```bash
cd /home/andoh_ezan/crypto_portfolio_guard
ssh -T git@github.com
# Vous devriez voir : "Hi ubntexd! You've successfully authenticated..."

./test_and_push.sh
```

## 🔍 Différence entre Deploy Key et SSH Key

- **Deploy Key** :
  - ❌ Lecture seule
  - ❌ Limitée à un seul repository
  - ✅ Utilisée pour déploiement automatique

- **SSH Key utilisateur** :
  - ✅ Lecture + écriture
  - ✅ Accès à tous vos repositories
  - ✅ Recommandée pour le développement

## ✅ Vérification

Après avoir ajouté la clé comme SSH Key utilisateur, le push devrait fonctionner sans problème !
