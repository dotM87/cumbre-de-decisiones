import tkinter as tk
import sys
import os
import json

# Agregar directorios al path
sys.path.append(os.path.dirname(__file__))

from ui.ui_manager import UIManager
from logic.game_engine import GameEngine
from config.settings import GameState

class BusinessSimulator:
    """Simulador empresarial refactorizado"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Simulador Estratégico Empresarial")
        self.root.geometry("1200x800")  # Ventana más grande para mejor UI
        self.root.configure(bg='#1a1b23')  # Fondo oscuro moderno
        self.root.resizable(True, True)
        
        # Configurar estilo moderno
        self._setup_window_style()
        
        try:
            self.game_engine = GameEngine()
            self.ui_manager = UIManager(self.root, self.handle_decision)
            
            # Mostrar pantalla de inicio en lugar de iniciar el juego directamente
            self.show_start_screen()
        except Exception as e:
            print(f"❌ Error en inicialización: {e}")
            raise
    
    def _setup_window_style(self):
        """Configura el estilo moderno de la ventana en pantalla completa"""
        try:
            # Configurar pantalla completa
            self.root.state('zoomed')  # Pantalla completa en Windows
            # Para otros sistemas operativos podrías usar:
            # self.root.attributes('-fullscreen', True)
        except Exception as e:
            print(f"⚠️ Error configurando pantalla completa: {e}")
            # Fallback a ventana maximizada manualmente
            try:
                width = self.root.winfo_screenwidth()
                height = self.root.winfo_screenheight()
                self.root.geometry(f"{width}x{height}+0+0")
            except Exception as e2:
                print(f"⚠️ Error configurando ventana: {e2}")
    
    def start_game(self):
        """Inicia o reinicia el juego"""
        try:
            print("🔄 Iniciando nuevo juego...")
            self.game_engine.reset_game()
            self.update_ui()
            self.show_current_phase()
            print("✅ Juego iniciado correctamente")
        except Exception as e:
            print(f"❌ Error al iniciar juego: {e}")
            raise
    
    def update_ui(self):
        """Actualiza la interfaz con el estado actual"""
        try:
            game_info = self.game_engine.get_game_info()
            self.ui_manager.update_indicators_display(
                game_info['indicators'],
                game_info['current_phase'],
                game_info['max_phases']
            )
        except Exception as e:
            print(f"❌ Error al actualizar UI: {e}")
            raise
    
    def show_current_phase(self):
        """Muestra la fase actual con manejo robusto de datos"""
        try:
            current_phase = self.game_engine.get_current_phase()
            
            # Debug info
            print(f"🔍 Mostrando fase actual...")
            print(f"   Tipo: {type(current_phase)}")
            print(f"   Estado del juego: {self.game_engine.game_state}")
            
            if current_phase and self.game_engine.game_state == GameState.PLAYING:
                # Convertir a diccionario sin importar el tipo original
                phase_data = self._normalize_phase_data(current_phase)
                print(f"   Datos normalizados: {phase_data.get('title', 'Sin título')}")
                
                self.ui_manager.show_phase(phase_data)
            else:
                print("🏁 Mostrando resultados finales...")
                self.show_final_results()
                
        except Exception as e:
            print(f"❌ Error al mostrar fase: {e}")
            print(f"   Tipo de current_phase: {type(current_phase)}")
            print(f"   Contenido: {current_phase}")
            
            # Intentar mostrar una fase de emergencia
            self._show_emergency_phase()
    
    def _normalize_phase_data(self, phase_data):
        """Normaliza los datos de fase independientemente de su formato original"""
        try:
            # Si es None o vacío
            if not phase_data:
                return self._get_default_phase()
            
            # Si es un objeto Phase (formato correcto)
            if hasattr(phase_data, 'title') and hasattr(phase_data, 'decisions'):
                # Convertir decisiones a formato dict
                options = []
                for decision in phase_data.decisions:
                    option = {
                        'title': decision.text,
                        'description': decision.description,
                        'strategy_type': getattr(decision, 'strategy_type', ''),
                        'effects': decision.effects,
                        'synergy_with': getattr(decision, 'synergy_with', None),
                        'synergy_bonus': getattr(decision, 'synergy_bonus', None),
                        'requires': getattr(decision, 'requires', None),
                        'unlocks': getattr(decision, 'unlocks', None)
                    }
                    options.append(option)
                
                return {
                    'title': phase_data.title,
                    'description': getattr(phase_data, 'context', ''),
                    'context': getattr(phase_data, 'context', ''),
                    'question': phase_data.question,
                    'options': options,
                    'id': phase_data.id,
                    'phase_number': self.game_engine.current_phase + 1
                }
            
            # Si es un diccionario (JSON)
            elif isinstance(phase_data, dict):
                return {
                    'title': phase_data.get('title', 'Fase sin título'),
                    'description': phase_data.get('description', 'Sin descripción'),
                    'context': phase_data.get('context', ''),
                    'question': phase_data.get('question', ''),
                    'options': phase_data.get('options', []),
                    'id': phase_data.get('id', f'fase_{self.game_engine.current_phase}'),
                    'phase_number': phase_data.get('phase_number', self.game_engine.current_phase + 1)
                }
            
            # Formato desconocido
            else:
                print(f"⚠️ Formato de fase desconocido: {type(phase_data)}")
                return self._get_default_phase()
                
        except Exception as e:
            print(f"❌ Error normalizando datos de fase: {e}")
            return self._get_default_phase()
    
    def _get_default_phase(self):
        """Retorna una fase por defecto en caso de error"""
        return {
            'title': f'Fase {self.game_engine.current_phase + 1}',
            'description': 'Error cargando datos de la fase. Usando valores por defecto.',
            'options': [
                {
                    'title': 'Continuar',
                    'description': 'Continuar con el juego',
                    'effects': {}
                }
            ],
            'id': f'emergency_fase_{self.game_engine.current_phase}',
            'phase_number': self.game_engine.current_phase + 1
        }
    
    def _show_emergency_phase(self):
        """Muestra una fase de emergencia si hay problemas graves"""
        try:
            emergency_phase = self._get_default_phase()
            self.ui_manager.show_phase(emergency_phase)
            print("🚨 Mostrando fase de emergencia")
        except Exception as e:
            print(f"❌ Error crítico mostrando fase de emergencia: {e}")
            self.show_final_results()
    
    def handle_decision(self, decision_index: int):
        """Maneja una decisión del jugador con logging mejorado"""
        try:
            print(f"🎯 Procesando decisión {decision_index}...")
            result = self.game_engine.make_decision(decision_index)
            
            if not result.get('success', False):
                print(f"⚠️ Decisión fallida: {result.get('error', 'Error desconocido')}")
                return
            
            # Mostrar efectos de la decisión
            if result.get('decision_text') and result.get('effects_list'):
                self.ui_manager.show_decision_effects(
                    result['decision_text'],
                    result['effects_list']
                )
            
            # Verificar condiciones especiales ANTES de actualizar UI
            if result.get('game_over'):
                print("💀 Game Over detectado")
                self.ui_manager.show_game_over(
                    result.get('failed_indicators', []),
                    self.game_engine.current_phase + 1,
                    self.game_engine.max_phases
                )
                self.show_restart_option()
                return
            
            if result.get('game_completed'):
                print("🎉 Juego completado")
                self.update_ui()
                self.show_final_results()
                return
            
            # Actualizar UI y continuar
            self.update_ui()
            
            if result.get('critical_indicators'):
                self.ui_manager.show_critical_warning(result['critical_indicators'])
            
            self.show_current_phase()
            
        except Exception as e:
            print(f"❌ Error al manejar decisión: {e}")
            import traceback
            traceback.print_exc()
            # Intentar continuar el juego
            try:
                self.show_current_phase()
            except:
                self.show_final_results()
    
    def show_final_results(self):
        """Muestra los resultados finales"""
        try:
            print("🏁 Mostrando resultados finales...")
            results = self.game_engine.get_final_results()
            self.ui_manager.show_final_results(
                results['indicators'],
                results['avg_score'],
                results['category'],
                results['message'],
                results['color'],
                self.restart_game,
                self.quit_game
            )
        except Exception as e:
            print(f"❌ Error al mostrar resultados: {e}")
            self.show_restart_option()
    
    def show_restart_option(self):
        """Muestra opción de reinicio después de game over"""
        try:
            self.ui_manager._show_restart_buttons(self.restart_game, self.quit_game)
        except Exception as e:
            print(f"❌ Error al mostrar opciones de reinicio: {e}")
    
    def restart_game(self):
        """Reinicia el juego volviendo a la pantalla de inicio"""
        try:
            print("🔄 Reiniciando juego...")
            self.show_start_screen()
        except Exception as e:
            print(f"❌ Error al reiniciar: {e}")
    
    def quit_game(self):
        """Cierra el juego"""
        print("👋 Cerrando simulador...")
        self.root.quit()
    
    def show_start_screen(self):
        """Muestra la pantalla de inicio"""
        print("🏠 Mostrando pantalla de inicio...")
        self.ui_manager.show_start_screen(
            start_game_callback=self.start_game_from_menu,
            show_rules_callback=self.show_rules_screen
        )
    
    def show_rules_screen(self):
        """Muestra la pantalla de reglas"""
        print("📖 Mostrando pantalla de reglas...")
        self.ui_manager.show_rules_screen(
            back_to_start_callback=self.show_start_screen
        )
    
    def start_game_from_menu(self):
        """Inicia el juego desde el menú principal"""
        print("🎮 Iniciando juego desde menú...")
        # Configurar la UI del juego
        self.ui_manager.setup_game_ui()
        # Iniciar el juego
        self.start_game()
    
    def run(self):
        """Ejecuta el simulador"""
        print("🚀 Iniciando interfaz gráfica...")
        self.root.mainloop()

def main():
    """Función principal con mejor presentación y validaciones"""
    print("=" * 60)
    print("🎮 SIMULADOR ESTRATÉGICO EMPRESARIAL")
    print("=" * 60)
    print()
    print("📋 INSTRUCCIONES:")
    print("   🔸 Comenzarás con todos los indicadores al 80%")
    print("   🔸 Debes completar 5 fases estratégicas")
    print("   🔸 Evita que cualquier indicador baje del 5%")
    print("   🔸 Busca encadenamientos lógicos entre decisiones")
    print("   🔸 ¡Mantén el equilibrio y haz crecer tu empresa!")
    print()
    print("🚀 ¡Iniciando simulación empresarial!")
    print("=" * 60)
    print()
    
    try:
        # Verificar archivos críticos
        critical_files = [
            'ui/ui_manager.py',
            'logic/game_engine.py', 
            'config/settings.py',
            'data/phases.json'
        ]
        
        missing_files = []
        for file_path in critical_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print("❌ Archivos faltantes:")
            for file in missing_files:
                print(f"   - {file}")
            input("Presiona Enter para salir...")
            return
        
        # Verificar que el JSON es válido
        try:
            with open('data/phases.json', 'r', encoding='utf-8') as f:
                phases_data = json.load(f)
                print(f"✅ Archivo phases.json cargado ({len(phases_data['phases'])} fases)")
        except json.JSONDecodeError as e:
            print(f"❌ Error en phases.json: {e}")
            input("Presiona Enter para salir...")
            return
        
        # Verificar módulos Python
        import importlib
        modules_to_check = [
            'ui.ui_manager',
            'logic.game_engine', 
            'config.settings'
        ]
        
        for module in modules_to_check:
            try:
                importlib.import_module(module)
                print(f"✅ Módulo {module} cargado correctamente")
            except ImportError as e:
                print(f"❌ Error cargando módulo {module}: {e}")
                input("Presiona Enter para salir...")
                return
        
        print("✅ Todos los archivos y módulos verificados. Iniciando simulador...")
        print()
        
        game = BusinessSimulator()
        game.run()
        
    except KeyboardInterrupt:
        print("\n👋 Simulador cerrado por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado al iniciar el simulador: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        print("Detalles del error:")
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()