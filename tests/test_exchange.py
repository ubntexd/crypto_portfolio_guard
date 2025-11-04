"""
Tests unitaires pour le module exchange
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import tempfile
import yaml
import os
from core.exchange import ExchangeManager, get_exchange


class TestExchangeManager:
    """Tests pour ExchangeManager"""
    
    @pytest.fixture
    def temp_config(self):
        """Créer un fichier de config temporaire pour les tests"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'exchange': {
                    'name': 'binance',
                    'api_key': 'test_api_key',
                    'api_secret': 'test_api_secret',
                    'sandbox': True,
                    'testnet': False
                },
                'database': {},
                'portfolio': {},
                'logging': {
                    'level': 'DEBUG',
                    'console': False,
                    'file': False
                }
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        yield temp_path
        
        # Nettoyage
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    @pytest.fixture
    def mock_ccxt_exchange(self):
        """Mock de l'exchange ccxt"""
        mock_exchange = MagicMock()
        
        # Mock pour fetch_ticker
        mock_ticker = {
            'last': 45000.0,
            'bid': 44999.0,
            'ask': 45001.0,
            'high': 46000.0,
            'low': 44000.0,
            'quoteVolume': 1000000.0,
            'timestamp': 1234567890000,
            'datetime': '2023-01-01T00:00:00.000Z'
        }
        mock_exchange.fetch_ticker.return_value = mock_ticker
        
        # Mock pour fetch_balance
        mock_balance = {
            'BTC': {'free': 0.5, 'used': 0.0, 'total': 0.5},
            'ETH': {'free': 2.0, 'used': 0.0, 'total': 2.0},
            'USDT': {'free': 1000.0, 'used': 0.0, 'total': 1000.0},
            'info': {},
            'free': {},
            'used': {},
            'total': {}
        }
        mock_exchange.fetch_balance.return_value = mock_balance
        
        # Mock pour fetch_tickers
        mock_tickers = {
            'BTC/USDT': mock_ticker,
            'ETH/USDT': {**mock_ticker, 'last': 3000.0},
            'BNB/USDT': {**mock_ticker, 'last': 400.0}
        }
        mock_exchange.fetch_tickers.return_value = mock_tickers
        
        return mock_exchange
    
    @patch('core.exchange.ccxt')
    def test_exchange_initialization(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test de l'initialisation de l'exchange"""
        # Réinitialiser les singletons
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        # Configurer le mock
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange = ExchangeManager(temp_config)
        
        assert exchange is not None
        assert exchange.exchange is not None
        assert exchange.exchange_config['name'] == 'binance'
    
    @patch('core.exchange.ccxt')
    def test_fetch_ticker(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test de récupération d'un ticker"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange = ExchangeManager(temp_config)
        ticker = exchange.fetch_ticker('BTC/USDT')
        
        assert ticker['symbol'] == 'BTC/USDT'
        assert ticker['last'] == 45000.0
        assert ticker['bid'] == 44999.0
        assert ticker['ask'] == 45001.0
        assert 'timestamp' in ticker
        assert 'datetime' in ticker
    
    @patch('core.exchange.ccxt')
    def test_fetch_balances(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test de récupération des balances"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange = ExchangeManager(temp_config)
        balances = exchange.fetch_balances()
        
        assert 'BTC' in balances
        assert 'ETH' in balances
        assert 'USDT' in balances
        assert balances['BTC']['total'] == 0.5
        assert balances['ETH']['total'] == 2.0
        assert 'info' not in balances
        assert 'free' not in balances
        assert 'used' not in balances
        assert 'total' not in balances
    
    @patch('core.exchange.ccxt')
    def test_fetch_tickers(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test de récupération de plusieurs tickers"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange = ExchangeManager(temp_config)
        
        # Test avec liste de symboles
        symbols = ['BTC/USDT', 'ETH/USDT']
        tickers = exchange.fetch_tickers(symbols)
        
        assert len(tickers) == 2
        assert 'BTC/USDT' in tickers
        assert 'ETH/USDT' in tickers
    
    @patch('core.exchange.ccxt')
    def test_fetch_tickers_all(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test de récupération de tous les tickers"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange = ExchangeManager(temp_config)
        tickers = exchange.fetch_tickers()
        
        # Devrait filtrer uniquement les paires USDT
        assert 'BTC/USDT' in tickers
        assert 'ETH/USDT' in tickers
        assert 'BNB/USDT' in tickers
    
    @patch('core.exchange.ccxt')
    def test_normalize_symbol(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test de normalisation des symboles"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange = ExchangeManager(temp_config)
        
        assert exchange.normalize_symbol('BTC') == 'BTC/USDT'
        assert exchange.normalize_symbol('ETH', 'BTC') == 'ETH/BTC'
    
    @patch('core.exchange.ccxt')
    def test_get_account_info(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test de récupération des informations du compte"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange = ExchangeManager(temp_config)
        account_info = exchange.get_account_info()
        
        assert account_info['exchange'] == 'binance'
        assert 'timestamp' in account_info
        assert 'balances_count' in account_info
    
    @patch('core.exchange.ccxt')
    def test_singleton_get_exchange(self, mock_ccxt, temp_config, mock_ccxt_exchange):
        """Test que get_exchange retourne une instance singleton"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        mock_exchange_class = MagicMock()
        mock_exchange_class.return_value = mock_ccxt_exchange
        mock_ccxt.binance = mock_exchange_class
        
        exchange1 = get_exchange(temp_config)
        exchange2 = get_exchange()
        
        # Devrait être la même instance
        assert exchange1 is exchange2
    
    @patch('core.exchange.ccxt')
    def test_exchange_not_supported(self, mock_ccxt, temp_config):
        """Test qu'une erreur est levée pour un exchange non supporté"""
        import core.exchange as ex
        import core.config_loader as cl
        import core.logger as lg
        ex._exchange_instance = None
        cl._config_instance = None
        lg._logger_instance = None
        
        # Modifier le config pour un exchange inexistant
        with open(temp_config, 'r') as f:
            config_data = yaml.safe_load(f)
        config_data['exchange']['name'] = 'nonexistent_exchange'
        with open(temp_config, 'w') as f:
            yaml.dump(config_data, f)
        
        # Supprimer l'attribut du mock pour simuler un exchange inexistant
        if hasattr(mock_ccxt, 'nonexistent_exchange'):
            delattr(mock_ccxt, 'nonexistent_exchange')
        
        # Utiliser un side_effect pour hasattr
        original_hasattr = hasattr
        def mock_hasattr(obj, name):
            if obj is mock_ccxt and name == 'nonexistent_exchange':
                return False
            return original_hasattr(obj, name)
        
        with patch('builtins.hasattr', side_effect=mock_hasattr):
            with pytest.raises(ValueError, match="non supporté"):
                ExchangeManager(temp_config)
