import os

from mod.etl import TIPOS_PERMITIDOS, buscar_en_arbol
from mod.utils import leer_csv, escribir_csv, formatear_mob, estadisticas_mobs, ordenar_mobs


# Ruta base de la jerarquia
BASE_DIR = "minecraft"


# -------------------- 1) Listar --------------------
def listar_recursivo(ruta_base, limite=5):
	"""Recorre el árbol desde `ruta_base` e imprime hasta `limite` mobs encontrados."""
	mostrados = 0

	def _listar(ruta):
		nonlocal mostrados
		# Si ya mostramos suficientes, terminamos (caso base que corta la recursión).
		if mostrados >= limite:
			return
		ruta_csv = os.path.join(ruta, "mobs.csv")
		if os.path.exists(ruta_csv):
			filas = leer_csv(ruta_csv)
			if filas:
				# Obtenemos la categoría del primer mob
				tipo, categoria = filas[0].get("type", "Desconocida"), filas[0].get("category", "Desconocida")
				print(f"\n=== {tipo.title()} - {categoria.title()} ===")
				for fila in filas:
					if mostrados >= limite:
						return
					print(formatear_mob(fila))
					mostrados += 1
		# Recorremos subcarpetas y llamamos de nuevo a `_listar` (recursión)
		try:
			for elemento in os.listdir(ruta):
				ruta_elemento = os.path.join(ruta, elemento)
				if os.path.isdir(ruta_elemento):
					_listar(ruta_elemento)
		except FileNotFoundError:
			# Si la carpeta no existe, simplemente ignoramos y seguimos
			return

	_listar(ruta_base)


def listar_interactivo():
	"""Función de conveniencia para llamar al listado sobre `BASE_DIR` sin límite práctico."""
	listar_recursivo(os.path.join(BASE_DIR), limite=9999)


# -------------------- 2) Agregar --------------------
def agregar_recursivo(ruta_base, nueva_fila, ruta_destino):
	"""Agrega `nueva_fila` al `mobs.csv` dentro de `ruta_destino` relativa a `ruta_base`.

	Retorna (fila_agregada, ruta_csv) o None en caso de fallo.
	"""
	try:
		# Construir ruta completa al CSV destino
		ruta_csv = os.path.join(ruta_base, ruta_destino, "mobs.csv")

		# Leer archivo existente o crear nuevo
		filas = leer_csv(ruta_csv)
		filas.append(nueva_fila)

		# Asegurar que exista el directorio
		os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

		# Escribir archivo
		escribir_csv(ruta_csv, filas)
		return nueva_fila, ruta_csv
	except Exception as e:
		print(f"Error al agregar mob: {str(e)}")
		return None


