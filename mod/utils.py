import csv
import os
from typing import List, Tuple, Dict, Any


def leer_csv(path: str) -> List[Dict[str, str]]:
    """Lee un CSV y devuelve una lista de diccionarios. Devuelve [] si no existe."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def escribir_csv(path: str, filas: List[Dict[str, str]]):
    """Escribe una lista de diccionarios en `path`.

    - Si `filas` es None: no hace nada.
    - Si `filas` está vacío: borra el archivo si existe.
    - Si tiene filas: crea directorio y escribe CSV con encabezado.
    """
    dirpath = os.path.dirname(path)
    if filas is None:
        return
    if not filas:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass
        return
    os.makedirs(dirpath, exist_ok=True)
    campos = list(filas[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def formatear_mob(mob: Dict[str, Any]) -> str:
    """Formatea un diccionario `mob` a una línea legible."""
    try:
        width = float(mob.get("width", "0"))
    except (ValueError, TypeError):
        width = 0.0
    try:
        height = float(mob.get("height", "0"))
    except (ValueError, TypeError):
        height = 0.0
    return (f"ID: {mob.get('id', 'N/A')} | "
            f"Nombre: {mob.get('displayName', mob.get('name', 'N/A'))} | "
            f"Tipo: {mob.get('type', 'N/A')} | "
            f"Dimensiones: {width:.2f}x{height:.2f}")


def recolectar_mobs(ruta_base: str) -> List[Tuple[Dict[str, str], str]]:
    """Recorre `ruta_base` recursivamente y recolecta todos los mobs.

    Retorna una lista de tuplas (mob_dict, ruta_del_csv).
    """
    resultados: List[Tuple[Dict[str, str], str]] = []

    def _rec(dirpath: str):
        try:
            for elemento in os.listdir(dirpath):
                path = os.path.join(dirpath, elemento)
                if os.path.isdir(path):
                    _rec(path)
                elif elemento == "mobs.csv":
                    filas = leer_csv(path)
                    for fila in filas:
                        resultados.append((fila, path))
        except FileNotFoundError:
            return

    _rec(ruta_base)
    return resultados


def estadisticas_mobs(ruta_base: str) -> Dict[str, Any]:
    """Genera estadísticas básicas sobre todos los mobs bajo `ruta_base`.

    Retorna un dict con: total, por_category, por_type, avg_width/height, min/max.
    """
    datos = recolectar_mobs(ruta_base)
    total = len(datos)
    por_category: Dict[str, int] = {}
    por_type: Dict[str, int] = {}

    widths = []
    heights = []

    for mob, _ in datos:
        cat = mob.get("category", "Desconocida")
        typ = mob.get("type", "Desconocida")
        por_category[cat] = por_category.get(cat, 0) + 1
        por_type[typ] = por_type.get(typ, 0) + 1
        try:
            widths.append(float(mob.get("width", "0") or 0))
        except (ValueError, TypeError):
            pass
        try:
            heights.append(float(mob.get("height", "0") or 0))
        except (ValueError, TypeError):
            pass

    def _avg(arr):
        return sum(arr) / len(arr) if arr else 0.0

    stats = {
        "total": total,
        "por_category": por_category,
        "por_type": por_type,
        "avg_width": _avg(widths),
        "avg_height": _avg(heights),
        "min_width": min(widths) if widths else 0.0,
        "max_width": max(widths) if widths else 0.0,
        "min_height": min(heights) if heights else 0.0,
        "max_height": max(heights) if heights else 0.0,
    }
    return stats


def ordenar_mobs(ruta_base: str, key: str = "name", reverse: bool = False) -> List[Tuple[Dict[str, str], str]]:
    """Recolecta y ordena mobs por `key` ('name','id','category','type').

    Retorna la lista ordenada de (mob, path).
    """
    datos = recolectar_mobs(ruta_base)

    def key_fn(item: Tuple[Dict[str, str], str]):
        mob, _ = item
        if key == "id":
            try:
                return int(mob.get("id", 0))
            except (ValueError, TypeError):
                return 0
        elif key in ("name", "displayName"):
            return str(mob.get("name", mob.get("displayName", ""))).lower()
        elif key == "category":
            return str(mob.get("category", "")).lower()
        elif key == "type":
            return str(mob.get("type", "")).lower()
        else:
            return str(mob.get(key, "")).lower()

    return sorted(datos, key=key_fn, reverse=reverse)
