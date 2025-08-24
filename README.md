# ☕ El Rincón de Amaru - Simulador Estratégico Empresarial

![Estado del Proyecto](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow)
![Licencia](https://img.shields.io/badge/Licencia-CC%20BY--NC--ND%204.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## 📖 Descripción del Juego

**El Rincón de Amaru** es un simulador interactivo de decisiones empresariales que te pone en los zapatos de Amaru Mamani, un joven emprendedor cochabambino de 26 años que debe gestionar estratégicamente su cafetería en el centro cultural de la ciudad.

### 🎯 Concepto del Juego

El juego está basado en el modelo de las **5 Fuerzas de Porter**, una herramienta fundamental del análisis estratégico empresarial. Los jugadores navegan a través de 5 "islas" de decisión, cada una representando una fuerza competitiva:

1. **🏝️ Isla 1**: Poder de Negociación con Proveedores
2. **🏝️ Isla 2**: Poder de Negociación de los Clientes  
3. **🏝️ Isla 3**: Amenaza de Nuevos Entrantes
4. **🏝️ Isla 4**: Amenaza de Productos Sustitutos
5. **🏝️ Isla 5**: Rivalidad entre Competidores Existentes

### 🎮 Mecánicas de Juego

- **Sistema de Indicadores**: Gestiona 5 métricas empresariales clave
  - 💵 **Liquidez**: Dinero disponible para operaciones
  - 📈 **Rentabilidad**: Retorno sobre inversión
  - ⭐ **Reputación**: Percepción de marca y calidad
  - ⚠️ **Riesgo Acumulado**: Exposición a errores estratégicos
  - 🌱 **Sostenibilidad Estratégica**: Coherencia de decisiones a largo plazo

- **Decisiones Estratégicas**: Cada fase presenta 4-6 opciones con consecuencias únicas
- **Sistema de Sinergias**: Las decisiones pasadas desbloquean nuevas opciones
- **Múltiples Finales**: El resultado depende del equilibrio de tus indicadores

### 🌟 Características Únicas

- **Narrativa Auténtica**: Ambientado en la cultura emprendedora boliviana
- **Aprendizaje Práctico**: Conceptos de estrategia empresarial aplicados de forma lúdica
- **Decisiones Realistas**: Basadas en situaciones empresariales reales
- **Sistema de Consecuencias**: Cada elección tiene impacto en múltiples indicadores

## 🚀 Tecnologías Utilizadas

### Versión Actual (v1.0)
- **Lenguaje**: Python 3.8+
- **Interfaz Gráfica**: Tkinter (interfaz de escritorio nativa)
- **Gestión de Datos**: JSON para configuración de fases
- **Arquitectura**: Modular con separación de responsabilidades

### Próxima Versión (v2.0) - En Desarrollo
- **Framework Web**: PyScript (Python ejecutándose en el navegador)
- **Tecnologías Web**: HTML5, CSS3, JavaScript
- **Ventajas**: 
  - Acceso desde cualquier navegador
  - No requiere instalación
  - Compatible con dispositivos móviles
  - Fácil distribución y actualización

## 📁 Estructura del Proyecto

```
juego_soceii/
├── main.py                 # Punto de entrada de la aplicación
├── README.md              # Documentación del proyecto
├── config/                # Configuración del juego
│   ├── __init__.py
│   └── settings.py        # Constantes y configuraciones
├── data/                  # Datos del juego
│   ├── __init__.py
│   ├── data_manager.py    # Gestión de datos y fases
│   └── phases.json        # Contenido narrativo y decisiones
├── logic/                 # Lógica del juego
│   ├── __init__.py
│   ├── game_engine.py     # Motor principal del juego
│   └── score_calculator.py # Cálculos de puntuación
└── ui/                    # Interfaz de usuario
    ├── __init__.py
    ├── ui_manager.py      # Gestión de la interfaz
    └── widget_factory.py  # Componentes de UI reutilizables
```

## 🎓 Propósito Académico

Este proyecto fue desarrollado como herramienta educativa para:

- **Aprendizaje de Estrategia Empresarial**: Aplicación práctica del modelo de Porter
- **Desarrollo de Software**: Implementación de arquitecturas modulares
- **Gamificación Educativa**: Uso de elementos lúdicos para el aprendizaje
- **Programación en Python**: Desarrollo de aplicaciones completas

## 🚦 Instalación y Uso

### Requisitos del Sistema
- Python 3.8 o superior
- Tkinter (incluido en instalaciones estándar de Python)

### Instalación
1. Clona o descarga el repositorio
2. Navega hasta el directorio del proyecto
3. Ejecuta el juego:
   ```bash
   python main.py
   ```

### Controles del Juego
- **Interfaz Gráfica**: Usa el mouse para navegar y seleccionar opciones
- **Pantalla Completa**: El juego se ejecuta en modo de pantalla completa por defecto
- **Menú Principal**: Accede a reglas del juego y opciones de configuración

## 🎯 Objetivos del Jugador

1. **Completar las 5 Fases**: Navega exitosamente por todas las islas de decisión
2. **Mantener el Equilibrio**: Evita que cualquier indicador baje del 5%
3. **Optimizar Resultados**: Busca la combinación de decisiones que maximice tu puntuación final
4. **Descubrir Sinergias**: Encuentra combinaciones de decisiones que se potencien mutuamente

## 👥 Equipo de Desarrollo

*[Lista de colaboradores será añadida próximamente]*

## 📄 Licencia

Este proyecto está licenciado bajo **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**.

**Esto significa que puedes:**
- ✅ Compartir — copiar y redistribuir el material en cualquier medio o formato

**Bajo las siguientes condiciones:**
- 📝 **Atribución** — Debes dar crédito apropiado
- 🚫 **No Comercial** — No puedes usar el material con propósitos comerciales  
- 🔒 **Sin Derivadas** — No puedes remezclar, transformar o construir sobre el material

## 🔮 Roadmap Futuro

### Versión 2.0 - Migración Web
- [ ] Conversión a PyScript
- [ ] Interfaz web responsive
- [ ] Optimización para dispositivos móviles
- [ ] Sistema de guardado en el navegador

### Futuras Mejoras
- [ ] Nuevos escenarios empresariales
- [ ] Sistema multijugador
- [ ] Analíticas de decisiones
- [ ] Integración con plataformas educativas

---

## 🤝 Contribuciones

Este es un proyecto académico abierto a sugerencias y mejoras. Si tienes ideas para nuevas funcionalidades o encuentras algún problema, no dudes en contactarnos.

## 📞 Contacto

*[Información de contacto será añadida próximamente]*

---

*Desarrollado con ❤️ para el aprendizaje de estrategia empresarial*