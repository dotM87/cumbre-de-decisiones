import json
import os
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Decision:
    """Representa una decisión con sus efectos en los indicadores"""
    id: str
    text: str
    effects: Dict[str, int]
    description: str
    strategy_type: str = ""
    unlocks: str = None
    requires: str = None
    synergy_with: str = None
    synergy_bonus: Dict[str, int] = None

@dataclass
class Phase:
    """Representa una fase del juego"""
    id: int
    title: str
    question: str
    decisions: List[Decision]

class DataManager:
    """Gestiona la carga y manejo de datos del juego"""
    
    def __init__(self):
        self.phases_data = None
        self._load_phases()
    
    def _load_phases(self) -> None:
        """Carga las fases desde el archivo JSON"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'phases.json')
            with open(data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.phases_data = self._parse_phases(data['phases'])
        except FileNotFoundError:
            print("⚠️ Archivo phases.json no encontrado. Usando datos por defecto.")
            self.phases_data = self._get_default_phases()
        except json.JSONDecodeError as e:
            print(f"⚠️ Error al parsear JSON: {e}. Usando datos por defecto.")
            self.phases_data = self._get_default_phases()
    
    def _parse_phases(self, phases_json: List[Dict]) -> List[Phase]:
        """Convierte los datos JSON en objetos Phase"""
        phases = []
        for phase_data in phases_json:
            decisions = []
            for dec in phase_data['decisions']:
                decision = Decision(
                    id=dec['id'],
                    text=dec['text'],
                    effects=dec['effects'],
                    description=dec['description'],
                    strategy_type=dec.get('strategy_type', ''),
                    unlocks=dec.get('unlocks'),
                    requires=dec.get('requires'),
                    synergy_with=dec.get('synergy_with'),
                    synergy_bonus=dec.get('synergy_bonus')
                )
                decisions.append(decision)
            
            phase = Phase(
                id=phase_data['id'],
                title=phase_data['title'],
                question=phase_data['question'],
                decisions=decisions
            )
            phases.append(phase)
        
        return phases
    
    def _get_default_phases(self) -> List[Phase]:
        """Datos por defecto en caso de error al cargar JSON"""
        # Aquí incluirías una versión simplificada de las fases como fallback
        return [
            Phase(
                id=1,
                title="🏝️ ISLA 1 – Poder de negociación",
                question="¿Cómo gestionarias tu cadena de suministros?",
                decisions=[
                    Decision(
                        id="A",
                        text="A) Opción por defecto",
                        effects={"Liquidez": 10, "Reputación": 5},
                        description="Opción por defecto del sistema"
                    )
                ]
            )
        ]
    
    def get_phases(self) -> List[Phase]:
        """Retorna todas las fases del juego"""
        return self.phases_data
    
    def get_phase(self, phase_index: int) -> Phase:
        """Retorna una fase específica"""
        if 0 <= phase_index < len(self.phases_data):
            return self.phases_data[phase_index]
        return None