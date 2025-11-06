# Parcial II - PROGRAMACION 1

Este proyecto implementa un sistema de gestión para mobs de Minecraft, organizando la información en una estructura jerárquica de directorios que refleja las características de cada mob.

## Requisitos
- No requiere dependencias externas

## Estructura de Directorios

La organización sigue una jerarquía de tres niveles:

1. **Hostilidad** (Primer nivel)
	# Gestor de Mobs de Minecraft — Resumen

	Pequeña utilidad en consola para gestionar registros de mobs y almacenarlos en una jerarquía de carpetas basada en sus características.

	Requisitos
	- Python 3.10+ (sin dependencias externas)

	Uso rápido
	- Ejecutar: `python main.py` y seguir el menú en pantalla.

	Qué hace
	- Organiza y guarda mobs en: `minecraft/<hostilidad>/<subtipo>/<movilidad>/mobs.csv`.
	- Operaciones soportadas: Listar, Agregar, Actualizar, Eliminar y Buscar (por ID o nombre — parcial/exacto).

	Formato de salida (ejemplo)
	- `ID: 7 | Nombre: Axolotl | Tipo: animal | Dimensiones: 0.75x0.42`

	Notas prácticas
	- Las dimensiones vacías se normalizan a `0`.
	- Para cancelar una operación en los prompts puede usar `cancel`.
	- Para confirmar una eliminación escriba exactamente `Eliminar`.
	- Los datos se guardan en CSV en la estructura de directorios mencionada.

	Más información
	- Para detalles sobre cada opción, consulte los comentarios en `mod/crud.py` y el código fuente.
