import tkinter as tk
from tkinter import ttk
from config.settings import UIConfig

class WidgetFactory:
    """Factory para crear widgets con estilos consistentes"""
    
    @staticmethod
    def create_label(parent, text: str, font_key: str = 'normal', 
                    fg_key: str = 'fg_primary', **kwargs) -> tk.Label:
        """Crea un label con estilo consistente"""
        defaults = {
            'font': UIConfig.FONTS[font_key],
            'fg': UIConfig.COLORS[fg_key],
            'bg': UIConfig.COLORS['bg_secondary'],
            'wraplength': 800 if 'wraplength' not in kwargs else kwargs['wraplength']
        }
        defaults.update(kwargs)
        
        return tk.Label(parent, text=text, **defaults)
    
    @staticmethod
    def create_button(parent, text: str, command=None, **kwargs) -> tk.Button:
        """Crea un botón con estilo consistente"""
        defaults = {
            'font': UIConfig.FONTS['normal'],
            'bg': UIConfig.COLORS['bg_button'],
            'fg': UIConfig.COLORS['fg_primary'],
            'activebackground': UIConfig.COLORS['bg_button_active'],
            'activeforeground': UIConfig.COLORS['fg_primary'],
            'relief': 'raised',
            'bd': 2,
            'wraplength': 700,
            'justify': 'left'
        }
        defaults.update(kwargs)
        
        return tk.Button(parent, text=text, command=command, **defaults)
    
    @staticmethod
    def create_frame(parent, bg_key: str = 'bg_secondary', **kwargs) -> tk.Frame:
        """Crea un frame con estilo consistente"""
        defaults = {
            'bg': UIConfig.COLORS[bg_key]
        }
        defaults.update(kwargs)
        
        return tk.Frame(parent, **defaults)
    
    @staticmethod
    def create_progressbar(parent, value: float) -> ttk.Progressbar:
        """Crea una barra de progreso con estilo según el valor"""
        progress = ttk.Progressbar(
            parent,
            length=UIConfig.PROGRESS_BAR_LENGTH,
            mode='determinate',
            value=value
        )
        return progress