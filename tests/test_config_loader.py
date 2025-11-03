"""
Tests unitaires pour le module config_loader
"""

import pytest
import yaml
from pathlib import Path
import tempfile
import os
from core.config_loader import ConfigLoader, get_config


class TestConfigLoader:
    """Tests pour ConfigLoader"""
    
    def test_load_valid_config(self):
        """Test du chargement d'une configuration valide"""
        # Créer un fichier de config temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'exchange': {
                    'name': 'binance',
                    'api_key': 'test_key',
                    'sandbox': True
                },
                'database': {
                    'type': 'sqlite',
                    'sqlite': {'path': 'test.db'}
                },
                'portfolio': {
                    'base_currency': 'USDT'
                },
                'logging': {
                    'level': 'INFO'
                }
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigLoader(temp_path)
            
            # Vérifier que la config est chargée
            assert config.config is not None
            assert config.get('exchange.name') == 'binance'
            assert config.get('exchange.api_key') == 'test_key'
            assert config.get('database.type') == 'sqlite'
            
        finally:
            os.unlink(temp_path)
    
    def test_load_nonexistent_config(self):
        """Test qu'une erreur est levée si le fichier n'existe pas"""
        with pytest.raises(FileNotFoundError):
            ConfigLoader('/nonexistent/path/settings.yaml')
    
    def test_get_method_with_dot_notation(self):
        """Test de la méthode get avec notation pointée"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'exchange': {
                    'name': 'binance',
                    'api_key': 'test_key'
                }
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigLoader(temp_path)
            
            assert config.get('exchange.name') == 'binance'
            assert config.get('exchange.api_key') == 'test_key'
            assert config.get('exchange.nonexistent', 'default') == 'default'
            assert config.get('nonexistent.section', None) is None
            
        finally:
            os.unlink(temp_path)
    
    def test_get_method_without_dot_notation(self):
        """Test de la méthode get sans notation pointée"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {'test_key': 'test_value'}
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigLoader(temp_path)
            assert config.get('test_key') == 'test_value'
            
        finally:
            os.unlink(temp_path)
    
    def test_set_method(self):
        """Test de la méthode set pour modifier la config"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {'exchange': {'name': 'binance'}}
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigLoader(temp_path)
            
            config.set('exchange.api_key', 'new_key')
            assert config.get('exchange.api_key') == 'new_key'
            
            config.set('new_section.key', 'value')
            assert config.get('new_section.key') == 'value'
            
        finally:
            os.unlink(temp_path)
    
    def test_get_exchange_config(self):
        """Test de get_exchange_config()"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'exchange': {
                    'name': 'binance',
                    'api_key': 'test_key'
                }
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigLoader(temp_path)
            exchange_config = config.get_exchange_config()
            
            assert exchange_config['name'] == 'binance'
            assert exchange_config['api_key'] == 'test_key'
            
        finally:
            os.unlink(temp_path)
    
    def test_get_database_config(self):
        """Test de get_database_config()"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'database': {
                    'type': 'sqlite',
                    'sqlite': {'path': 'test.db'}
                }
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigLoader(temp_path)
            db_config = config.get_database_config()
            
            assert db_config['type'] == 'sqlite'
            assert db_config['sqlite']['path'] == 'test.db'
            
        finally:
            os.unlink(temp_path)
    
    def test_get_logging_config(self):
        """Test de get_logging_config()"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'logging': {
                    'level': 'DEBUG',
                    'console': True
                }
            }
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigLoader(temp_path)
            logging_config = config.get_logging_config()
            
            assert logging_config['level'] == 'DEBUG'
            assert logging_config['console'] is True
            
        finally:
            os.unlink(temp_path)
    
    def test_singleton_get_config(self):
        """Test que get_config retourne une instance singleton"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {'test': 'value'}
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            # Réinitialiser le singleton pour le test
            import core.config_loader as cl
            cl._config_instance = None
            
            config1 = get_config(temp_path)
            config2 = get_config()
            
            # Devrait être la même instance
            assert config1 is config2
            
        finally:
            os.unlink(temp_path)
    
    def test_invalid_yaml(self):
        """Test qu'une erreur est levée pour un YAML invalide"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('invalid: yaml: content: [unclosed')
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Erreur de syntaxe"):
                ConfigLoader(temp_path)
        finally:
            os.unlink(temp_path)
