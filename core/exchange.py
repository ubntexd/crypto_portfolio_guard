"""
Module de connexion et d'interaction avec les exchanges crypto
"""

from typing import Dict, List, Optional, Any
import ccxt
from datetime import datetime
from .config_loader import get_config
from .logger import get_logger


class ExchangeManager:
    """Gestionnaire de connexion et d'interaction avec l'exchange"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise le gestionnaire d'exchange
        
        Args:
            config_path: Chemin vers le fichier de configuration
        """
        self.config = get_config(config_path)
        self.logger = get_logger(config_path)
        self.exchange_config = self.config.get_exchange_config()
        self.exchange = None
        self._initialize_exchange()
    
    def _initialize_exchange(self) -> None:
        """Initialise la connexion à l'exchange"""
        exchange_name = self.exchange_config.get('name', 'binance').lower()
        api_key = self.exchange_config.get('api_key', '')
        api_secret = self.exchange_config.get('api_secret', '')
        sandbox = self.exchange_config.get('sandbox', True)
        testnet = self.exchange_config.get('testnet', False)
        
        try:
            # Obtenir la classe de l'exchange depuis ccxt
            if not hasattr(ccxt, exchange_name):
                raise ValueError(f"Exchange '{exchange_name}' non supporté par ccxt")
            exchange_class = getattr(ccxt, exchange_name)
            
            # Configuration de base
            exchange_params = {
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',  # Spot trading
                }
            }
            
            # Configuration pour testnet/sandbox
            if testnet or sandbox:
                if exchange_name == 'binance':
                    if testnet:
                        exchange_params['options']['defaultType'] = 'test'
                        exchange_params['urls'] = {
                            'api': {
                                'public': 'https://testnet.binance.vision/api',
                                'private': 'https://testnet.binance.vision/api',
                            }
                        }
                    else:
                        # Mode sandbox (simulation)
                        self.logger.log_warning(
                            "Mode sandbox activé - les ordres ne seront pas exécutés réellement"
                        )
            
            # Créer l'instance de l'exchange
            self.exchange = exchange_class(exchange_params)
            
            # Test de connexion basique
            self._test_connection()
            
            self.logger.log_info(
                f"Exchange {exchange_name} initialisé avec succès",
                testnet=testnet,
                sandbox=sandbox
            )
            
        except AttributeError:
            raise ValueError(f"Exchange '{exchange_name}' non supporté par ccxt")
        except Exception as e:
            self.logger.log_error(f"Erreur lors de l'initialisation de l'exchange: {e}")
            raise
    
    def _test_connection(self) -> None:
        """Teste la connexion à l'exchange"""
        try:
            # Tester avec une requête publique (pas besoin d'API key)
            if hasattr(self.exchange, 'fetch_ticker'):
                self.exchange.fetch_ticker('BTC/USDT')
                self.logger.log_debug("Test de connexion réussi")
        except Exception as e:
            self.logger.log_warning(f"Test de connexion échoué (normal si pas d'API key): {e}")
    
    def fetch_balances(self) -> Dict[str, Any]:
        """
        Récupère les balances du compte
        
        Returns:
            Dictionnaire contenant les balances (free, used, total) par asset
        """
        try:
            self.logger.log_execution('exchange', 'fetch_balances')
            
            # Récupérer les balances
            balances_response = self.exchange.fetch_balance()
            
            # Formater les balances (ignorer les balances à zéro)
            balances = {}
            for asset, balance_info in balances_response.items():
                if isinstance(balance_info, dict):
                    total = balance_info.get('total', 0)
                    free = balance_info.get('free', 0)
                    used = balance_info.get('used', 0)
                    
                    # Ignorer les balances complètement à zéro
                    if total > 0 or free > 0 or used > 0:
                        balances[asset] = {
                            'free': free,
                            'used': used,
                            'total': total
                        }
            
            # Retirer les clés système de ccxt (info, free, used, total, etc.)
            balances_cleaned = {
                k: v for k, v in balances.items()
                if k not in ['info', 'free', 'used', 'total'] and isinstance(v, dict)
            }
            
            self.logger.log_info(
                f"Balances récupérées: {len(balances_cleaned)} assets avec balance > 0",
                asset_count=len(balances_cleaned)
            )
            
            return balances_cleaned
            
        except ccxt.AuthenticationError as e:
            self.logger.log_error(f"Erreur d'authentification: {e}")
            raise
        except ccxt.NetworkError as e:
            self.logger.log_error(f"Erreur réseau: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Erreur lors de la récupération des balances: {e}")
            raise
    
    def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Récupère le ticker (prix actuel) pour un symbole
        
        Args:
            symbol: Symbole de trading (ex: 'BTC/USDT')
        
        Returns:
            Dictionnaire contenant les informations du ticker
        """
        try:
            self.logger.log_execution('exchange', 'fetch_ticker', {'symbol': symbol})
            
            ticker = self.exchange.fetch_ticker(symbol)
            
            # Formater les données importantes
            ticker_data = {
                'symbol': symbol,
                'last': ticker.get('last'),  # Prix actuel
                'bid': ticker.get('bid'),    # Meilleur prix d'achat
                'ask': ticker.get('ask'),    # Meilleur prix de vente
                'high': ticker.get('high'),  # Prix le plus haut (24h)
                'low': ticker.get('low'),    # Prix le plus bas (24h)
                'volume': ticker.get('quoteVolume'),  # Volume en quote currency
                'timestamp': ticker.get('timestamp'),
                'datetime': ticker.get('datetime', datetime.now().isoformat())
            }
            
            self.logger.log_debug(
                f"Ticker récupéré pour {symbol}: {ticker_data['last']}"
            )
            
            return ticker_data
            
        except Exception as e:
            self.logger.log_error(f"Erreur lors de la récupération du ticker pour {symbol}: {e}")
            raise
    
    def fetch_tickers(self, symbols: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Récupère les tickers pour plusieurs symboles
        
        Args:
            symbols: Liste de symboles (ex: ['BTC/USDT', 'ETH/USDT'])
                    Si None, récupère tous les tickers
        
        Returns:
            Dictionnaire de tickers indexés par symbole
        """
        try:
            self.logger.log_execution(
                'exchange',
                'fetch_tickers',
                {'symbol_count': len(symbols) if symbols else 'all'}
            )
            
            if symbols:
                tickers = {}
                for symbol in symbols:
                    try:
                        tickers[symbol] = self.fetch_ticker(symbol)
                    except Exception as e:
                        self.logger.log_warning(f"Impossible de récupérer le ticker pour {symbol}: {e}")
                return tickers
            else:
                # Récupérer tous les tickers
                tickers_raw = self.exchange.fetch_tickers()
                
                # Formater les tickers
                tickers = {}
                for symbol, ticker in tickers_raw.items():
                    if symbol.endswith('/USDT'):  # Filtrer uniquement les paires USDT
                        tickers[symbol] = {
                            'symbol': symbol,
                            'last': ticker.get('last'),
                            'bid': ticker.get('bid'),
                            'ask': ticker.get('ask'),
                            'high': ticker.get('high'),
                            'low': ticker.get('low'),
                            'volume': ticker.get('quoteVolume'),
                            'timestamp': ticker.get('timestamp'),
                            'datetime': ticker.get('datetime', datetime.now().isoformat())
                        }
                
                self.logger.log_info(f"Tickers récupérés: {len(tickers)} paires USDT")
                return tickers
                
        except Exception as e:
            self.logger.log_error(f"Erreur lors de la récupération des tickers: {e}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Récupère les informations du compte
        
        Returns:
            Dictionnaire contenant les informations du compte
        """
        try:
            self.logger.log_execution('exchange', 'get_account_info')
            
            # Pour Binance, on peut utiliser fetch_balance qui contient aussi des infos
            balance = self.exchange.fetch_balance()
            
            account_info = {
                'exchange': self.exchange_config.get('name', 'unknown'),
                'timestamp': datetime.now().isoformat(),
                'balances_count': len([k for k, v in balance.items() 
                                     if isinstance(v, dict) and v.get('total', 0) > 0])
            }
            
            return account_info
            
        except Exception as e:
            self.logger.log_error(f"Erreur lors de la récupération des infos du compte: {e}")
            raise
    
    def normalize_symbol(self, asset: str, quote: str = 'USDT') -> str:
        """
        Normalise un symbole au format de l'exchange (ex: 'BTC' -> 'BTC/USDT')
        
        Args:
            asset: Asset de base (ex: 'BTC')
            quote: Quote currency (défaut: 'USDT')
        
        Returns:
            Symbole normalisé (ex: 'BTC/USDT')
        """
        return f"{asset}/{quote}"


# Instance globale (sera initialisée lors de l'import)
_exchange_instance: Optional[ExchangeManager] = None


def get_exchange(config_path: Optional[str] = None) -> ExchangeManager:
    """
    Obtient l'instance globale du gestionnaire d'exchange (singleton)
    
    Args:
        config_path: Chemin vers le fichier de configuration (uniquement au premier appel)
    
    Returns:
        Instance ExchangeManager
    """
    global _exchange_instance
    
    if _exchange_instance is None:
        _exchange_instance = ExchangeManager(config_path)
    
    return _exchange_instance
