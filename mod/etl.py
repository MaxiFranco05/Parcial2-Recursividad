import csv
import os


# Campos importantes a conservar de mobs.csv (excluidos metadatos e id interno)
CAMPOS_IMPORTANTES = [
	"id", "name", "displayName", "type", "category", "width", "height"
]

# Listas simples para derivaciones
NO_MUERTOS = {"zombie", "zombie_villager", "husk", "drowned", "zombified_piglin", "wither_skeleton", "skeleton", "stray", "zombie_horse"}
VOLADORES = {"bat", "bee", "parrot", "phantom", "vex", "blaze", "ghast", "happy_ghast"}
NADADORES = {"cod", "salmon", "tropical_fish", "pufferfish", "tadpole", "axolotl", "dolphin", "squid", "glow_squid", "guardian", "elder_guardian", "turtle"}
TIPOS_PERMITIDOS = {"mob", "passive", "animal", "hostile", "acuatico", "water_creature"}


def leer_csv(ruta_csv):
	filas = []
	with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
		lector = csv.DictReader(archivo)
		for fila in lector:
			filas.append(fila)
	return filas


def filtrar_campos_importantes(filas):
	filtrado = []
	for fila in filas:
		nueva = {}
		for campo in CAMPOS_IMPORTANTES:
			nueva[campo] = fila.get(campo)
		filtrado.append(nueva)
	return filtrado


def normalizar_dimensiones(filas):
	for f in filas:
		if (f.get("width") in (None, "", "None")) and (f.get("height") in (None, "", "None")):
			f["width"] = "0"
			f["height"] = "0"


def filtrar_tipos_permitidos(filas):
	resultado = []
	for f in filas:
		tipo = (f.get("type") or "").strip().lower()
		if tipo in TIPOS_PERMITIDOS:
			resultado.append(f)
	return resultado


def derivar_hostilidad(categoria):
	if not categoria:
		return "desconocido"
	if categoria == "Hostile mobs":
		return "hostiles"
	if categoria == "Passive mobs":
		return "pasivos"
	if categoria == "Neutral mobs":
		return "neutrales"
	return categoria.lower().replace(" ", "_")


def derivar_subtipo(fila):
	nombre = (fila.get("name") or "").strip().lower()
	tipo = (fila.get("type") or "").strip().lower()
	if nombre in NO_MUERTOS:
		return "no_muerto"
	if tipo == "water_creature":
		return "animal"  # Reclasificamos water_creature como animal
	if tipo in {"animal", "passive"}:
		return "animal"
	if tipo == "hostile":
		return "vivo"
	return tipo or "otro"


def derivar_movilidad(fila):
	nombre = (fila.get("name") or "").strip().lower()
	if nombre in VOLADORES:
		return "volador"
	if nombre in NADADORES:
		return "nadador"
	return "caminador"


def escribir_csv(ruta_salida, filas, campos):
	os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
	with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
		escritor = csv.DictWriter(archivo, fieldnames=campos)
		escritor.writeheader()
		escritor.writerows(filas)


def _escribir_jerarquia_recursiva(ruta_actual, filas, encabezados, niveles, posicion):
	# Caso base: cuando ya no hay más niveles, escribimos un mobs.csv aquí
	if posicion == len(niveles):
		ruta_csv_final = os.path.join(ruta_actual, "mobs.csv")
		escribir_csv(ruta_csv_final, filas, encabezados)
		return

	# Nombre del nivel actual (por ejemplo: hostilidad, subtipo, movilidad)
	nombre_nivel = niveles[posicion]

	# Juntar los valores distintos de este nivel (sin estructuras avanzadas)
	valores_nivel = []
	for fila in filas:
		valor = fila.get(nombre_nivel) or "desconocido"
		if valor not in valores_nivel:
			valores_nivel.append(valor)
	valores_nivel.sort()

	# Para cada valor, filtrar filas y bajar recursivamente
	for valor in valores_nivel:
		subconjunto = []
		for fila in filas:
			if (fila.get(nombre_nivel) or "desconocido") == valor:
				subconjunto.append(fila)
		ruta_siguiente = os.path.join(ruta_actual, valor)
		_escribir_jerarquia_recursiva(ruta_siguiente, subconjunto, encabezados, niveles, posicion + 1)


