class Prenda:
    """Clase que representa una prenda individual del Iro-Drop."""
    
    def __init__(self, nombre: str, tipo: str, color: str, tono: str, ocasion: str, estado: str = "Limpia"):
        self.nombre = nombre
        self.tipo = tipo
        self.color = color
        self.tono = tono
        self.ocasion = ocasion
        self.estado = estado # Por defecto siempre inicia como "Limpia"

    def actualizar_estado(self, nuevo_estado: str):
        """Modifica el estado físico de la prenda."""
        estados_validos = ["Limpia", "Usada", "Lavando", "Sin planchar"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
        else:
            print(f"Error: '{nuevo_estado}' no es un estado válido.")

    def __repr__(self):
        return f"Prenda(nombre='{self.nombre}', tipo='{self.tipo}', estado='{self.estado}')"