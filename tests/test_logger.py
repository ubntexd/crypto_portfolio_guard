"""
Tests unitaires pour le module logger
"""

import pytest
import yaml
from pathlib import Path
import tempfile
import os
from core.logger import PortfolioLogger, get_logger


class TestPortfolioLogger:
    """Tests pour PortfolioLogger"""
    
    @pytest.fixture(autouse=True)
    def reset_singletons(self):
        """Réinitialiser les singletons avant chaque test"""
        import core.logger as lg
        import core.config_loader as cl
        lg._logger_instance = None
        cl._config_instance = None
        yield
        # Nettoyage après le test
        lg._logger_instance = None
        cl._config_instance = None
    
    @pytest.fixture
    def temp_config(self):
        """Créer un fichier de config temporaire pour les tests"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'logging': {
                    'level': 'DEBUG',
                    'console': True,
                    'file': True,
                    'directory': 'test_logs',
                    'rotation': '00:00',
                    'retention': '7 days',
                    'compression': 'zip',
                    'format': '{time} | {level} | {message}'
                },
                'exchange': {},
                'database': {},
                'portfolio': {}
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        yield temp_path
        
        # Nettoyage
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        # Nettoyer les logs de test
        test_logs_dir = Path('test_logs')
        if test_logs_dir.exists():
            import shutil
            shutil.rmtree(test_logs_dir)
    
    def test_logger_initialization(self, temp_config):
        """Test de l'initialisation du logger"""
        logger = PortfolioLogger(temp_config)
        assert logger is not None
        assert logger.config is not None
        # Vérifier que la config contient les clés attendues
        assert 'level' in logger.config or logger.config.get('level') == 'DEBUG'
    
    def test_log_info(self, temp_config):
        """Test de log_info()"""
        logger = PortfolioLogger(temp_config)
        logger.log_info("Test info message")
        # Si pas d'exception, c'est OK
    
    def test_log_debug(self, temp_config):
        """Test de log_debug()"""
        logger = PortfolioLogger(temp_config)
        logger.log_debug("Test debug message")
    
    def test_log_warning(self, temp_config):
        """Test de log_warning()"""
        logger = PortfolioLogger(temp_config)
        logger.log_warning("Test warning message")
    
    def test_log_error(self, temp_config):
        """Test de log_error()"""
        logger = PortfolioLogger(temp_config)
        logger.log_error("Test error message")
    
    def test_log_critical(self, temp_config):
        """Test de log_critical()"""
        logger = PortfolioLogger(temp_config)
        logger.log_critical("Test critical message")
    
    def test_log_execution(self, temp_config):
        """Test de log_execution()"""
        logger = PortfolioLogger(temp_config)
        logger.log_execution('exchange', 'fetch_balances', {'coins': ['BTC', 'ETH']})
        logger.log_execution('portfolio', 'calculate_pnl')
    
    def test_log_decision(self, temp_config):
        """Test de log_decision()"""
        logger = PortfolioLogger(temp_config)
        logger.log_decision(
            'rules',
            'convert_to_usdt',
            'Profit threshold exceeded',
            asset='BTC',
            amount=0.5
        )
    
    def test_log_transaction(self, temp_config):
        """Test de log_transaction()"""
        logger = PortfolioLogger(temp_config)
        logger.log_transaction('sell', 'BTC', 0.5, price=45000.0)
        logger.log_transaction('buy', 'ETH', 2.0)
    
    def test_log_alert(self, temp_config):
        """Test de log_alert()"""
        logger = PortfolioLogger(temp_config)
        logger.log_alert('profit_threshold', 'BTC has exceeded profit threshold', 'WARNING')
        logger.log_alert('loss_threshold', 'ETH has dropped below threshold', 'ERROR')
    
    def test_logger_creates_log_directory(self, temp_config):
        """Test que le logger crée le répertoire de logs"""
        # Utiliser le chemin absolu depuis le répertoire de travail
        test_logs_dir = Path.cwd() / 'test_logs'
        if test_logs_dir.exists():
            import shutil
            shutil.rmtree(test_logs_dir)
        
        logger = PortfolioLogger(temp_config)
        
        # Le répertoire devrait être créé seulement si file: True dans la config
        # Vérifier que la config indique file: True
        if logger.config.get('file', True):
            # Le logger crée le répertoire dans le répertoire de travail courant
            assert test_logs_dir.exists() or Path('test_logs').exists()
    
    def test_singleton_get_logger(self, temp_config):
        """Test que get_logger retourne une instance singleton"""
        logger1 = get_logger(temp_config)
        logger2 = get_logger()
        
        # Devrait être la même instance
        assert logger1 is logger2
    
    def test_logger_with_console_only(self):
        """Test du logger avec console seulement (pas de fichier)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'logging': {
                    'level': 'INFO',
                    'console': True,
                    'file': False
                },
                'exchange': {},
                'database': {},
                'portfolio': {}
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            logger = PortfolioLogger(temp_path)
            logger.log_info("Console only test")
            
        finally:
            os.unlink(temp_path)