def generar_jerarquia(ruta_entrada:str = "mobs.csv", carpeta_salida:str = ""):
	"""Genera la jerarquía de carpetas y archivos para los mobs.
	
	Implementación recursiva mediante _escribir_jerarquia_recursiva:
	1. Prepara y filtra los datos del CSV de entrada
	2. Deriva campos adicionales (hostilidad, subtipo, movilidad)
	3. Llama a función recursiva para generar estructura de directorios
	"""
	# 1) Lectura y preparación
	filas = leer_csv(ruta_entrada)
	filas = filtrar_campos_importantes(filas)
	normalizar_dimensiones(filas)
	filas = filtrar_tipos_permitidos(filas)
	if not filas:
		print("No quedaron filas válidas.")
		return

	# 2) Derivados en español
	for f in filas:
		f["hostilidad"] = derivar_hostilidad(f.get("category"))
		f["subtipo"] = derivar_subtipo(f)
		f["movilidad"] = derivar_movilidad(f)

	# 3) Encabezados: campos importantes + derivados
	encabezados = CAMPOS_IMPORTANTES + ["hostilidad", "subtipo", "movilidad"]

	# 4) Llamada recursiva para construir: minecraft/<hostilidad>/<subtipo>/<movilidad>/mobs.csv
	base = "minecraft"
	niveles = ["hostilidad", "subtipo", "movilidad"]
	_escribir_jerarquia_recursiva(base, filas, encabezados, niveles, 0)

	print("Árbol generado en:", os.path.abspath(base))


def generar_interactivo():
	"""Función interactiva para generar jerarquía con valores predeterminados."""
	entrada = "mobs.csv"  # Archivo de entrada predeterminado
	os.makedirs("minecraft", exist_ok=True)  # Crear carpeta base
	generar_jerarquia(entrada)


def _buscar_recursivo_en_directorio(ruta_directorio, coincidencias, criterio_clave, criterio_valor):
    # Si existe un mobs.csv aquí, leerlo y filtrar filas que cumplan criterio
    ruta_csv = os.path.join(ruta_directorio, "mobs.csv")
    if os.path.exists(ruta_csv):
        with open(ruta_csv, "r", encoding="utf-8", newline="") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                valor = (fila.get(criterio_clave) or "")
                # Búsqueda simple: si el valor contiene el criterio (en minúsculas)
                if criterio_valor.lower() in str(valor).lower():
                    coincidencias.append(fila)

    # Recorrer subdirectorios recursivamente (sin os.walk para explicitar recursión)
    try:
        elementos = os.listdir(ruta_directorio)
    except FileNotFoundError:
        return
    for nombre in elementos:
        ruta_hija = os.path.join(ruta_directorio, nombre)
        if os.path.isdir(ruta_hija):
            _buscar_recursivo_en_directorio(ruta_hija, coincidencias, criterio_clave, criterio_valor)


def buscar_en_arbol(carpeta_salida, criterio_clave, criterio_valor):
    base = os.path.join(carpeta_salida, "minecraft")
    coincidencias = []
    _buscar_recursivo_en_directorio(base, coincidencias, criterio_clave, criterio_valor)
    return coincidencias


def buscar_interactivo():
	"""Función interactiva para buscar mobs con ruta predeterminada."""
	clave = input("Campo por el que buscar (ej: name, type, category): ").strip() or "name"
	valor = input("Valor a buscar (se usa coincidencia por contiene): ").strip()
	resultados = buscar_en_arbol("", clave, valor)  # Usar carpeta base minecraft directamente
	print("Resultados:", len(resultados))
	contador = 0
	for fila in resultados:
		print(fila)
		contador = contador + 1
		if contador >= 20:
			break


