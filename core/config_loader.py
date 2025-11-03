"""
Module de chargement et validation de la configuration
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger


class ConfigLoader:
    """Chargeur de configuration depuis settings.yaml"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise le chargeur de configuration
        
        Args:
            config_path: Chemin vers le fichier settings.yaml
                        Si None, cherche dans config/settings.yaml
        """
        if config_path is None:
            # Chercher depuis la racine du projet
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "settings.yaml"
        
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Charge la configuration depuis le fichier YAML"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Fichier de configuration non trouvé: {self.config_path}"
            )
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
            
            logger.info(f"Configuration chargée depuis {self.config_path}")
            self._validate_config()
            
        except yaml.YAMLError as e:
            raise ValueError(f"Erreur de syntaxe dans le fichier YAML: {e}")
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement de la configuration: {e}")
    
    def _validate_config(self) -> None:
        """Valide la structure de base de la configuration"""
        required_sections = ['exchange', 'database', 'portfolio', 'logging']
        
        for section in required_sections:
            if section not in self.config:
                logger.warning(f"Section '{section}' manquante dans la configuration")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration (notation pointée supportée)
        
        Args:
            key: Clé de configuration (ex: 'exchange.api_key' ou 'exchange')
            default: Valeur par défaut si la clé n'existe pas
        
        Returns:
            Valeur de configuration ou default
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Définit une valeur de configuration (notation pointée supportée)
        
        Args:
            key: Clé de configuration
            value: Valeur à définir
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.debug(f"Configuration mise à jour: {key} = {value}")
    
    def reload(self) -> None:
        """Recharge la configuration depuis le fichier"""
        self._load_config()
        logger.info("Configuration rechargée")
    
    def get_exchange_config(self) -> Dict[str, Any]:
        """Récupère la configuration de l'exchange"""
        return self.get('exchange', {})
    
    def get_database_config(self) -> Dict[str, Any]:
        """Récupère la configuration de la base de données"""
        return self.get('database', {})
    
    def get_portfolio_config(self) -> Dict[str, Any]:
        """Récupère la configuration du portefeuille"""
        return self.get('portfolio', {})
    
    def get_rules_config(self) -> Dict[str, Any]:
        """Récupère la configuration des règles automatiques"""
        return self.get('rules', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Récupère la configuration du logging"""
        return self.get('logging', {})
    
    def get_web_config(self) -> Dict[str, Any]:
        """Récupère la configuration du serveur web"""
        return self.get('web', {})


# Instance globale de configuration (sera initialisée lors de l'import)
_config_instance: Optional[ConfigLoader] = None


def get_config(config_path: Optional[str] = None) -> ConfigLoader:
    """
    Obtient l'instance globale de configuration (singleton)
    
    Args:
        config_path: Chemin vers le fichier de configuration (uniquement au premier appel)
    
    Returns:
        Instance ConfigLoader
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = ConfigLoader(config_path)
    
    return _config_instance
