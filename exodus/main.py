"""Punto de entrada principal para el sistema de trading."""
import os
import sys
import logging
import argparse
import pandas as pd
from datetime import datetime

# Importar módulos del sistema
from exodus.utils.logger_config import LoggerConfig
from exodus.core.parameters_pinescript import TradingParameters
from exodus.data.timestamp_validator import TimestampValidator
from exodus.validation.data_validation import perform_comprehensive_data_validation
from exodus.utils.system_monitor import SystemMonitor
from exodus.models import EnsembleLearner
from exodus.strategies.trading_strategy_pinescript import PineScriptTradingStrategy
from exodus.data import DataValidator

def parse_arguments():
    """
    Parsea los argumentos de línea de comandos.
    
    Returns:
        argparse.Namespace: Argumentos parseados
    """
    parser = argparse.ArgumentParser(description='Sistema de trading con machine learning')
    
    # Argumentos generales
    parser.add_argument('--mode', type=str, choices=['train', 'predict', 'backtest', 'optimize'],
                        default='backtest', help='Modo de operación')
    parser.add_argument('--data', type=str, required=True, help='Ruta al archivo de datos')
    parser.add_argument('--output', type=str, default='output', help='Directorio de salida')
    
    # Argumentos específicos para entrenamiento
    parser.add_argument('--epochs', type=int, default=10, help='Número de épocas para LSTM')
    parser.add_argument('--sequence-length', type=int, default=20, help='Longitud de secuencia para LSTM')
    
    # Argumentos específicos para backtesting
    parser.add_argument('--initial-capital', type=float, default=350, help='Capital inicial')
    parser.add_argument('--fee', type=float, default=0.0005, help='Comisión por operación')
    
    # Argumentos específicos para optimización
    parser.add_argument('--n-trials', type=int, default=30, help='Número de pruebas para optimización')
    
    return parser.parse_args()

def setup_environment():
    """
    Configura el entorno de ejecución con monitoreo mejorado.
    
    Returns:
        logging.Logger: Logger configurado
        SystemMonitor: Monitor del sistema configurado
    """
    logger = LoggerConfig.setup()
    
    # Inicializar monitor del sistema
    system_monitor = SystemMonitor()
    
    # Registrar estado inicial del sistema
    initial_metrics = system_monitor.log_system_metrics()
    logger.info(f"Estado inicial del sistema: {initial_metrics}")
    
    # Crear directorio de salida si no existe
    if not os.path.exists('output'):
        os.makedirs('output')
        logger.info("Directorio de salida creado: output")
    
    # Configurar entorno de TensorFlow
    try:
        import tensorflow as tf
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        
        # Verificar disponibilidad de GPU
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            logger.info(f"GPU disponible: {gpus}")
            # Configurar memoria de GPU
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        else:
            logger.warning("No se detectó GPU. El entrenamiento será más lento.")
    except ImportError:
        logger.warning("TensorFlow no está instalado. No se podrá usar LSTM.")
    
    return logger, system_monitor

def load_and_validate_data(file_path: str, logger: logging.Logger):
    """
    Carga y valida los datos de trading.
    
    Args:
        file_path: Ruta al archivo de datos
        logger: Logger para registrar mensajes
        
    Returns:
        pd.DataFrame: DataFrame con los datos validados
    """
    logger.info(f"Cargando datos desde: {file_path}")
    
    try:
        # Validar timestamps
        timestamp_validator = TimestampValidator(logger=logger)
        df = timestamp_validator.validate(file_path)
        
        # Corregir: Asegurar que el DataFrame no está vacío después de la validación
        if df.empty:
            logger.error("La validación resultó en un DataFrame vacío")
            raise ValueError("No hay datos válidos después de la validación")
            
        # Validación completa de datos
        df = perform_comprehensive_data_validation(df)
        
        logger.info(f"Datos cargados y validados. Registros: {len(df)}")
        return df
        
    except Exception as e:
        logger.error(f"Error al cargar datos: {str(e)}")
        raise

def main():
    """
    Función principal del sistema.
    """
    # Parsear argumentos
    args = parse_arguments()
    
    # Configurar entorno
    logger, system_monitor = setup_environment()
    logger.info(f"Iniciando sistema en modo: {args.mode}")
    
    try:
        # Cargar y validar datos
        df = load_and_validate_data(args.data, logger)
        
        # Crear parámetros de trading
        params = TradingParameters()
        
        # Actualizar parámetros desde argumentos
        if args.epochs:
            params.lstm_epochs = args.epochs
        if args.sequence_length:
            params.sequence_length = args.sequence_length
        if args.initial_capital:
            params.capital_inicial = args.initial_capital
        
        # Validar parámetros
        params.validate()
        
        # Monitorear recursos iniciales
        initial_metrics = system_monitor.log_system_metrics()
        logger.info(f"Recursos iniciales: {initial_metrics}")
        
        # Ejecutar modo seleccionado
        if args.mode == 'train':
            logger.info("Iniciando modo de entrenamiento")
            # Aquí se implementaría la lógica de entrenamiento
            system_monitor.log_system_metrics()  # Monitorear después del entrenamiento
            
        elif args.mode == 'predict':
            logger.info("Iniciando modo de predicción")
            # Aquí se implementaría la lógica de predicción
            system_monitor.log_system_metrics()  # Monitorear después de la predicción
            
        elif args.mode == 'backtest':
            logger.info("Iniciando modo de backtesting")
            # Aquí se implementaría la lógica de backtesting
            system_monitor.log_system_metrics()  # Monitorear después del backtesting
            
        elif args.mode == 'optimize':
            logger.info("Iniciando modo de optimización")
            # Aquí se implementaría la lógica de optimización
            system_monitor.log_system_metrics()  # Monitorear después de la optimización
        
        # Monitorear recursos finales
        final_metrics = system_monitor.log_system_metrics()
        logger.info(f"Recursos finales: {final_metrics}")
        
        logger.info(f"Ejecución en modo {args.mode} completada con éxito")
        
    except Exception as e:
        logger.error(f"Error en la ejecución: {str(e)}")
        # Registrar métricas en caso de error
        error_metrics = system_monitor.log_system_metrics()
        logger.error(f"Estado del sistema al momento del error: {error_metrics}")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())