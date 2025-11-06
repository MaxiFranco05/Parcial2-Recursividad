import csv
import os

from mod.etl import TIPOS_PERMITIDOS, derivar_hostilidad, buscar_en_arbol


# Base directory where the hierarchy lives
BASE_DIR = "minecraft"


# -------------------- Helpers --------------------
def leer_csv(path):
	"""Lee un CSV y devuelve lista de diccionarios. Devuelve [] si no existe.

	Comentario sencillo:
	- Si no existe el archivo, devolvemos una lista vacía.
	- Si existe, usamos csv.DictReader para obtener una lista de filas (como diccionarios).
	"""
	if not os.path.exists(path):
		return []
	with open(path, "r", encoding="utf-8", newline="") as f:
		return list(csv.DictReader(f))


def escribir_csv(path, filas):
	"""Escribe una lista de diccionarios en el archivo CSV.

	Política aplicada:
	- Si `filas` es None, no hacemos nada.
	- Si `filas` es una lista vacía, borramos el archivo si existe (significa que ya no hay mobs).
	- En caso contrario, creamos el directorio padre si hace falta y escribimos el CSV con las claves de la primera fila como encabezado.

	Comentario sencillo: así mantenemos la estructura en archivos CSV colocados en las
	carpetas finales del árbol.
	"""
	dirpath = os.path.dirname(path)
	if filas is None:
		return
	if not filas:
		# borrar archivo si existe (cuando ya no quedan registros)
		try:
			if os.path.exists(path):
				os.remove(path)
		except OSError:
			pass
		return
	os.makedirs(dirpath, exist_ok=True)
	campos = list(filas[0].keys())
	# Escritura simple; se podría hacer más segura con un archivo temporal + os.replace.
	with open(path, "w", encoding="utf-8", newline="") as f:
		escritor = csv.DictWriter(f, fieldnames=campos)
		escritor.writeheader()
		escritor.writerows(filas)


# -------------------- 1) Listar --------------------
def listar_recursivo(ruta_base, limite=5):
	"""Imprime hasta `limite` filas encontradas en los `mobs.csv` del árbol.

	Explicación de la recursividad (versión simple):
	- La función interna `_listar` procesa una carpeta: si encuentra `mobs.csv` imprime sus filas.
	- Luego pide la lista de subcarpetas y llama a sí misma (`_listar`) para cada una.
	- Esto repite el mismo paso en cada subcarpeta hasta recorrer todo el árbol o hasta llegar al límite.

	Por qué funciona y cuándo se detiene:
	- Caso base: si ya se alcanzó el `limite` se vuelve sin seguir; esto evita recorrer todo el árbol cuando no hace falta.
	- Paso recursivo: para cada subcarpeta se vuelve a ejecutar la misma lógica.
	"""
	mostrados = 0

	def _listar(ruta):
		nonlocal mostrados
		# Si ya mostramos suficientes, terminamos (caso base que corta la recursión).
		if mostrados >= limite:
			return
		ruta_csv = os.path.join(ruta, "mobs.csv")
		if os.path.exists(ruta_csv):
			filas = leer_csv(ruta_csv)
			if filas:  # Solo si hay filas
				# Obtenemos la categoría del primer mob (todos en el mismo archivo tienen la misma)
				tipo, categoria = filas[0].get("type", "Desconocida"), filas[0].get("category", "Desconocida")
				print(f"\n=== {tipo.title()} - {categoria.title()} ===")
				
				for fila in filas:
					if mostrados >= limite:
						return
					# Mostrar la fila en formato amigable
					print(f"ID: {fila.get('id', 'N/A')} | "
						f"Nombre: {fila.get('displayName', fila.get('name', 'N/A'))} | "
						f"Tipo: {fila.get('type', 'N/A')} | "
						f"Dimensiones: {float(fila.get('width', '0')):.2f}x{float(fila.get('height', '0')):.2f}")
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
	"""Agrega una fila al mobs.csv en la ruta específica según su clasificación.

	Lógica:
	- La ruta_destino se construye según hostilidad/subtipo/movilidad
	- Crea el archivo mobs.csv si no existe
	- Agrega el mob manteniendo todos los campos

	Retorna: (fila_agregada, ruta_csv) si tuvo éxito, o None si hubo fallo.
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
	"""Interfaz para agregar un mob con validaciones inmediatas.

	Comentarios sencillos:
	- Valida cada campo inmediatamente después de ingresarlo.
	- Muestra opciones válidas para type y category.
	- Normaliza y verifica los datos en el momento.
	"""
	ruta = os.path.join(BASE_DIR)
	print("Ingrese valores (o 'cancel' para cancelar en cualquier momento)")
	fila = {}

	# 1. ID - Validación inmediata de obligatorio y único
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

	# 2. Name - Validación inmediata de obligatorio y único
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

	# 4. Type - Mostrar y validar contra opciones permitidas
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

	# 5. Category y clasificación - Recopilar toda la información de ubicación
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

	# 6 y 7. Width y Height - Validar que sean numéricos
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
	"""Actualiza el primer mob cuyo 'name' coincida con id_buscar.

	Lógica:
	- Buscamos `mobs.csv` en la carpeta; si hay filas, iteramos y comparamos el campo `name`.
	- Si encontramos una coincidencia, actualizamos esa fila con los nuevos valores y escribimos.
	- Si no está en esa carpeta, probamos en cada subcarpeta (recursión).

	Retorna (obj_actualizado, ruta_csv) o None si no encuentra.
	"""
	resultado = None

	def _actualizar(ruta):
		nonlocal resultado
		if resultado is not None:
			return True
		ruta_csv = os.path.join(ruta, "mobs.csv")
		if os.path.exists(ruta_csv):
			filas = leer_csv(ruta_csv)
			for i, fila in enumerate(filas):
				# Comparamos por 'name' (no por id), como solicitaste
				if str(fila.get("name", "")).strip() == str(id_buscar).strip():
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


# -------------------- Helpers --------------------
def formatear_mob(mob):
    """Formatea los datos de un mob en un string legible."""
    return (f"ID: {mob.get('id', 'N/A')} | "
            f"Nombre: {mob.get('displayName', mob.get('name', 'N/A'))} | "
            f"Tipo: {mob.get('type', 'N/A')} | "
            f"Dimensiones: {float(mob.get('width', '0')):.2f}x{float(mob.get('height', '0')):.2f}")

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
	"""Elimina el primer mob que coincida por `name` en el árbol.

	- Recorre las carpetas buscando `mobs.csv`.
	- Si encuentra la fila que tiene `name` igual a `id_eliminar`, la elimina y reescribe el CSV.
	- Retorna (fila_eliminada, ruta_csv) cuando elimina, o None si no encuentra.

	Comentario sobre la recursión: el patrón es igual que en listar/actualizar/agregar:
	- En cada carpeta miramos el CSV (caso local).
	- Si no está, llamamos a la misma función para cada subcarpeta (llamada recursiva)
	- Se detiene cuando encuentra algo o cuando no quedan subcarpetas.
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