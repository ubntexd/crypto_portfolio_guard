"""
Module de journalisation avec rotation automatique et sauvegarde
"""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger
from .config_loader import get_config


class PortfolioLogger:
    """Gestionnaire de logs avec rotation journalière et sauvegarde en DB"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise le système de logging
        
        Args:
            config_path: Chemin vers le fichier de configuration
        """
        self.config = get_config(config_path).get_logging_config()
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Configure le logger selon la configuration"""
        # Supprimer le handler par défaut
        logger.remove()
        
        # Configuration de base
        log_level = self.config.get('level', 'INFO')
        log_format = self.config.get(
            'format',
            "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
        )
        
        # Handler console
        if self.config.get('console', True):
            logger.add(
                sys.stderr,
                format=log_format,
                level=log_level,
                colorize=True,
                backtrace=True,
                diagnose=True
            )
        
        # Handler fichier avec rotation
        if self.config.get('file', True):
            log_dir = Path(self.config.get('directory', 'logs'))
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / "portfolio_{time:YYYY-MM-DD}.log"
            rotation = self.config.get('rotation', '00:00')  # Rotation à minuit
            retention = self.config.get('retention', '30 days')
            compression = self.config.get('compression', 'zip')
            
            logger.add(
                str(log_file),
                format=log_format,
                level=log_level,
                rotation=rotation,
                retention=retention,
                compression=compression,
                backtrace=True,
                diagnose=True,
                enqueue=True  # Thread-safe
            )
        
        logger.info("Système de logging initialisé")
    
    def log_info(self, message: str, **kwargs) -> None:
        """Enregistre un message d'information"""
        logger.info(message, **kwargs)
    
    def log_debug(self, message: str, **kwargs) -> None:
        """Enregistre un message de debug"""
        logger.debug(message, **kwargs)
    
    def log_warning(self, message: str, **kwargs) -> None:
        """Enregistre un avertissement"""
        logger.warning(message, **kwargs)
    
    def log_error(self, message: str, **kwargs) -> None:
        """Enregistre une erreur"""
        logger.error(message, **kwargs)
    
    def log_critical(self, message: str, **kwargs) -> None:
        """Enregistre une erreur critique"""
        logger.critical(message, **kwargs)
    
    def log_execution(self, module: str, action: str, details: Optional[dict] = None) -> None:
        """
        Enregistre une exécution de module/action
        
        Args:
            module: Nom du module (ex: 'exchange', 'portfolio', 'rules')
            action: Action effectuée (ex: 'fetch_balances', 'calculate_pnl')
            details: Détails supplémentaires à logger
        """
        details_str = f" | Details: {details}" if details else ""
        logger.info(f"EXECUTION | Module: {module} | Action: {action}{details_str}")
    
    def log_decision(self, module: str, decision: str, reason: str, **kwargs) -> None:
        """
        Enregistre une décision prise par le système
        
        Args:
            module: Module qui a pris la décision
            decision: Décision prise (ex: 'convert_to_usdt', 'rebase_price')
            reason: Raison de la décision
        """
        logger.info(
            f"DECISION | Module: {module} | Decision: {decision} | Reason: {reason}",
            **kwargs
        )
    
    def log_transaction(self, transaction_type: str, asset: str, amount: float, 
                       price: Optional[float] = None, **kwargs) -> None:
        """
        Enregistre une transaction
        
        Args:
            transaction_type: Type de transaction (ex: 'buy', 'sell', 'convert')
            asset: Asset concerné (ex: 'BTC', 'ETH')
            amount: Montant de la transaction
            price: Prix de la transaction (optionnel)
        """
        price_str = f" | Price: {price}" if price else ""
        logger.info(
            f"TRANSACTION | Type: {transaction_type} | Asset: {asset} | "
            f"Amount: {amount}{price_str}",
            **kwargs
        )
    
    def log_alert(self, alert_type: str, message: str, severity: str = 'WARNING', **kwargs) -> None:
        """
        Enregistre une alerte
        
        Args:
            alert_type: Type d'alerte (ex: 'profit_threshold', 'loss_threshold')
            message: Message d'alerte
            severity: Niveau de sévérité (INFO, WARNING, ERROR, CRITICAL)
        """
        log_method = getattr(logger, severity.lower(), logger.warning)
        log_method(f"ALERT | Type: {alert_type} | Message: {message}", **kwargs)


# Instance globale de logger (sera initialisée lors de l'import)
_logger_instance: Optional[PortfolioLogger] = None


def get_logger(config_path: Optional[str] = None) -> PortfolioLogger:
    """
    Obtient l'instance globale du logger (singleton)
    
    Args:
        config_path: Chemin vers le fichier de configuration (uniquement au premier appel)
    
    Returns:
        Instance PortfolioLogger
    """
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = PortfolioLogger(config_path)
    
    return _logger_instance


# Exporter directement le logger loguru pour compatibilité
__all__ = ['PortfolioLogger', 'get_logger', 'logger']
