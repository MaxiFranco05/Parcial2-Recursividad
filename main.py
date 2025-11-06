import os
from mod.etl import buscar_interactivo, generar_jerarquia
from mod.crud import listar_interactivo, agregar_interactivo, actualizar_interactivo, eliminar_interactivo


def mostrar_menu():
	print("\n=== Menú de Gestión de Mobs ===")
	print("1) Listar mobs (recursivo)")
	print("2) Agregar mob")
	print("3) Actualizar mob por nombre")
	print("4) Eliminar mob por nombre")
	print("5) Buscar mobs")
	print("0) Salir")

def main():
	# Crear estructura base si no existe
	os.makedirs("minecraft", exist_ok=True)
	# Generar automáticamente la jerarquía (desde mobs.csv) al iniciar
	try:
		generar_jerarquia()
	except Exception:
		# No bloquear el menú si falla la generación automática
		pass
    
	while True:
		mostrar_menu()
		opcion = input("\nElija una opción: ").strip()
        
		if opcion == "1":
			listar_interactivo()
		elif opcion == "2":
			agregar_interactivo()
		elif opcion == "3":
			actualizar_interactivo()
		elif opcion == "4":
			eliminar_interactivo()
		elif opcion == "5":
			buscar_interactivo()
		elif opcion == "0":
			print("¡Hasta luego!")
			break
		else:
			print("Opción no válida. Intenta nuevamente.")
		input("Presione Enter...")

if __name__ == "__main__":
	main()


