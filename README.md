# Exodus Trading System

Sistema automatizado de trading basado en estrategias avanzadas para el mercado de criptomonedas.

## 🚀 Características

- Backtesting avanzado con VectorBT
- Análisis temporal de estrategias
- Optimización de parámetros
- Múltiples estrategias de trading
- Validación y pruebas de estrés
- Análisis de rendimiento y métricas
- Integración con múltiples exchanges

## 📁 Estructura del Proyecto

```
exodus/
├── core/           # Funcionalidad central del sistema
├── strategies/     # Implementaciones de estrategias de trading
├── indicators/     # Indicadores técnicos personalizados
├── backtesting/   # Motor de backtesting y análisis
├── optimization/  # Optimización de parámetros
├── validation/    # Validación y pruebas
├── models/        # Modelos predictivos
├── data/          # Gestión de datos
├── utils/         # Utilidades generales
└── docs/          # Documentación

```

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/josetraderx/exodus-trading-system.git
cd exodus-trading-system
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 📊 Uso

### Backtesting
```python
python main.py --mode backtest --strategy nombre_estrategia --symbol AVAX-USD
```

### Optimización
```python
python main.py --mode optimize --strategy nombre_estrategia --symbol AVAX-USD
```

### Pruebas de Estrés
```python
python stress_test.py --strategy nombre_estrategia
```

## 📈 Resultados y Métricas

El sistema genera automáticamente:
- Gráficos de rendimiento
- Métricas de trading (Sharpe, Sortino, Win Rate, etc.)
- Análisis de drawdown
- Estadísticas por activo

## 🔍 Tests

Para ejecutar las pruebas:
```bash
pytest
```

## 📝 Licencia

Este proyecto es privado y confidencial.

## 👥 Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear una rama para tu feature
3. Commit de tus cambios
4. Push a la rama
5. Crear un Pull Request

## ⚠️ Disclaimer

Este software es para uso exclusivo de trading algorítmico. Opera bajo tu propio riesgo.