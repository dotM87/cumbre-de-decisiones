from dataclasses import dataclass
from typing import Dict
from enum import Enum

class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"
    COMPLETED = "completed"

class IndicatorType(Enum):
    LIQUIDEZ = "Liquidez"
    RENTABILIDAD = "Rentabilidad"
    REPUTACION = "Reputación"
    RIESGO_ACUMULADO = "Riesgo acumulado"
    SOSTENIBILIDAD_ESTRATEGICA = "Sostenibilidad estratégica"

class UIConfig:
    """Configuración de la interfaz de usuario"""
    
    # Colores del tema
    COLORS = {
        'bg_primary': '#1e1e2e',
        'bg_secondary': '#282a36',
        'bg_button': '#44475a',
        'bg_button_active': '#6272a4',
        'fg_primary': '#f8f8f2',
        'fg_secondary': '#6272a4',
        'fg_success': '#50fa7b',
        'fg_warning': '#ffb86c',
        'fg_error': '#ff5555',
        'fg_info': '#8be9fd'
    }
    
    # Fuentes
    FONTS = {
        'title': ('Arial', 20, 'bold'),
        'subtitle': ('Arial', 14, 'bold'),
        'normal': ('Arial', 11),
        'small': ('Arial', 9, 'italic'),
        'indicator': ('Arial', 10, 'bold')
    }
    
    # Dimensiones
    WINDOW_SIZE = "1000x700"
    PROGRESS_BAR_LENGTH = 300
    INDICATOR_LABEL_WIDTH = 20
    VALUE_LABEL_WIDTH = 8
    
    # Valores del juego
    INITIAL_INDICATOR_VALUE = 50
    MAX_PHASES = 5
    CRITICAL_THRESHOLD = 20
    FAILURE_THRESHOLD = 5

class GameConfig:
    """Configuración del juego"""
    
    INITIAL_INDICATORS = {
        IndicatorType.LIQUIDEZ.value: UIConfig.INITIAL_INDICATOR_VALUE,
        IndicatorType.RENTABILIDAD.value: UIConfig.INITIAL_INDICATOR_VALUE,
        IndicatorType.REPUTACION.value: UIConfig.INITIAL_INDICATOR_VALUE,
        IndicatorType.RIESGO_ACUMULADO.value: UIConfig.INITIAL_INDICATOR_VALUE,
        IndicatorType.SOSTENIBILIDAD_ESTRATEGICA.value: UIConfig.INITIAL_INDICATOR_VALUE
    }