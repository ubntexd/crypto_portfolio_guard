#!/usr/bin/env python3
"""
Point d'entrée principal de Crypto Portfolio Guard
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.logger import get_logger
from core.config_loader import get_config


def main():
    """Fonction principale"""
    try:
        # Charger la configuration
        config = get_config()
        
        # Initialiser le logger
        logger = get_logger()
        
        logger.log_info("=== Crypto Portfolio Guard démarré ===")
        logger.log_info(f"Version: 0.1.0")
        
        # Afficher la configuration chargée
        exchange_config = config.get_exchange_config()
        logger.log_info(f"Exchange configuré: {exchange_config.get('name', 'N/A')}")
        logger.log_info(f"Mode sandbox: {exchange_config.get('sandbox', False)}")
        
        # TODO: Ajouter les modules suivants ici
        logger.log_info("Module 1 (Configuration & Logger) - ✅ Opérationnel")
        logger.log_info("En attente des modules suivants...")
        
        return 0
        
    except Exception as e:
        print(f"Erreur fatale: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
