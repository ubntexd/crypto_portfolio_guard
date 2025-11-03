# Crypto Portfolio Guard

Application complète de gestion et de suivi d'actifs crypto avec surveillance en temps réel, sauvegarde automatique, et dashboard web professionnel.

## 🎯 Fonctionnalités

- 📊 Surveillance en temps réel des coins, balances, prix, variations, PnL
- 💾 Sauvegarde quotidienne dans base de données SQLite/MySQL
- 📝 Journalisation complète de toutes les opérations
- 🎨 Dashboard Web professionnel (Flask + React + Tailwind)
- 🤖 Gestion automatique avec règles configurables
- ✅ Tests unitaires complets
- 🚀 CI/CD avec GitHub Actions

## 🏗️ Architecture

```
crypto_portfolio_guard/
├── config/          # Configuration (YAML)
├── core/            # Modules principaux
├── storage/         # Base de données
├── web/             # Interface web
├── tests/           # Tests unitaires
├── run.py           # Point d'entrée
└── requirements.txt # Dépendances
```

## 📦 Installation

```bash
# Cloner le repository
git clone https://github.com/ubntexd/crypto_portfolio_guard.git
cd crypto_portfolio_guard

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer
cp config/settings.yaml.example config/settings.yaml
# Éditer config/settings.yaml avec vos paramètres
```

## 🚀 Utilisation

```bash
# Lancer l'application
python run.py

# Lancer les tests
pytest tests/

# Lancer avec Docker
docker-compose up
```

## 📝 Configuration

Éditez `config/settings.yaml` pour configurer :
- Clés API Exchange (Binance)
- Seuils de gain/p perte
- Paramètres de la base de données
- Paramètres de logging

## 🧪 Tests

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=core --cov=storage

# Tests d'un module spécifique
pytest tests/test_exchange.py
```

## 📄 Licence

MIT

## 👤 Auteur

andoh.ezan1@gmail.com

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.
