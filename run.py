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
        
        # Module 1: Configuration & Logger
        logger.log_info("Module 1 (Configuration & Logger) - ✅ Opérationnel")
        
        # Module 2: API Exchange
        try:
            from core.exchange import get_exchange
            exchange = get_exchange()
            
            # Test de récupération d'un ticker (requête publique, pas besoin d'API key)
            logger.log_info("Module 2 (API Exchange) - Test de connexion...")
            ticker = exchange.fetch_ticker('BTC/USDT')
            logger.log_info(f"Module 2 (API Exchange) - ✅ Opérationnel")
            logger.log_info(f"  Test réussi: BTC/USDT = ${ticker['last']:.2f}")
            
        except Exception as e:
            logger.log_warning(f"Module 2 (API Exchange) - ⚠️  Erreur: {e}")
            logger.log_info("  (Normal si pas d'API key configurée ou pas de connexion internet)")
        
        # TODO: Ajouter les modules suivants ici
        
        return 0
        
    except Exception as e:
        print(f"Erreur fatale: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
