# 🎮 Gestor de Mobs de Minecraft

## 📚 Información Académica

**Materia:** Programación 1  
**Carrera:** Tecnicatura Universitaria en Programación (TUP)  
**Comisión:** 3 
**Integrantes:**
- Maximo Franco
- Octavio Fiore

**Repositorio:** [Parcial2-Recursividad](https://github.com/MaxiFranco05/Parcial2-Recursividad)

---

## 📖 Descripción del Proyecto

Este proyecto consiste en una aplicación de consola desarrollada en Python que permite gestionar información de mobs de Minecraft mediante una **estructura jerárquica de directorios**. El sistema organiza 148 mobs según sus características (hostilidad, subtipo y movilidad), persistiendo los datos en archivos CSV distribuidos en un árbol de carpetas de 3 niveles.

El objetivo principal es aplicar y consolidar conocimientos fundamentales de programación, incluyendo:
- Estructuras de datos jerárquicas (árboles de directorios)
- Recursividad para recorrer y manipular estructuras
- Persistencia de datos en archivos CSV
- Operaciones CRUD completas (Create, Read, Update, Delete)
- Clasificación automática según reglas del dominio
- Validación exhaustiva de datos

El dataset incluye información de mobs con datos sobre dimensiones (width/height), tipo, categoría y clasificación en el sistema de carpetas.

---

## 🚀 Instrucciones de Uso

### Requisitos Previos
- Python 3.10 o superior instalado en el sistema
- Terminal o consola de comandos
- Los archivos del proyecto descargados o clonados

### Pasos para Ejecutar

1. **Clonar o descargar el repositorio:**
```bash
git clone https://github.com/MaxiFranco05/Parcial2-Recursividad.git
cd Parcial2-Recursividad
```

2. **Verificar que el archivo CSV esté presente:**
Asegúrese de que `mobs.csv` esté en la raíz del proyecto.

3. **Ejecutar el programa:**
```bash
python main.py
```

4. **Navegar por el menú:**
Seleccione la opción deseada ingresando el número correspondiente y siga las instrucciones en pantalla.

---

## 💡 Ejemplos de Uso por Menú

### **Menú Principal**

```
=== Menú de Gestión de Mobs ===
1) Listar mobs (recursivo)
2) Agregar mob
3) Actualizar mob por nombre
4) Eliminar mob por nombre
5) Buscar mobs
0) Salir

Elija una opción:
```

---

### **1. Listar Mobs (Recursivo)**

**Entrada:**
```
Elija una opción: 1
```

**Salida:**
```
=== Hostile - Hostile Mobs ===
ID: 14 | Nombre: Blaze | Tipo: hostile | Dimensiones: 0.60x1.80
ID: 17 | Nombre: Breeze | Tipo: hostile | Dimensiones: 0.60x1.77
ID: 21 | Nombre: Cave Spider | Tipo: hostile | Dimensiones: 0.70x0.50
ID: 30 | Nombre: Creeper | Tipo: hostile | Dimensiones: 0.60x1.70

=== Animal - Passive Mobs ===
ID: 7  | Nombre: Axolotl | Tipo: animal | Dimensiones: 0.75x0.42
ID: 11 | Nombre: Bee     | Tipo: animal | Dimensiones: 0.70x0.60
ID: 19 | Nombre: Camel   | Tipo: animal | Dimensiones: 1.70x2.38
ID: 20 | Nombre: Cat     | Tipo: animal | Dimensiones: 0.60x0.70
```

**Descripción:**
El sistema recorre recursivamente toda la jerarquía de carpetas, mostrando los mobs organizados por su tipo y categoría.

---

### **2. Agregar Mob**

**Entrada:**
```
Elija una opción: 2

Ingrese valores (o 'cancel' para cancelar en cualquier momento)
id: 150
name: phantom_cat
displayName: Phantom Cat
type: hostile

Tipos permitidos: ['animal', 'hostile', 'mob', 'passive', 'water_creature']
type: hostile

HOSTILIDAD:
1. Hostile mobs -> hostiles
2. Passive mobs -> pasivos
Elige hostilidad (1-2): 1

SUBTIPO:
1. Animal
2. No muerto (zombie, skeleton, etc)
3. Mob (otros)
4. Vivo (hostiles vivos)
Elige subtipo (1-4): 4

MOVILIDAD:
1. Caminador
2. Volador
3. Nadador
Elige movilidad (1-3): 2

width: 0.8
height: 1.2
```

**Salida:**
```
Mob agregado correctamente:
ID: 150
Nombre: Phantom Cat
Clasificación: hostiles/vivo/volador

Archivo: minecraft/hostiles/vivo/volador/mobs.csv
```

**Descripción:**
Permite agregar un nuevo mob con validaciones exhaustivas:
- ID único y numérico
- Nombre sin duplicados
- Tipo válido de la lista permitida
- Clasificación interactiva en 3 niveles
- Dimensiones numéricas

---

### **3. Actualizar Mob por Nombre**

**Entrada:**
```
Elija una opción: 3

Ingrese ID o nombre del mob a actualizar: blaze
```

**Salida:**
```
Mob encontrado:
ID: 14 | Nombre: Blaze | Tipo: hostile | Dimensiones: 0.60x1.80
Ubicación: minecraft/hostiles/vivo/volador

Campos disponibles para modificar:
1. ID del mob (Actual: 14)
2. Nombre (Actual: blaze)
3. Nombre mostrado (Actual: Blaze)
4. Tipo (Actual: hostile)
5. Ancho (Actual: 0.6)
6. Alto (Actual: 1.8)
0. Finalizar modificaciones

Seleccione el campo a modificar (0-6): 6
Nuevo valor para Alto: 1.9
¿Confirma el cambio? (s/n): s

Campo 'height' actualizado correctamente

  Anterior: 1.8
  Nuevo   : 1.9

¿Desea modificar otro campo? (s/n): n
```

**Descripción:**
Busca un mob por ID o nombre y permite editar campos individuales con validación en tiempo real.

---

### **4. Eliminar Mob por Nombre**

**Entrada:**
```
Elija una opción: 4

Nombre del mob a eliminar: phantom_cat
```

**Salida:**
```
Mob a eliminar:
ID: 150 | Nombre: Phantom Cat | Tipo: hostile | Dimensiones: 0.80x1.20

Escriba "Eliminar" para confirmar: Eliminar

Mob eliminado correctamente:
ID: 150 | Nombre: Phantom Cat | Tipo: hostile | Dimensiones: 0.80x1.20
Archivo: minecraft/hostiles/vivo/volador/mobs.csv
```

**Descripción:**
Busca y elimina un mob del sistema con doble confirmación para evitar eliminaciones accidentales.

---

### **5. Buscar Mobs**

**Entrada:**
```
Elija una opción: 5

Campo por el que buscar (ej: name, type, category): type
Valor a buscar (se usa coincidencia por contiene): water_creature
```

**Salida:**
```
Resultados: 5

ID: 26 | Nombre: Cod | Tipo: water_creature | Dimensiones: 0.50x0.30
Ubicación: minecraft/pasivos/animal/nadador/

ID: 102 | Nombre: Pufferfish | Tipo: water_creature | Dimensiones: 0.70x0.70
Ubicación: minecraft/pasivos/animal/nadador/

ID: 105 | Nombre: Salmon | Tipo: water_creature | Dimensiones: 0.70x0.40
Ubicación: minecraft/pasivos/animal/nadador/

ID: 125 | Nombre: Tadpole | Tipo: water_creature | Dimensiones: 0.40x0.30
Ubicación: minecraft/pasivos/animal/nadador/

ID: 131 | Nombre: Tropical Fish | Tipo: water_creature | Dimensiones: 0.50x0.40
Ubicación: minecraft/pasivos/animal/nadador/
```

**Descripción:**
Búsqueda recursiva por cualquier campo:
- **Por ID**: Búsqueda exacta
- **Por nombre**: Búsqueda parcial (contiene el texto)
- **Por tipo/categoría**: Búsqueda por coincidencia

---

### **0. Salir**

**Entrada:**
```
Elija una opción: 0
```

**Salida:**
```
¡Hasta luego!
```

---

## 🛠️ Tecnologías y Funcionalidades

### **Tecnologías Utilizadas**
- **Lenguaje:** Python 3.10+
- **Módulos estándar:** `csv`, `os`
- **Control de versiones:** Git y GitHub

### **Estructuras de Datos**
- **Listas:** Para almacenar colecciones de mobs
- **Diccionarios:** Para representar cada mob con sus atributos
- **Árbol de directorios:** Estructura jerárquica de 3 niveles

### **Funcionalidades Implementadas**

#### **1. Listar Mobs (Recursivo)**
- Recorrido recursivo de toda la jerarquía de carpetas
- Lectura de archivos CSV en cada nivel
- Visualización organizada por categoría
- Límite configurable de resultados mostrados

#### **2. Agregar Mobs**
- Validación de ID único y numérico
- Verificación de nombres sin duplicados
- Tipos permitidos: hostile, passive, animal, mob, water_creature
- Clasificación interactiva en 3 niveles:
  - **Hostilidad:** hostiles/pasivos
  - **Subtipo:** animal/no_muerto/mob/vivo
  - **Movilidad:** caminador/volador/nadador
- Normalización de dimensiones (valores vacíos → "0")
- Persistencia automática en la ruta correcta

#### **3. Actualizar Mobs**
- Búsqueda por ID o nombre (exacta o parcial)
- Menú interactivo de campos modificables
- Validación de unicidad para ID y nombres
- Validación de tipos permitidos
- Múltiples modificaciones en una sesión
- Confirmación antes de aplicar cambios

#### **4. Eliminar Mobs**
- Búsqueda por nombre exacto
- Visualización completa antes de eliminar
- Doble confirmación ("Eliminar" exacto)
- Actualización automática del archivo CSV
- Eliminación de archivos vacíos

#### **5. Buscar Mobs**
- Búsqueda recursiva en todo el árbol
- Filtrado por cualquier campo (name, type, category, etc.)
- Búsqueda exacta para IDs
- Búsqueda parcial para nombres
- Muestra ubicación en el árbol de cada resultado

#### **6. Generación de Jerarquía**
- Lectura del archivo mobs.csv original
- Clasificación automática según reglas del dominio:
  - **Hostilidad:** Derivada del campo "category"
  - **Subtipo:** Derivado de "type" y análisis del nombre
  - **Movilidad:** Basada en listas predefinidas
- Creación recursiva de estructura de carpetas
- Escritura de archivos CSV en las hojas del árbol

#### **7. Validaciones y Manejo de Errores**
- Control de formato en archivos CSV
- Validación de tipos de datos
- Prevención de duplicados (ID y nombre)
- Normalización de campos vacíos
- Mensajes claros de error
- Manejo de excepciones para entradas inválidas
- Prevención de caídas del programa

### **Estructura Modular**

```
tp_integrador_prog1/
│
├── main.py                  # Punto de entrada y menú principal
├── mobs.csv                 # Dataset original con 148 mobs
├── README.md                # Documentación del proyecto
│
├── minecraft/               # Jerarquía generada automáticamente
│   ├── hostiles/
│   │   ├── animal/
│   │   │   └── caminador/
│   │   │       └── mobs.csv
│   │   ├── no_muerto/
│   │   │   └── caminador/
│   │   │       └── mobs.csv
│   │   ├── vivo/
│   │   │   ├── caminador/
│   │   │   │   └── mobs.csv
│   │   │   ├── volador/
│   │   │   │   └── mobs.csv
│   │   │   └── nadador/
│   │   │       └── mobs.csv
│   │   └── mob/
│   │       ├── caminador/
│   │       │   └── mobs.csv
│   │       └── volador/
│   │           └── mobs.csv
│   └── pasivos/
│       ├── animal/
│       │   ├── caminador/
│       │   │   └── mobs.csv
│       │   ├── volador/
│       │   │   └── mobs.csv
│       │   └── nadador/
│       │       └── mobs.csv
│       ├── mob/
│       │   └── caminador/
│       │       └── mobs.csv
│       └── no_muerto/
│           └── caminador/
│               └── mobs.csv
│
└── mod/                     # Módulo de utilidades
    ├── __init__.py
    ├── crud.py              # Operaciones CRUD recursivas
    ├── etl.py               # ETL y generación de jerarquía
    └── utils.py             # Funciones auxiliares
```

### **Principios de Diseño**
- **Recursividad pura:** Sin uso de `os.walk` u otras utilidades de alto nivel
- **Modularización:** Separación CRUD/ETL/Helpers
- **Reutilización:** Funciones auxiliares compartidas
- **Legibilidad:** Código comentado y nombres descriptivos
- **Robustez:** Validaciones exhaustivas y manejo de errores
- **Persistencia:** Datos organizados en sistema de archivos

---

## 📊 Implementación Recursiva

### **Concepto de Recursividad Aplicado**

El proyecto utiliza recursividad explícita en todas las operaciones para recorrer la estructura de árbol de directorios:

#### **1. Generación de Jerarquía**

```python
def _escribir_jerarquia_recursiva(ruta, filas, niveles, posicion):
    # CASO BASE: sin más niveles, escribir mobs.csv
    if posicion == len(niveles):
        escribir_csv(os.path.join(ruta, "mobs.csv"), filas)
        return
    
    # PASO RECURSIVO: agrupar y descender
    nivel_actual = niveles[posicion]  # "hostilidad", "subtipo", "movilidad"
    
    for valor in valores_distintos_del_nivel:
        subconjunto = filtrar_filas(filas, nivel_actual, valor)
        nueva_ruta = os.path.join(ruta, valor)
        
        # Llamada recursiva al siguiente nivel
        _escribir_jerarquia_recursiva(
            nueva_ruta, subconjunto, niveles, posicion + 1
        )
```

**Funcionamiento:**
1. **Primera llamada** (posición 0): Agrupa por hostilidad (hostiles/pasivos)
2. **Segunda llamada** (posición 1): Agrupa por subtipo (animal/vivo/mob/no_muerto)
3. **Tercera llamada** (posición 2): Agrupa por movilidad (caminador/volador/nadador)
4. **Caso base** (posición 3): Escribe el archivo mobs.csv

#### **2. Listar Recursivo**

```python
def _listar(ruta):
    # Caso base: si hay mobs.csv, leerlo y mostrar
    if os.path.exists(os.path.join(ruta, "mobs.csv")):
        filas = leer_csv(ruta_csv)
        for fila in filas:
            print(formatear_mob(fila))
    
    # Recursión: procesar subdirectorios
    for elemento in os.listdir(ruta):
        ruta_elemento = os.path.join(ruta, elemento)
        if os.path.isdir(ruta_elemento):
            _listar(ruta_elemento)
```

#### **3. Buscar Recursivo**

```python
def _buscar_recursivo_en_directorio(ruta, coincidencias, campo, valor):
    # Caso base: buscar en mobs.csv de esta carpeta
    ruta_csv = os.path.join(ruta, "mobs.csv")
    if os.path.exists(ruta_csv):
        filas = leer_csv(ruta_csv)
        for fila in filas:
            if valor.lower() in str(fila.get(campo, "")).lower():
                coincidencias.append(fila)
    
    # Recursión: buscar en subdirectorios
    for elemento in os.listdir(ruta):
        ruta_hija = os.path.join(ruta, elemento)
        if os.path.isdir(ruta_hija):
            _buscar_recursivo_en_directorio(ruta_hija, coincidencias, campo, valor)
```

---

## 🎯 Estructura de la Jerarquía

### **Reglas de Clasificación**

#### **Nivel 1: Hostilidad**
- **Origen:** Campo `category` del CSV
- **Mapeo:**
  - `"Hostile mobs"` → `hostiles/`
  - `"Passive mobs"` → `pasivos/`

#### **Nivel 2: Subtipo**
- **Origen:** Campos `type` y `name`
- **Lógica:**
  ```python
  if nombre in ["zombie", "skeleton", "drowned", "husk", ...]:
      return "no_muerto"
  elif type in ["water_creature", "animal", "passive"]:
      return "animal"
  elif type == "hostile":
      return "vivo"
  elif type == "mob":
      return "mob"
  ```

#### **Nivel 3: Movilidad**
- **Origen:** Nombre específico del mob
- **Listas predefinidas:**
  ```python
  VOLADORES = {"bat", "bee", "parrot", "phantom", "vex", "blaze", "ghast"}
  NADADORES = {"cod", "axolotl", "dolphin", "guardian", "squid", "turtle"}
  # Por defecto: "caminador"
  ```

### **Ejemplos de Clasificación**

| Mob | Category | Type | Hostilidad | Subtipo | Movilidad | Ruta Final |
|-----|----------|------|------------|---------|-----------|------------|
| Blaze | Hostile mobs | hostile | hostiles | vivo | volador | `hostiles/vivo/volador/` |
| Axolotl | Passive mobs | animal | pasivos | animal | nadador | `pasivos/animal/nadador/` |
| Zombie | Hostile mobs | hostile | hostiles | no_muerto | caminador | `hostiles/no_muerto/caminador/` |
| Cow | Passive mobs | animal | pasivos | animal | caminador | `pasivos/animal/caminador/` |

---

## 📝 Conclusión

Este proyecto ha permitido consolidar conocimientos fundamentales de programación estructurada en Python, demostrando la capacidad de:

1. **Gestionar estructuras jerárquicas:** Mediante el uso de árboles de directorios de 3 niveles, logramos organizar 148 mobs de forma lógica y eficiente.

2. **Implementar recursividad:** Aplicamos recursividad explícita en todas las operaciones CRUD, permitiendo recorrer y manipular estructuras de árbol sin usar funciones de alto nivel como `os.walk`.

3. **Persistir datos jerárquicamente:** Los datos se organizan físicamente en el sistema de archivos, reflejando la clasificación lógica de los mobs.

4. **Clasificar automáticamente:** Desarrollamos algoritmos que derivan propiedades (hostilidad, subtipo, movilidad) según reglas del dominio de Minecraft.

5. **Validar exhaustivamente:** Implementamos validaciones robustas que previenen duplicados, datos inconsistentes y errores de ejecución.

6. **Modularizar código:** La separación en módulos (`crud.py`, `etl.py`) facilitó el desarrollo colaborativo y el mantenimiento.

### **Aprendizajes Clave**

- La importancia de **diseñar estructuras de datos** que reflejen la lógica del dominio del problema.
- El poder de la **recursividad** para resolver problemas de recorrido de estructuras jerárquicas.
- La necesidad de **validar datos** en múltiples puntos para garantizar integridad.
- El valor de la **persistencia organizada** para facilitar consultas y análisis.
- La efectividad del **trabajo en equipo** con división clara de responsabilidades.

---
**Desarrollado con 💻 por Maximo Franco y Octavio Fiore | TUP - UTN | 2025**