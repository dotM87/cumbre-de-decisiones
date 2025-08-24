import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable
from config.settings import UIConfig
from ui.widget_factory import WidgetFactory
from logic.score_calculator import ScoreCalculator
from data.data_manager import Phase

class UIManager:
    """Gestiona toda la interfaz de usuario con diseño gaming minimalista"""
    
    def __init__(self, root: tk.Tk, on_decision_callback: Callable):
        self.root = root
        self.on_decision_callback = on_decision_callback
        self.indicators_frame = None
        self.content_frame = None
        self.buttons_frame = None
        self.start_game_callback = None
        self._setup_modern_styles()
        self._setup_main_ui()
    
    def _setup_modern_styles(self):
        """Configura estilos oscuros modernos"""
        # Paleta de colores oscura moderna
        self.colors = {
            'primary': '#1a1b23',      # Fondo principal muy oscuro
            'secondary': '#2d3142',    # Fondo secundario gris oscuro
            'accent': '#44475a',       # Elementos de acento
            'highlight': '#6272a4',    # Hover y destacados
            'success': '#50fa7b',      # Verde brillante
            'warning': '#ffb86c',      # Naranja brillante
            'danger': '#ff5555',       # Rojo brillante
            'text_primary': '#f8f8f2', # Texto principal claro
            'text_secondary': '#6272a4', # Texto secundario
            'card_bg': '#373844'       # Fondo de cards
        }
        
        # Fuentes limpias
        self.fonts = {
            'title': ('Segoe UI', 24, 'bold'),
            'subtitle': ('Segoe UI', 16, 'bold'), 
            'body': ('Segoe UI', 14),
            'small': ('Segoe UI', 12),
            'mono': ('Segoe UI', 12)
        }
        
        # Configurar estilos de ttk para barras de progreso oscuras
        style = ttk.Style()
        
        # Estilo normal (verde)
        style.configure("Success.Horizontal.TProgressbar", 
                       background=self.colors['success'],
                       troughcolor=self.colors['secondary'],
                       borderwidth=0,
                       lightcolor=self.colors['success'],
                       darkcolor=self.colors['success'])
        
        # Estilo warning (naranja)
        style.configure("Warning.Horizontal.TProgressbar",
                       background=self.colors['warning'],
                       troughcolor=self.colors['secondary'],
                       borderwidth=0,
                       lightcolor=self.colors['warning'],
                       darkcolor=self.colors['warning'])
        
        # Estilo danger (rojo)
        style.configure("Danger.Horizontal.TProgressbar",
                       background=self.colors['danger'],
                       troughcolor=self.colors['secondary'],
                       borderwidth=0,
                       lightcolor=self.colors['danger'],
                       darkcolor=self.colors['danger'])
    
    def _setup_main_ui(self):
        """Configura la interfaz principal con layout lateral y pantalla completa"""
        self.root.title("🎮 Simulador Estratégico Empresarial")
        self.root.state('zoomed')  # Pantalla completa en Windows
        self.root.configure(bg=self.colors['primary'])
        self.root.resizable(True, True)
        
        # Container principal con padding
        main_container = tk.Frame(self.root, bg=self.colors['primary'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título principal centrado arriba
        title_label = tk.Label(
            main_container, 
            text="🎮 Simulador Estratégico Empresarial",
            font=self.fonts['title'],
            fg=self.colors['text_primary'],
            bg=self.colors['primary']
        )
        title_label.pack(pady=(0, 20))
        
        # Container horizontal para contenido y panel lateral
        content_container = tk.Frame(main_container, bg=self.colors['primary'])
        content_container.pack(fill='both', expand=True)
        
        # Área de contenido principal (lado izquierdo)
        self.content_frame = tk.Frame(content_container, 
                                    bg=self.colors['secondary'],
                                    relief='flat',
                                    bd=0)
        self.content_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        # Panel de indicadores (lado derecho)
        self.indicators_frame = tk.Frame(content_container, 
                                       bg=self.colors['primary'],
                                       width=350)
        self.indicators_frame.pack(side='right', fill='y', padx=(20, 0))
        self.indicators_frame.pack_propagate(False)  # Mantener ancho fijo
    
    def update_indicators_display(self, indicators: Dict[str, float], current_phase: int, max_phases: int):
        """Actualiza la visualización de indicadores en panel lateral derecho"""
        # Limpiar frame anterior
        for widget in self.indicators_frame.winfo_children():
            widget.destroy()
        
        # Título del panel de indicadores (más compacto)
        indicators_title = tk.Label(
            self.indicators_frame,
            text=f"📊 Indicadores\nFase {current_phase + 1}/{max_phases}",
            font=('Segoe UI', 14, 'bold'),  # Reducido de 16 a 14
            fg=self.colors['text_primary'],
            bg=self.colors['primary'],
            justify='center'
        )
        indicators_title.pack(pady=(8, 15))  # Reducido de (10, 20) a (8, 15)
        
        # Container para los indicadores verticales
        indicators_container = tk.Frame(self.indicators_frame, bg=self.colors['primary'])
        indicators_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))  # Reducido padding
        
        # Crear indicadores verticalmente con espaciado optimizado
        for i, (name, value) in enumerate(indicators.items()):
            # Frame para cada indicador con fondo oscuro (más compacto)
            indicator_card = tk.Frame(indicators_container, 
                                    bg=self.colors['card_bg'], 
                                    relief='flat', 
                                    bd=1)
            indicator_card.pack(fill='x', pady=4)  # Reducido de 8 a 4
            
            # Contenido del indicador (padding reducido)
            indicator_content = tk.Frame(indicator_card, bg=self.colors['card_bg'])
            indicator_content.pack(fill='both', expand=True, padx=12, pady=10)  # Reducido de (15, 15) a (12, 10)
            
            # Nombre del indicador (fuente más pequeña)
            label = tk.Label(
                indicator_content,
                text=name,
                font=('Segoe UI', 10, 'bold'),  # Reducido de 11 a 10
                fg=self.colors['text_primary'],
                bg=self.colors['card_bg']
            )
            label.pack()
            
            # Valor numérico (tamaño reducido)
            color = self._get_indicator_color(value)
            value_label = tk.Label(
                indicator_content,
                text=f"{value:.1f}%",
                font=('Segoe UI', 14, 'bold'),  # Reducido de 16 a 14
                fg=color,
                bg=self.colors['card_bg']
            )
            value_label.pack(pady=(3, 8))  # Reducido de (5, 10) a (3, 8)
            
            # Determinar estilo de la barra según el valor
            if value < 20:
                style_name = "Danger.Horizontal.TProgressbar"
            elif value < 50:
                style_name = "Warning.Horizontal.TProgressbar"
            else:
                style_name = "Success.Horizontal.TProgressbar"
            
            # Barra de progreso horizontal (más pequeña)
            progress = ttk.Progressbar(
                indicator_content,
                length=220,  # Reducido de 250 a 220
                mode='determinate',
                value=value,
                style=style_name
            )
            progress.pack(pady=(0, 3))  # Reducido de (0, 5) a (0, 3)
            
            # Estado del indicador (fuente más pequeña)
            if value < 20:
                status_text = "CRÍTICO"
                status_color = self.colors['danger']
            elif value < 50:
                status_text = "ALERTA"
                status_color = self.colors['warning']
            else:
                status_text = "ESTABLE"
                status_color = self.colors['success']
            
            status_label = tk.Label(
                indicator_content,
                text=status_text,
                font=('Segoe UI', 8, 'bold'),  # Reducido de 9 a 8
                fg=status_color,
                bg=self.colors['card_bg']
            )
            status_label.pack()
    
    def _get_indicator_color(self, value: float) -> str:
        """Determina el color del indicador según su valor (tema oscuro)"""
        if value < 20:
            return self.colors['danger']    # Rojo brillante
        elif value < 50:
            return self.colors['warning']   # Naranja brillante
        else:
            return self.colors['success']   # Verde brillante
    
    def show_phase(self, phase_data):
        """Muestra fase con diseño oscuro limpio y scroll en opciones"""
        self._clear_content()
        
        # Container principal con padding
        main_frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        main_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Pregunta principal centrada y destacada
        question_frame = tk.Frame(main_frame, bg=self.colors['accent'], relief='flat', bd=0)
        question_frame.pack(fill='x', pady=(0, 20))
        
        question_label = tk.Label(
            question_frame,
            text=phase_data['question'],
            font=self.fonts['subtitle'],
            fg=self.colors['text_primary'],
            bg=self.colors['accent'],
            wraplength=900,
            justify='center'
        )
        question_label.pack(pady=15, padx=30)
        
        # Frame con scrollbar para las opciones
        canvas_frame = tk.Frame(main_frame, bg=self.colors['secondary'])
        canvas_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Canvas y scrollbar
        canvas = tk.Canvas(canvas_frame, bg=self.colors['secondary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['secondary'])
        
        # Crear ventana del frame dentro del canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            # Actualizar scroll region
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Hacer que el frame scrollable ocupe todo el ancho del canvas
            canvas.itemconfig(canvas_window, width=event.width)
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Bindings para mantener el tamaño sincronizado
        canvas.bind('<Configure>', on_canvas_configure)
        scrollable_frame.bind('<Configure>', on_frame_configure)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Opciones de decisión con tema oscuro dentro del frame scrollable
        for i, option in enumerate(phase_data['options']):
            # Frame para cada opción SIN padx para usar todo el ancho
            option_frame = tk.Frame(scrollable_frame, bg=self.colors['secondary'])
            option_frame.pack(fill='x', pady=10, padx=0)
            
            # Botón principal con tema oscuro - ocupa todo el ancho
            btn = tk.Button(
                option_frame,
                text=f"{chr(65+i)}) {option['title']}",
                font=('Segoe UI', 11, 'bold'),
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary'],
                activebackground=self.colors['highlight'],
                activeforeground=self.colors['text_primary'],
                relief='flat',
                bd=1,
                wraplength=850,
                justify='left',
                command=lambda idx=i: self.on_decision_callback(idx),
                cursor="hand2"
            )
            btn.pack(fill='x', pady=(0, 5), padx=5)
            
            # Tipo de estrategia (si está disponible)
            if option.get('strategy_type'):
                strategy_label = tk.Label(
                    option_frame,
                    text=f"📋 {option['strategy_type']}",
                    font=('Segoe UI', 9, 'italic'),
                    fg=self.colors['accent'],
                    bg=self.colors['secondary'],
                    justify='left'
                )
                strategy_label.pack(fill='x', padx=25, pady=(0, 3))
            
            # Descripción con texto claro - ocupa todo el ancho
            if option.get('description'):
                desc_label = tk.Label(
                    option_frame,
                    text=option['description'],
                    font=('Segoe UI', 10),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['secondary'],
                    wraplength=900,
                    justify='left'
                )
                desc_label.pack(fill='x', padx=25)
        
        # Bind mouse wheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _clear_content(self):
        """Limpia el contenido del frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_decision_effects(self, decision_text: str, effects_list: List[str]):
        """Muestra los efectos de una decisión con mensaje limpio"""
        # Crear mensaje simple y claro
        effects_message = f"Decisión tomada: {decision_text}\n\n"
        effects_message += "Impacto en indicadores:\n" + "\n".join(effects_list)
        
        messagebox.showinfo("Resultado", effects_message)
    
    def show_critical_warning(self, critical_indicators: List[str]):
        """Muestra advertencia crítica limpia"""
        warning_msg = "⚠️ Alerta: Indicadores en zona de riesgo\n\n"
        for indicator in critical_indicators:
            warning_msg += f"• {indicator} (menos del 20%)\n"
        warning_msg += "\nTen cuidado con las próximas decisiones."
        
        messagebox.showwarning("Zona de Riesgo", warning_msg)
    
    def show_game_over(self, failed_indicators: List[str], current_phase: int, max_phases: int):
        """Muestra game over limpio"""
        failure_msg = f"Fin del juego\n\n"
        failure_msg += f"Llegaste hasta la Fase {current_phase}/{max_phases}\n\n"
        failure_msg += "Indicadores críticos:\n"
        for indicator in failed_indicators:
            failure_msg += f"• {indicator} (menos del 5%)\n"
        
        messagebox.showerror("Fin del Juego", failure_msg)
    
    def show_final_results(self, indicators: Dict[str, float], avg_score: float, 
                          category: str, message: str, color: str, 
                          restart_callback: Callable, quit_callback: Callable):
        """Muestra resultados finales con diseño gaming como el original"""
        # Limpiar contenido
        self._clear_content()
        
        # Título de resultados oscuro
        title_label = tk.Label(
            self.content_frame,
            text="🎊 Simulación Completada",
            font=('Segoe UI', 18, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['secondary']
        )
        title_label.pack(pady=20)
        
        # Categoría con colores oscuros
        cat_color = self.colors['success'] if avg_score >= 70 else self.colors['warning'] if avg_score >= 50 else self.colors['danger']
        category_label = tk.Label(
            self.content_frame,
            text=category,
            font=('Segoe UI', 16, 'bold'),
            fg=cat_color,
            bg=self.colors['secondary']
        )
        category_label.pack(pady=10)
        
        # Puntuación en frame destacado oscuro
        score_frame = tk.Frame(self.content_frame, bg=self.colors['accent'], relief='flat', bd=0)
        score_frame.pack(pady=15)
        
        score_label = tk.Label(
            score_frame,
            text=f"Puntuación Final: {avg_score:.1f}/100",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['accent']
        )
        score_label.pack(pady=15, padx=30)
        
        # Mensaje con tema oscuro
        message_label = tk.Label(
            self.content_frame,
            text=message,
            font=('Segoe UI', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['secondary'],
            wraplength=500,
            justify='center'
        )
        message_label.pack(pady=20)
        
        # Desglose de indicadores finales
        details_frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        details_frame.pack(pady=20)
        
        details_title = tk.Label(
            details_frame,
            text="� INDICADORES FINALES:",
            font=('Arial', 12, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['secondary']
        )
        details_title.pack()
        
        for name, value in indicators.items():
            color = self._get_indicator_color(value)
            indicator_label = tk.Label(
                details_frame,
                text=f"{name}: {value:.1f}%",
                font=('Arial', 11),
                fg=color,
                bg=self.colors['secondary']
            )
            indicator_label.pack()
        
        # Botones de acción
        buttons_frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        buttons_frame.pack(pady=30)
        
        restart_btn = tk.Button(
            buttons_frame,
            text="🔄 JUGAR NUEVAMENTE",
            font=('Arial', 12, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['secondary'],
            activebackground='#8be9fd',
            command=restart_callback,
            padx=20,
            pady=10
        )
        restart_btn.pack(side='left', padx=10)
        
        quit_btn = tk.Button(
            buttons_frame,
            text="❌ SALIR",
            font=('Arial', 12, 'bold'),
            bg=self.colors['danger'],
            fg=self.colors['text_primary'],
            activebackground='#ff6b6b',
            command=quit_callback,
            padx=20,
            pady=10
        )
        quit_btn.pack(side='left', padx=10)
    
    def _show_restart_buttons(self, restart_callback: Callable, quit_callback: Callable):
        """Muestra botones de reinicio con tema oscuro después de game over"""
        restart_frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        restart_frame.pack(pady=30)
        
        restart_btn = tk.Button(
            restart_frame,
            text="🔄 Nueva Partida",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['primary'],
            activebackground=self.colors['highlight'],
            command=restart_callback,
            padx=20,
            pady=10,
            relief='flat',
            bd=0,
            cursor="hand2"
        )
        restart_btn.pack(side='left', padx=10)
        
        quit_btn = tk.Button(
            restart_frame,
            text="❌ Salir",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['danger'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['highlight'],
            command=quit_callback,
            padx=20,
            pady=10,
            relief='flat',
            bd=0,
            cursor="hand2"
        )
        quit_btn.pack(side='left', padx=10)

    def show_start_screen(self, start_game_callback: Callable, show_rules_callback: Callable):
        """Muestra la pantalla de inicio del juego"""
        # Guardar callback para usar después
        self.start_game_callback = start_game_callback
        
        # Limpiar todo el contenido
        self._clear_all_content()
        
        # Container principal centrado
        main_container = tk.Frame(self.root, bg=self.colors['primary'])
        main_container.pack(fill='both', expand=True)
        
        # Frame central para centrar todo el contenido
        center_frame = tk.Frame(main_container, bg=self.colors['primary'])
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal del juego
        title_label = tk.Label(
            center_frame,
            text="🎮 Simulador de Decisiones Estratégicas",
            font=('Segoe UI', 28, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['primary']
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(
            center_frame,
            text='"El Rincón de Amaru"',
            font=('Segoe UI', 20, 'italic'),
            fg=self.colors['accent'],
            bg=self.colors['primary']
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Frame para los botones
        buttons_frame = tk.Frame(center_frame, bg=self.colors['primary'])
        buttons_frame.pack(pady=20)
        
        # Botón Jugar
        play_btn = tk.Button(
            buttons_frame,
            text="🚀 JUGAR",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['primary'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['text_primary'],
            command=start_game_callback,
            padx=40,
            pady=15,
            relief='flat',
            bd=0,
            cursor="hand2"
        )
        play_btn.pack(pady=10)
        
        # Botón Reglas
        rules_btn = tk.Button(
            buttons_frame,
            text="📖 REGLAS",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['text_primary'],
            command=show_rules_callback,
            padx=40,
            pady=15,
            relief='flat',
            bd=0,
            cursor="hand2"
        )
        rules_btn.pack(pady=10)
        
        # Información adicional
        info_label = tk.Label(
            center_frame,
            text="Un juego basado en las 5 Fuerzas de Porter\nDesarrolla tu estrategia empresarial",
            font=('Segoe UI', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['primary'],
            justify='center'
        )
        info_label.pack(pady=(30, 0))

    def show_rules_screen(self, back_to_start_callback: Callable):
        """Muestra la pantalla de reglas del juego"""
        # Limpiar todo el contenido
        self._clear_all_content()
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors['primary'])
        main_container.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Título de reglas
        title_label = tk.Label(
            main_container,
            text="📖 Reglas del Juego",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['primary']
        )
        title_label.pack(pady=(10, 20))
        
        # Frame con scroll para el contenido de reglas
        canvas_frame = tk.Frame(main_container, bg=self.colors['primary'])
        canvas_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Canvas y scrollbar
        canvas = tk.Canvas(canvas_frame, bg=self.colors['secondary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['secondary'])
        
        # Crear ventana del frame dentro del canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas.bind('<Configure>', on_canvas_configure)
        scrollable_frame.bind('<Configure>', on_frame_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido de las reglas
        content_frame = tk.Frame(scrollable_frame, bg=self.colors['secondary'])
        content_frame.pack(fill='both', expand=True, padx=60, pady=40)
        
        # Bienvenida en un frame destacado
        welcome_frame = tk.Frame(content_frame, bg=self.colors['accent'], relief='flat', bd=0)
        welcome_frame.pack(fill='x', pady=(0, 30))
        
        welcome_label = tk.Label(
            welcome_frame,
            text='Bienvenido al Simulador de Decisiones Estratégicas "El Rincón de Amaru"',
            font=('Segoe UI', 18, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['accent'],
            wraplength=650,
            justify='center'
        )
        welcome_label.pack(pady=20, padx=30)
        
        # Descripción principal en frame separado
        desc_frame = tk.Frame(content_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        desc_frame.pack(fill='x', pady=(0, 25))
        
        description_text = """En este juego representarás a un emprendedor que ha fundado una cafetería con identidad cultural, insumos locales y un enfoque experiencial. Tu objetivo es mantener el equilibrio estratégico a lo largo de 5 rondas (islas), cada una basada en una de las 5 fuerzas de Porter."""
        
        description_label = tk.Label(
            desc_frame,
            text=description_text,
            font=('Segoe UI', 13),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg'],
            wraplength=650,
            justify='left'
        )
        description_label.pack(pady=20, padx=30, fill='x')
        
        # Sección de reglas con frame propio
        rules_frame = tk.Frame(content_frame, bg=self.colors['secondary'])
        rules_frame.pack(fill='x', pady=(10, 30))
        
        # Título de reglas
        rules_title = tk.Label(
            rules_frame,
            text="📋 Reglas del Juego:",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['secondary']
        )
        rules_title.pack(anchor='w', pady=(0, 15))
        
        # Lista de reglas con mejor espaciado
        rules_list = [
            "Cada decisión que tomes afectará uno o más de los siguientes indicadores: liquidez, rentabilidad, reputación, sostenibilidad estratégica y riesgo acumulado.",
            "No hay decisiones \"correctas\" o \"incorrectas\" absolutas. El éxito radica en tu coherencia estratégica, capacidad de adaptación y visión de largo plazo.",
            "Tu empresa puede crecer, sostenerse o fracasar según cómo combines tus decisiones.",
            "Al finalizar cada isla, verás cómo cambian tus indicadores. Analiza los resultados y aprende.",
            "El juego termina cuando completas las 5 islas o cuando el riesgo acumulado alcanza el 100% (fracaso operativo)."
        ]
        
        for i, rule in enumerate(rules_list, 1):
            # Frame para cada regla individual
            rule_frame = tk.Frame(rules_frame, bg=self.colors['card_bg'], relief='flat', bd=1)
            rule_frame.pack(fill='x', pady=5, padx=10)
            
            rule_label = tk.Label(
                rule_frame,
                text=f"{i}. {rule}",
                font=('Segoe UI', 12),
                fg=self.colors['text_primary'],
                bg=self.colors['card_bg'],
                wraplength=600,
                justify='left'
            )
            rule_label.pack(pady=12, padx=20, anchor='w')
        
        # Sección de historia con frame propio
        story_frame = tk.Frame(content_frame, bg=self.colors['secondary'])
        story_frame.pack(fill='x', pady=(20, 30))
        
        # Título de historia
        story_title = tk.Label(
            story_frame,
            text='📖 Historia de la Cafetería "El Rincón de Amaru"',
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['warning'],
            bg=self.colors['secondary']
        )
        story_title.pack(anchor='w', pady=(0, 20))
        
        # Container para los párrafos de historia
        story_container = tk.Frame(story_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        story_container.pack(fill='x', padx=10)
        
        # Historia - párrafo 1
        story_p1 = """Amaru Mamani, joven emprendedor cochabambino, fundó El Rincón de Amaru con el sueño de unir café de altura, cultura local y emprendimiento juvenil. Tras años de esfuerzo, abrió una cafetería con una propuesta única: arte local, música en vivo, productos regionales y atención personalizada."""
        
        story_label1 = tk.Label(
            story_container,
            text=story_p1,
            font=('Segoe UI', 12),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg'],
            wraplength=600,
            justify='left'
        )
        story_label1.pack(pady=(20, 15), padx=30, fill='x')
        
        # Historia - párrafo 2
        story_p2 = """Aunque el inicio fue exitoso, pronto enfrentó dilemas estratégicos: expandir el menú o mejorar márgenes, contratar personal o mantener turnos familiares, elegir entre proveedores baratos o microproductores, participar en ferias o enfocarse en el local, y adoptar delivery o preservar la experiencia presencial."""
        
        story_label2 = tk.Label(
            story_container,
            text=story_p2,
            font=('Segoe UI', 12),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg'],
            wraplength=600,
            justify='left'
        )
        story_label2.pack(pady=(0, 15), padx=30, fill='x')
        
        # Historia - párrafo 3
        story_p3 = """Cada decisión afectaba indicadores clave como liquidez, rentabilidad, reputación y sostenibilidad. Amaru aprendió que no hay decisiones "correctas", sino estrategias coherentes que acumulen valor a largo plazo."""
        
        story_label3 = tk.Label(
            story_container,
            text=story_p3,
            font=('Segoe UI', 12),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg'],
            wraplength=600,
            justify='left'
        )
        story_label3.pack(pady=(0, 15), padx=30, fill='x')
        
        # Historia - párrafo final
        story_p4 = """Este concepto se convierte en la base de un juego de simulación empresarial, donde el jugador toma decisiones como Amaru, enfrentando las 5 fuerzas de Porter: proveedores, clientes, productos sustitutos, nuevos competidores y rivalidad sectorial. El resultado final dependerá de cómo se gestionan estas decisiones y su impacto acumulado en el negocio."""
        
        story_label4 = tk.Label(
            story_container,
            text=story_p4,
            font=('Segoe UI', 12),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg'],
            wraplength=600,
            justify='left'
        )
        story_label4.pack(pady=(0, 20), padx=30, fill='x')
        
        # Bind mouse wheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botones de navegación
        nav_frame = tk.Frame(main_container, bg=self.colors['primary'])
        nav_frame.pack(pady=20)
        
        # Botón Volver
        back_btn = tk.Button(
            nav_frame,
            text="⬅️ VOLVER",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['text_primary'],
            command=back_to_start_callback,
            padx=30,
            pady=12,
            relief='flat',
            bd=0,
            cursor="hand2"
        )
        back_btn.pack(side='left', padx=10)
        
        # Botón Jugar desde reglas
        play_btn = tk.Button(
            nav_frame,
            text="🚀 JUGAR",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['success'],
            fg=self.colors['primary'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['text_primary'],
            command=self.start_game_callback if self.start_game_callback else lambda: None,
            padx=30,
            pady=12,
            relief='flat',
            bd=0,
            cursor="hand2"
        )
        play_btn.pack(side='left', padx=10)

    def _clear_all_content(self):
        """Limpia todo el contenido de la ventana principal"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_game_ui(self):
        """Configura la UI del juego después de las pantallas de inicio"""
        # Primero limpiar todo el contenido de la ventana
        self._clear_all_content()
        # Reconfigurar la UI principal para el juego
        self._setup_main_ui()
