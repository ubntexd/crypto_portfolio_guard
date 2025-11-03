# 🔑 Ajouter la clé SSH à GitHub

## Votre clé publique SSH :

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ8oy/Kbi87yt4ua564dJGvWnST0FButv6d2WAwZe3MI andoh.ezan1@gmail.com
```

## Étapes pour ajouter la clé à GitHub :

1. **Copiez la clé publique ci-dessus** (la ligne complète)

2. **Allez sur GitHub** :
   - Ouvrez : https://github.com/settings/keys
   - Cliquez sur **"New SSH key"**

3. **Remplissez le formulaire** :
   - **Title** : `VPS Server` (ou un nom de votre choix)
   - **Key type** : `Authentication Key`
   - **Key** : Collez la clé publique complète (la ligne ci-dessus)

4. **Cliquez sur "Add SSH key"**

5. **Vérifiez la connexion** :
   ```bash
   cd /home/andoh_ezan/crypto_portfolio_guard
   ssh -T git@github.com
   ```
   
   Vous devriez voir : `Hi ubntexd! You've successfully authenticated...`

6. **Poussez le code** :
   ```bash
   git push -u origin main
   ```

## ✅ Une fois la clé ajoutée :

Exécutez simplement :
```bash
cd /home/andoh_ezan/crypto_portfolio_guard
git push -u origin main
```

C'est tout ! Pas besoin de token ou de mot de passe à chaque fois. 🎉
