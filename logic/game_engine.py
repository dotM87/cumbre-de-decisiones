from typing import Dict, List
from config.settings import GameConfig, GameState
from logic.score_calculator import ScoreCalculator
from data.data_manager import DataManager, Phase

class GameEngine:
    """Maneja toda la lógica del juego"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.score_calculator = ScoreCalculator()
        self.indicators = {}
        self.current_phase = 0
        self.game_state = GameState.PLAYING
        self.phases = []
        self.max_phases = 0
        self.decision_history = {}
        self.unlocked_options = set()
        self.applied_synergies = set()
        self.reset_game()
    
    def reset_game(self):
        """Resetea el juego al estado inicial"""
        self.indicators = GameConfig.INITIAL_INDICATORS.copy()
        self.current_phase = 0
        self.game_state = GameState.PLAYING
        self.phases = self.data_manager.get_phases()
        self.max_phases = len(self.phases)
        self.decision_history = {}  # Tracking de decisiones por fase: {fase_id: opcion_id}
        self.unlocked_options = set()  # Opciones desbloqueadas: {"isla_4_E", "isla_4_F"}
        self.applied_synergies = set()   # Sinergias ya aplicadas para evitar duplicados
    
    def get_current_phase(self) -> Phase:
        """Retorna la fase actual con opciones filtradas según los unlocks"""
        if self.current_phase < self.max_phases:
            original_phase = self.phases[self.current_phase]
            
            # Filtrar decisiones según requirements y unlocks
            filtered_decisions = []
            for decision in original_phase.decisions:
                if self._is_decision_available(decision):
                    filtered_decisions.append(decision)
            
            # Crear nueva fase con decisiones filtradas
            filtered_phase = Phase(
                id=original_phase.id,
                title=original_phase.title,
                question=original_phase.question,
                decisions=filtered_decisions
            )
            
            return filtered_phase
        return None
    
    def _is_decision_available(self, decision) -> bool:
        """Verifica si una decisión está disponible según los requisitos"""
        # Verificar si tiene requires y si se cumple
        if hasattr(decision, 'requires') and decision.requires:
            if isinstance(decision.requires, str):
                # Formato: "isla_1_D"
                available = decision.requires in self.decision_history
                print(f"🔍 Opción {decision.id} requiere '{decision.requires}' - {'✅ Disponible' if available else '❌ Bloqueada'}")
                print(f"   Historial actual: {list(self.decision_history.keys())}")
                return available
            elif isinstance(decision.requires, list):
                # Formato: ["isla_2_C", "isla_3_B"]
                missing_requirements = [req for req in decision.requires if req not in self.decision_history]
                available = len(missing_requirements) == 0
                print(f"🔍 Opción {decision.id} requiere {decision.requires}")
                print(f"   Historial actual: {list(self.decision_history.keys())}")
                if missing_requirements:
                    print(f"   ❌ Bloqueada - Faltan: {missing_requirements}")
                else:
                    print("   ✅ Disponible - Todos los requisitos cumplidos")
                return available
        
        return True  # Si no tiene requires, está disponible
    
    def make_decision(self, decision_index: int) -> Dict:
        """Procesa una decisión y retorna el resultado"""
        if self.game_state != GameState.PLAYING:
            return {'success': False, 'message': 'Juego no está activo'}
        
        current_phase = self.get_current_phase()
        if not current_phase or decision_index >= len(current_phase.decisions):
            return {'success': False, 'message': 'Decisión inválida'}
        
        selected_decision = current_phase.decisions[decision_index]
        
        # Aplicar efectos base
        old_indicators = self.indicators.copy()
        self.indicators = self.score_calculator.apply_decision_effects(
            self.indicators, selected_decision.effects
        )
        
        # Guardar decisión en historial (formato: isla_X_Y)
        phase_key = f"isla_{current_phase.id}_{selected_decision.id}"
        self.decision_history[phase_key] = True
        print(f"📝 Decisión guardada: {phase_key}")
        print(f"📋 Historial actual: {list(self.decision_history.keys())}")
        
        # Verificar y activar unlocks
        self._check_unlocks(selected_decision)
        
        # Verificar y aplicar sinergias
        synergy_effects = self._check_synergies(selected_decision)
        if synergy_effects:
            self.indicators = self.score_calculator.apply_decision_effects(
                self.indicators, synergy_effects
            )
        
        # Calcular cambios para mostrar
        effects_list = self._calculate_effects_display(old_indicators, selected_decision.effects, synergy_effects)
        
        # Verificar estado del juego
        critical_indicators, failed_indicators = self.score_calculator.check_critical_indicators(self.indicators)
        
        result = {
            'success': True,
            'decision_text': selected_decision.text,
            'effects_list': effects_list,
            'critical_indicators': critical_indicators,
            'failed_indicators': failed_indicators
        }
        
        # Verificar game over
        if failed_indicators:
            self.game_state = GameState.GAME_OVER
            result['game_over'] = True
            return result
        
        # Verificar si se completó el juego ANTES de incrementar la fase
        if self.current_phase + 1 >= self.max_phases:
            self.game_state = GameState.COMPLETED
            result['game_completed'] = True
        else:
            # Solo avanzar fase si no se completó el juego
            self.current_phase += 1
        
        return result
    
    def _check_unlocks(self, decision):
        """Verifica y activa unlocks basados en la decisión"""
        if hasattr(decision, 'unlocks') and decision.unlocks:
            unlock_key = decision.unlocks
            self.unlocked_options.add(unlock_key)
            print(f"🔓 Desbloqueado: {unlock_key}")
            print(f"📋 Opciones desbloqueadas actuales: {list(self.unlocked_options)}")
        else:
            print(f"📝 Decisión {decision.id} no tiene unlocks")
    
    def _check_synergies(self, decision) -> Dict[str, int]:
        """Verifica y activa sinergias si aplican según las reglas específicas"""
        synergy_effects = {}
        current_phase_id = self.current_phase + 1
        decision_id = decision.id
        
        print(f"🔍 Verificando sinergias para isla_{current_phase_id}_{decision_id}")
        
        # Verificar sinergia definida en JSON (sistema principal)
        if hasattr(decision, 'synergy_with') and hasattr(decision, 'synergy_bonus'):
            synergy_key = decision.synergy_with
            print(f"   Buscando sinergia con: {synergy_key}")
            print(f"   Decisiones en historial: {list(self.decision_history.keys())}")
            
            # Verificar si la condición de sinergia se cumple
            if synergy_key in self.decision_history:
                synergy_id = f"{synergy_key}_with_isla_{current_phase_id}_{decision_id}"
                
                # Aplicar sinergia solo una vez
                if synergy_id not in self.applied_synergies:
                    synergy_effects = decision.synergy_bonus.copy()
                    self.applied_synergies.add(synergy_id)
                    print(f"✨ Sinergia activada: {synergy_key} + isla_{current_phase_id}_{decision_id}")
                    print(f"   Efectos: {synergy_effects}")
                else:
                    print(f"⚠️ Sinergia {synergy_id} ya fue aplicada anteriormente")
            else:
                print(f"❌ Sinergia NO activada: {synergy_key} no encontrado en historial")
        else:
            print("   No tiene sinergia definida")
        
        return synergy_effects
    
    def _calculate_effects_display(self, old_indicators: Dict[str, float], 
                                 base_effects: Dict[str, int], 
                                 synergy_effects: Dict[str, int] = None) -> List[str]:
        """Calcula la lista de efectos para mostrar, incluyendo sinergias"""
        effects_list = []
        
        # Combinar efectos base y de sinergia
        all_effects = base_effects.copy()
        if synergy_effects:
            for indicator, value in synergy_effects.items():
                all_effects[indicator] = all_effects.get(indicator, 0) + value
        
        for indicator, change in all_effects.items():
            if indicator in old_indicators:
                old_value = old_indicators[indicator]
                new_value = self.indicators[indicator]
                
                synergy_note = ""
                if synergy_effects and indicator in synergy_effects:
                    synergy_change = synergy_effects[indicator]
                    synergy_note = f" (✨+{synergy_change} sinergia)"
                
                if change > 0:
                    effects_list.append(f"📈 {indicator}: +{change}% ({old_value:.1f}% → {new_value:.1f}%){synergy_note}")
                elif change < 0:
                    effects_list.append(f"📉 {indicator}: {change}% ({old_value:.1f}% → {new_value:.1f}%){synergy_note}")
        
        return effects_list
    
    def get_final_results(self) -> Dict:
        """Calcula y retorna los resultados finales"""
        avg_score, category, message, color = self.score_calculator.calculate_final_score(self.indicators)
        
        return {
            'avg_score': avg_score,
            'category': category,
            'message': message,
            'color': color,
            'indicators': self.indicators.copy()
        }
    
    def get_indicators(self) -> Dict[str, float]:
        """Retorna los indicadores actuales"""
        return self.indicators.copy()
    
    def get_game_info(self) -> Dict:
        """Retorna información general del juego"""
        return {
            'current_phase': self.current_phase,
            'max_phases': self.max_phases,
            'game_state': self.game_state,
            'indicators': self.get_indicators()
        }