def agregar_interactivo():
	"""Interfaz interactiva: solicita datos, valida y agrega el mob al árbol."""
	ruta = os.path.join(BASE_DIR)
	print("Ingrese valores (o 'cancel' para cancelar en cualquier momento)")
	fila = {}

	# 1. ID - obligatorio y único
	while True:
		id_input = input("id: ").strip()
		if id_input.lower() == 'cancel':
			return None
		if not id_input:
			print("Error: 'id' es obligatorio.")
			continue
		try:
			int(id_input)  # Verificar que sea numérico
		except ValueError:
			print("Error: 'id' debe ser un número.")
			continue

		# Buscar coincidencias exactas del ID
		try:
			coincidencias = buscar_en_arbol("", "id", id_input)
		except Exception:
			coincidencias = []
		
		if coincidencias:
			print(f"Error: ID '{id_input}' ya existe en:")
			for mob in coincidencias:
				print(formatear_mob(mob))
			continue
		
		fila["id"] = id_input
		break

	# 2. Name - obligatorio y único
	while True:
		name_input = input("name: ").strip()
		if name_input.lower() == 'cancel':
			return None
		if not name_input:
			print("Error: 'name' es obligatorio.")
			continue

		# Buscar coincidencias exactas del nombre
		try:
			coincidencias = buscar_en_arbol("", "name", name_input)
		except Exception:
			coincidencias = []
		
		# También buscar coincidencias en displayName
		try:
			coincidencias_display = buscar_en_arbol("", "displayName", name_input)
		except Exception:
			coincidencias_display = []

		if coincidencias or coincidencias_display:
			print(f"Error: El nombre '{name_input}' ya existe en:")
			for mob in coincidencias + coincidencias_display:
				print(formatear_mob(mob))
			continue
		
		fila["name"] = name_input
		break

	# 3. Display Name
	display_name = input("displayName: ").strip()
	if display_name.lower() == 'cancel':
		return None
	fila["displayName"] = display_name if display_name else fila["name"]  # Usar name si está vacío

	# 4. Type - validar contra opciones permitidas
	print(f"\nTipos permitidos: {sorted(TIPOS_PERMITIDOS)}")
	while True:
		type_input = input("type: ").strip().lower()
		if type_input == 'cancel':
			return None
		if not type_input:
			print("Error: 'type' es obligatorio.")
			continue
		if type_input not in TIPOS_PERMITIDOS:
			print(f"Error: type debe ser uno de: {sorted(TIPOS_PERMITIDOS)}")
			continue
		fila["type"] = type_input
		break

	# 5. Category y clasificación - recopilar la ruta de destino
	try:
		hostilidades = {d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))}
	except FileNotFoundError:
		hostilidades = {"hostiles", "pasivos"}

	print("\nHOSTILIDAD:")
	print("1. Hostile mobs -> hostiles")
	print("2. Passive mobs -> pasivos")

	while True:
		hostilidad_input = input("Elige hostilidad (1-2): ").strip()
		if hostilidad_input == 'cancel':
			return None
		if hostilidad_input == "1":
			fila["category"] = "Hostile mobs"
			hostilidad = "hostiles"
			break
		elif hostilidad_input == "2":
			fila["category"] = "Passive mobs"
			hostilidad = "pasivos"
			break
		print("Error: elige 1 o 2")

	print("\nSUBTIPO:")
	print("1. Animal")
	print("2. No muerto (zombie, skeleton, etc)")
	print("3. Mob (otros)")
	print("4. Vivo (hostiles vivos)")
	
	while True:
		subtipo_input = input("Elige subtipo (1-4): ").strip()
		if subtipo_input == 'cancel':
			return None
		if subtipo_input == "1":
			subtipo = "animal"
			break
		elif subtipo_input == "2":
			subtipo = "no_muerto"
			break
		elif subtipo_input == "3":
			subtipo = "mob"
			break
		elif subtipo_input == "4":
			subtipo = "vivo"
			break
		print("Error: elige 1-4")

	print("\nMOVILIDAD:")
	print("1. Caminador")
	print("2. Volador")
	print("3. Nadador")

	while True:
		movilidad_input = input("Elige movilidad (1-3): ").strip()
		if movilidad_input == 'cancel':
			return None
		if movilidad_input == "1":
			movilidad = "caminador"
			break
		elif movilidad_input == "2":
			movilidad = "volador"
			break
		elif movilidad_input == "3":
			movilidad = "nadador"
			break
		print("Error: elige 1-3")

	# Guardar los valores derivados en la fila
	fila["hostilidad"] = hostilidad
	fila["subtipo"] = subtipo
	fila["movilidad"] = movilidad

	# 6 y 7. Width y Height - validar numéricos
	for dim in ("width", "height"):
		while True:
			v = input(f"{dim}: ").strip()
			if v.lower() == 'cancel':
				return None
			if not v:  # Si está vacío, usar 0
				fila[dim] = "0"
				break
			try:
				float(v)  # Validar que sea numérico
				fila[dim] = v
				break
			except ValueError:
				print(f"Error: {dim} debe ser numérico (se recibió '{v}').")

	# Construir la ruta de destino basada en la clasificación
	ruta_destino = os.path.join(
		fila["hostilidad"],
		fila["subtipo"],
		fila["movilidad"]
	)

	try:
		res = agregar_recursivo(ruta, fila, ruta_destino)
		if res:
			obj, archivo = res
			print("\nMob agregado correctamente:")
			print(f"ID: {obj['id']}")
			print(f"Nombre: {obj['displayName']}")
			print(f"Clasificación: {obj['hostilidad']}/{obj['subtipo']}/{obj['movilidad']}")
			print(f"\nArchivo: {archivo}")
			return res
	except Exception as e:
		print(f"\nError al agregar el mob: {str(e)}")
	return None


