# Iro-Drop 👕✨

**Iro-Drop** es un motor de terminal (CLI) desarrollado en Python que actúa como un generador RNG de equipamiento diario (Outfits). Inspirado en los sistemas de *loot* y gestión de inventario, el programa calcula y sugiere combinaciones de ropa válidas basándose en reglas estrictas de contraste de color y la ocasión o misión del día.

## 🚀 Características Principales

- **Algoritmo de Validación (Regla de Oro):** El motor evalúa las combinaciones antes de sugerirlas. Por ejemplo, fuerza el uso de tops claros si el pantalón seleccionado es de tono oscuro.
- **Filtrado por Misión:** Clasifica el *drop* dependiendo de si el usuario necesita un atuendo `Casual`, `Gym` o de `Relax`.
- **Persistencia Dinámica de Datos:** Utiliza un archivo base `closet.json` como molde de datos y genera automáticamente un archivo `estado_closet.csv` para mantener un registro persistente.
- **Sistema de Estados:** Evita sugerir ropa que ya ha sido utilizada, cambiando dinámicamente el estado físico de las prendas (Limpia -> Usada).

## 🏗️ Arquitectura del Proyecto

El código está estructurado aplicando **Programación Orientada a Objetos (POO)** y separación de responsabilidades:

```text
iro-drop/
├── data/
│   ├── closet.json         # Base de datos inicial
│   └── estado_closet.csv   # Archivo autogenerado de estados
├── src/
│   ├── main.py             # Lógica de negocio y motor RNG
│   └── modelos.py          # Definición de la clase Prenda
└── README.md