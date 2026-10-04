import json
import os
import random
import csv
from modelos import Prenda

# ==========================================
# 1. CAPA DE DATOS (JSON y CSV)
# ==========================================
def sincronizar_datos(ruta_json: str, ruta_csv: str) -> list:
    """
    Lee el inventario. Si existe el CSV (con estados), lo usa.
    Si no existe, lee el JSON base, asume estado 'Limpia' y crea el CSV.
    """
    closet = []
    
    # Intenta leer desde el CSV primero (donde guardaremos los estados)
    if os.path.exists(ruta_csv):
        print("Cargando inventario desde la base de datos CSV...")
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                prenda = Prenda(
                    nombre=fila['Nombre'],
                    tipo=fila['Tipo'],
                    color=fila['Color'],
                    tono=fila['Tono'],
                    ocasion=fila['Ocasión'],
                    estado=fila['Estado']
                )
                closet.append(prenda)
        return closet

    # Si no hay CSV, lee el JSON (tu molde original)
    print("Primer arranque: Leyendo JSON base y creando registro CSV...")
    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            
        for item in datos['prendas']:
            # Al instanciar, el modelo le asigna estado "Limpia" por defecto
            prenda = Prenda(
                nombre=item['nombre'],
                tipo=item['tipo'],
                color=item['color'],
                tono=item['tono'],
                ocasion=item['ocasion']
            )
            closet.append(prenda)
            
        # Guarda lo leído del JSON en el nuevo CSV
        guardar_csv(ruta_csv, closet)
        return closet
        
    except FileNotFoundError:
        print(f"Error crítico: No se encontró el archivo JSON base en {ruta_json}")
        return []

def guardar_csv(ruta_csv: str, closet: list):
    """Sobrescribe el archivo CSV con el estado actual del inventario."""
    columnas = ['Nombre', 'Tipo', 'Color', 'Tono', 'Ocasión', 'Estado']
    
    with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escritor.writeheader()
        
        for p in closet:
            escritor.writerow({
                'Nombre': p.nombre,
                'Tipo': p.tipo,
                'Color': p.color,
                'Tono': p.tono,
                'Ocasión': p.ocasion,
                'Estado': p.estado
            })

# ==========================================
# 2. CAPA DE LÓGICA DE NEGOCIO (Reglas)
# ==========================================
def validar_regla_de_oro(bottom: Prenda, top: Prenda) -> bool:
    if bottom.tono == "Oscuro":
        return top.tono == "Claro"
    elif bottom.tono == "Claro" or bottom.color in ["Azul", "Beige", "Caqui"]:
        return True
    return False

# ==========================================
# 3. CAPA DEL MOTOR RNG Y ESTADOS
# ==========================================
def generar_outfit(tops: list, bottoms: list, ocasion_deseada: str):
    """Filtra ropa por ocasión Y que esté limpia, luego aplica RNG."""
    
    # FILTRO: Solo usa ropa que esté "Limpia" y que coincida con la ocasión
    tops_filtrados = [t for t in tops if (ocasion_deseada in t.ocasion or t.ocasion in ["Casual/Gym", "Urbano/Gym"]) and t.estado == "Limpia"]
    bottoms_filtrados = [b for b in bottoms if ocasion_deseada in b.ocasion and b.estado == "Limpia"]
    
    if not tops_filtrados or not bottoms_filtrados:
        print(f"\n⚠️ Alerta: No tienes suficiente ropa LIMPIA para armar un outfit '{ocasion_deseada}'.")
        print("¡Es hora de lavar ropa!")
        return None, None

    intentos = 0
    while True:
        intentos += 1
        bottom_random = random.choice(bottoms_filtrados)
        top_random = random.choice(tops_filtrados)
        
        if validar_regla_de_oro(bottom_random, top_random):
            print(f"\n✨ ¡Iro-Drop [{ocasion_deseada.upper()}] Exitoso! (Calculado en {intentos} intento(s))")
            print(f"🛡️  Bottom : {bottom_random.nombre} ({bottom_random.tono})")
            print(f"🗡️  Top    : {top_random.nombre} ({top_random.tono})")
            
            # Cambiamos el estado de las prendas seleccionadas a "Usada"
            bottom_random.actualizar_estado("Usada")
            top_random.actualizar_estado("Usada")
            
            return bottom_random, top_random

# ==========================================
# 4. INTERFAZ Y EJECUCIÓN PRINCIPAL
# ==========================================
def seleccionar_ocasion() -> str:
    print("\n--- IRO-DROP: SELECCIÓN DE MISIÓN ---")
    print("1. 🚶‍♂️ Casual (Clases Duoc, Salidas)")
    print("2. ⚔️ Gym (Entrenamiento)")
    print("3. 🛋️ Relax (Descanso)")
    
    while True:
        opcion = input("\nSelecciona el número de tu misión para hoy: ")
        if opcion == "1": return "Casual"
        elif opcion == "2": return "Gym"
        elif opcion == "3": return "Relax"
        else: print("❌ Opción inválida. Ingresa 1, 2 o 3.")

if __name__ == "__main__":
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(ruta_actual, '..', 'data', 'closet.json')
    ruta_csv = os.path.join(ruta_actual, '..', 'data', 'estado_closet.csv')
    
    print("Iniciando Motor Iro-Drop...")
    mi_closet = sincronizar_datos(ruta_json, ruta_csv)
    
    if mi_closet:
        tops = [p for p in mi_closet if p.tipo == "Top"]
        bottoms = [p for p in mi_closet if p.tipo == "Bottom"]
        
        mision_actual = seleccionar_ocasion()
        print(f"\nBuscando equipamiento limpio para: {mision_actual}...")
        
        bottom_elegido, top_elegido = generar_outfit(tops, bottoms, mision_actual)
        
        if bottom_elegido and top_elegido:
            guardar_csv(ruta_csv, mi_closet)
            print("\n💾 Estado del inventario actualizado en el archivo CSV. Las prendas fueron marcadas como 'Usada'.")