# -------------------- 3) Actualizar --------------------
def actualizar_recursivo(ruta_base, id_buscar, nuevos_valores):
	"""Actualiza el primer mob cuyo `id` o `name` coincida con `id_buscar`.

	Retorna (obj_actualizado, ruta_csv) o None si no encuentra.
	"""
	resultado = None

	search = str(id_buscar).strip().lower()

	def _actualizar(ruta):
		nonlocal resultado
		if resultado is not None:
			return True
		ruta_csv = os.path.join(ruta, "mobs.csv")
		if os.path.exists(ruta_csv):
			filas = leer_csv(ruta_csv)
			for i, fila in enumerate(filas):
				name_val = str(fila.get("name", "")).strip().lower()
				id_val = str(fila.get("id", "")).strip().lower()
				# Coincidir por id exacto o por name exacto
				if search == id_val or search == name_val:
					filas[i].update(nuevos_valores)
					escribir_csv(ruta_csv, filas)
					resultado = (filas[i], ruta_csv)
					return True
		try:
			for elemento in os.listdir(ruta):
				ruta_elemento = os.path.join(ruta, elemento)
				if os.path.isdir(ruta_elemento):
					if _actualizar(ruta_elemento):
						return True
		except FileNotFoundError:
			return False
		return False

	_actualizar(ruta_base)
	return resultado


def actualizar_interactivo():
	"""Interfaz para actualizar un mob con un menú interactivo y validaciones.
	
	- Permite seleccionar el campo a modificar desde un menú
	- Valida cada campo según su tipo
	- Muestra el valor actual antes de modificar
	"""
	ruta = os.path.join(BASE_DIR)
	termino = input("Ingrese ID o nombre del mob a actualizar: ").strip()
	
	# Buscar el mob
	resultados = buscar_mob(termino)
	if not resultados:
		print("No se encontró ningún mob con ese ID o nombre")
		return None
	
	# Si hay múltiples coincidencias, mostrar lista para elegir
	if len(resultados) > 1:
		print("\nSe encontraron varios mobs. Seleccione uno:")
		for i, (mob, ruta_archivo) in enumerate(resultados, 1):
			print(f"\n{i}. {formatear_mob(mob)}")
			print(f"   Ubicación: {os.path.dirname(ruta_archivo)}")
		
		while True:
			try:
				seleccion = int(input("\nIngrese el número del mob a actualizar (0 para cancelar): "))
				if seleccion == 0:
					return None
				if 1 <= seleccion <= len(resultados):
					original = resultados[seleccion - 1][0]
					break
				print("Número inválido")
			except ValueError:
				print("Por favor ingrese un número válido")
	else:
		original = resultados[0][0]
		print("\nMob encontrado:")
		print(formatear_mob(original))
		print(f"Ubicación: {os.path.dirname(resultados[0][1])}")
	
	original_id = original.get("id")

	campos_permitidos = {
		"1": ("id", "ID del mob"),
		"2": ("name", "Nombre"),
		"3": ("displayName", "Nombre mostrado"),
		"4": ("type", "Tipo"),
		"5": ("width", "Ancho"),
		"6": ("height", "Alto")
	}

	nuevos = {}
	while True:
		print("\nCampos disponibles para modificar:")
		for num, (campo, desc) in campos_permitidos.items():
			valor_actual = original.get(campo, "No definido")
			print(f"{num}. {desc} (Actual: {valor_actual})")
		print("0. Finalizar modificaciones")
		
		opcion = input("\nSeleccione el campo a modificar (0-6): ").strip()
		if opcion == "0":
			break
		if opcion not in campos_permitidos:
			print("Opción no válida")
			continue
		
		campo, desc = campos_permitidos[opcion]
		valor = input(f"Nuevo valor para {desc}: ").strip()

		# Validar según el tipo de campo
		if campo == "id":
			if not valor:
				print("Error: ID no puede quedar vacío")
				continue
			try:
				existentes = buscar_en_arbol("", "id", valor)
			except Exception:
				existentes = []
			if existentes and not (len(existentes) == 1 and existentes[0].get("id") == original_id):
				print(f"Error: ID '{valor}' ya existe en otro registro")
				continue
			try:
				int(valor)  # Verificar que sea numérico
				nuevos[campo] = valor
			except ValueError:
				print("Error: ID debe ser un número")
				continue

		elif campo == "name":
			if not valor:
				print("Error: Nombre no puede quedar vacío")
				continue
			try:
				existentes = buscar_en_arbol("", "name", valor)
			except Exception:
				existentes = []
			if existentes and not (len(existentes) == 1 and existentes[0].get("name") == original.get("name")):
				print(f"Error: Nombre '{valor}' ya existe")
				continue
			nuevos[campo] = valor

		elif campo == "type":
			valor = valor.strip().lower()
			if valor not in TIPOS_PERMITIDOS:
				print(f"Error: Tipo debe ser uno de: {sorted(TIPOS_PERMITIDOS)}")
				continue
			nuevos[campo] = valor

		elif campo in ["width", "height"]:
			if not valor:
				nuevos[campo] = "0"
			else:
				try:
					float(valor)
					nuevos[campo] = valor
				except ValueError:
					print(f"Error: {campos_permitidos[opcion][1]} debe ser un número")
					continue

		else:  # displayName
			nuevos[campo] = valor if valor else original.get("name", "")

	if not nuevos:
		print("No se realizaron modificaciones")
		return None

	res = actualizar_recursivo(ruta, original.get("name"), nuevos)
	if res:
		obj, archivo = res
		print("\nMob actualizado correctamente:")
		print(formatear_mob(obj))
		print(f"Ubicación: {os.path.dirname(archivo)}")
		return res
	print("No se pudo actualizar el mob")
	return None

