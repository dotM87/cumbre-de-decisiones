from typing import Dict, Tuple
from config.settings import UIConfig

class ScoreCalculator:
    """Maneja todos los cálculos relacionados con puntuaciones e indicadores"""
    
    @staticmethod
    def get_indicator_color(value: float) -> str:
        """Determina el color del indicador según su valor"""
        if value < UIConfig.CRITICAL_THRESHOLD:
            return UIConfig.COLORS['fg_error']
        elif value < 50:
            return UIConfig.COLORS['fg_warning']
        else:
            return UIConfig.COLORS['fg_success']
    
    @staticmethod
    def get_progressbar_style(value: float) -> str:
        """Determina el estilo de la barra de progreso"""
        if value < UIConfig.CRITICAL_THRESHOLD:
            return "Red.Horizontal.TProgressbar"
        elif value < 50:
            return "Orange.Horizontal.TProgressbar"
        else:
            return "Green.Horizontal.TProgressbar"
    
    @staticmethod
    def calculate_final_score(indicators: Dict[str, float]) -> Tuple[float, str, str, str]:
        """Calcula la puntuación final y determina la categoría"""
        total_score = sum(indicators.values())
        avg_score = total_score / len(indicators)
        
        if avg_score >= 70:
            category = "🏆 EXCELENTE"
            message = "¡Felicidades! Has logrado construir una empresa sólida y próspera."
            color = UIConfig.COLORS['fg_success']
        elif avg_score >= 50:
            category = "👍 BUENO"
            message = "Buen trabajo. Tu empresa está en una posición estable con potencial de crecimiento."
            color = UIConfig.COLORS['fg_info']
        elif avg_score >= 30:
            category = "⚠️ REGULAR"
            message = "Tu empresa sobrevivió, pero necesita mejoras importantes para prosperar."
            color = UIConfig.COLORS['fg_warning']
        else:
            category = "❌ CRÍTICO"
            message = "Tu empresa está en serios problemas. Es momento de replantear la estrategia."
            color = UIConfig.COLORS['fg_error']
        
        return avg_score, category, message, color
    
    @staticmethod
    def check_critical_indicators(indicators: Dict[str, float]) -> Tuple[list, list]:
        """Verifica indicadores críticos y fallidos"""
        critical_indicators = [
            name for name, value in indicators.items() 
            if value < UIConfig.CRITICAL_THRESHOLD
        ]
        failed_indicators = [
            name for name, value in indicators.items() 
            if value < UIConfig.FAILURE_THRESHOLD
        ]
        
        return critical_indicators, failed_indicators
    
    @staticmethod
    def apply_decision_effects(indicators: Dict[str, float], effects: Dict[str, int]) -> Dict[str, float]:
        """Aplica los efectos de una decisión a los indicadores"""
        new_indicators = indicators.copy()
        for indicator, change in effects.items():
            if indicator in new_indicators:
                old_value = new_indicators[indicator]
                new_indicators[indicator] = max(0, min(100, old_value + change))
        
        return new_indicators