# -------------------- 4) Buscar --------------------
def buscar_mob(termino_buscar):
    """Busca mobs por nombre o ID, permitiendo búsqueda parcial para nombres.
    
    Args:
        termino_buscar: ID o nombre (completo o parcial) a buscar
        
    Returns:
        Lista de tuplas (mob, ruta_archivo) que coinciden con la búsqueda
    """
    resultados = []
    termino_buscar = str(termino_buscar).lower()
    
    def _buscar(ruta):
        try:
            for elemento in os.listdir(ruta):
                ruta_elemento = os.path.join(ruta, elemento)
                if os.path.isdir(ruta_elemento):
                    _buscar(ruta_elemento)
                elif elemento == "mobs.csv":
                    filas = leer_csv(ruta_elemento)
                    for fila in filas:
                        # Búsqueda por ID (exacta)
                        if termino_buscar == str(fila.get("id", "")).lower():
                            resultados.append((fila, ruta_elemento))
                            continue
                            
                        # Búsqueda por nombre (parcial)
                        nombre = fila.get("name", "").lower()
                        display_name = fila.get("displayName", "").lower()
                        if termino_buscar in nombre or termino_buscar in display_name:
                            resultados.append((fila, ruta_elemento))
        except FileNotFoundError:
            return

    _buscar(os.path.join(BASE_DIR))
    return resultados

def buscar_interactivo():
    """Interfaz para buscar mobs por ID o nombre."""
    termino = input("Ingrese ID o nombre a buscar: ").strip()
    if not termino:
        print("Debe ingresar un ID o nombre para buscar")
        return None

    resultados = buscar_mob(termino)
    if not resultados:
        print("No se encontraron mobs que coincidan con la búsqueda")
        return None

    print(f"\nSe encontraron {len(resultados)} coincidencias:")
    for mob, ruta in resultados:
        print("\n" + formatear_mob(mob))
        print(f"Ubicación: {os.path.dirname(ruta)}")
    
    return resultados


# -------------------- 5) Eliminar --------------------
def eliminar_recursivo(ruta_base, id_eliminar):
	"""Elimina el primer mob cuyo `name` coincida con `id_eliminar`.

	Retorna (fila_eliminada, ruta_csv) o None si no encuentra.
	"""
	resultado = None

	def _eliminar(ruta):
		nonlocal resultado
		if resultado is not None:
			return True
		ruta_csv = os.path.join(ruta, "mobs.csv")
		if os.path.exists(ruta_csv):
			filas = leer_csv(ruta_csv)
			for i, fila in enumerate(filas):
				if str(fila.get("name", "")).strip() == str(id_eliminar).strip():
					eliminada = filas.pop(i)
					escribir_csv(ruta_csv, filas)
					resultado = (eliminada, ruta_csv)
					return True
		try:
			for elemento in os.listdir(ruta):
				ruta_elemento = os.path.join(ruta, elemento)
				if os.path.isdir(ruta_elemento):
					if _eliminar(ruta_elemento):
						return True
		except FileNotFoundError:
			return False
		return False

	_eliminar(ruta_base)
	return resultado


def eliminar_interactivo():
	"""Interfaz para eliminar por nombre con confirmación."""
	ruta = os.path.join(BASE_DIR)
	nombre = input("Nombre del mob a eliminar: ").strip()
	try:
		coincidencias = buscar_en_arbol("", "name", nombre)
	except Exception:
		coincidencias = []
	if not coincidencias:
		print("No se encontró el mob con ese nombre")
		return None

	mob = coincidencias[0]
	print("\nMob a eliminar:")
	print(formatear_mob(mob))
	
	confirmacion = input('\nEscriba "Eliminar" para confirmar: ').strip()
	if confirmacion != "Eliminar":
		print("Eliminación cancelada")
		return None

	res = eliminar_recursivo(ruta, nombre)
	if res:
		obj, archivo = res
		print("\nMob eliminado correctamente:")
		print(formatear_mob(obj))
		print(f"Archivo: {archivo}")
		return res
	print("No se pudo eliminar el mob")
	return None


# -------------------- 6) Estadísticas globales --------------------
def estadisticas_interactivo(ruta_base=BASE_DIR):
	"""Muestra estadísticas globales sobre todos los mobs bajo `ruta_base`.

	Esta función imprime un resumen legible con	total de mobs, conteos por categoría/tipo y estadísticas simples de	dimensiones (ancho/alto). Usa `mod.utils.estadisticas_mobs`.
	"""
	try:
		stats = estadisticas_mobs(ruta_base)
	except Exception as e:
		print(f"Error al calcular estadísticas: {e}")
		return None

	# Salida legible para el usuario
	print("\n=== Estadísticas globales ===")
	print(f"Total de mobs: {stats.get('total', 0)}")
	print("\nPor categoría:")
	for cat, cnt in stats.get("por_category", {}).items():
		print(f" - {cat}: {cnt}")
	print("\nPor tipo:")
	for typ, cnt in stats.get("por_type", {}).items():
		print(f" - {typ}: {cnt}")

	print("\nDimensiones (promedio/min/max):")
	print(f" Width: {stats.get('avg_width'):.2f} / {stats.get('min_width'):.2f} / {stats.get('max_width'):.2f}")
	print(f" Height: {stats.get('avg_height'):.2f} / {stats.get('min_height'):.2f} / {stats.get('max_height'):.2f}")
	return stats


# -------------------- 7) Ordenamiento global --------------------
def ordenar_interactivo(ruta_base=BASE_DIR):
	"""Interfaz simple para ordenar mobs globalmente.

	Permite elegir la clave de ordenamiento y muestra los resultados formateados. No modifica archivos; solo muestra la lista ordenada por pantalla.
	"""
	print("\nOpciones de ordenamiento: id, name, category, type")
	clave = input("Ingrese clave de ordenamiento (por defecto 'name'): ").strip() or "name"
	sentido = input("Invertir orden? (s/N): ").strip().lower()
	reverse = True if sentido == "s" else False

	try:
		ordenados = ordenar_mobs(ruta_base, key=clave, reverse=reverse)
	except Exception as e:
		print(f"Error al ordenar: {e}")
		return None

	if not ordenados:
		print("No hay mobs para mostrar")
		return []

	print(f"\nMobs ordenados por '{clave}' (invertido={reverse}):")
	for mob, path in ordenados:
		print(formatear_mob(mob))
		print(f"  Ubicación: {os.path.dirname(path)}")

	return ordenados