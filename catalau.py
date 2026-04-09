 # -*- coding: utf-8 -*-
import os
import random

# Colores para terminal
class Colores:
    MORADO = '\033[95m'
    FUXIA = '\033[35m'
    VERDE = '\033[92m'
    ROJO = '\033[91m'
    AZUL = '\033[94m'
    FIN = '\033[0m'

def mostrar_titulo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Colores.MORADO}{'='*35}")
    print(f"{Colores.FUXIA}           TOOLS CATA")
    print(f"{Colores.VERDE}{'='*35}{Colores.FIN}")

def generar_password(longitud=8):
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(random.choices(caracteres, k=longitud))

def crear_combo():
    print(f"\n{Colores.AZUL}--- CREAR NUEVO COMBO ---{Colores.FIN}")
    ruta_nombres = input(f"{Colores.MORADO}Ingresa la ruta del archivo de nombres: {Colores.FIN}")
    
    if not os.path.isfile(ruta_nombres):
        print(f"{Colores.ROJO}✖ Archivo no encontrado.{Colores.FIN}")
        input("\nPresiona Enter para continuar...")
        return

    try:
        with open(ruta_nombres, "r", encoding="utf-8") as f:
            nombres = list(set(f.read().splitlines()))
    except Exception as e:
        print(f"{Colores.ROJO}Error al leer el archivo: {e}{Colores.FIN}")
        input("\nPresiona Enter para continuar...")
        return

    if not nombres:
        print(f"{Colores.ROJO}El archivo está vacío.{Colores.FIN}")
        input("\nPresiona Enter para continuar...")
        return

    nombre_salida = input(f"{Colores.VERDE}Nombre para el archivo final (sin .txt): {Colores.FIN}")
    ruta_guardar = "/storage/emulated/0/CATA/Combos"
    os.makedirs(ruta_guardar, exist_ok=True)

    combos = [f"{nombre}:{generar_password()}" for nombre in nombres]
    salida_path = os.path.join(ruta_guardar, f"{nombre_salida}.txt")

    with open(salida_path, "w", encoding="utf-8") as f:
        f.write("\n".join(combos))

    print(f"{Colores.VERDE}✓ Combo creado exitosamente!{Colores.FIN}")
    print(f"{Colores.FUXIA}Ubicación: {salida_path}{Colores.FIN}")
    input("\nPresiona Enter para continuar...")

def eliminar_duplicados():
    print(f"\n{Colores.AZUL}--- ELIMINAR DUPLICADOS ---{Colores.FIN}")
    ruta_entrada = input(f"{Colores.MORADO}Ingresa la ruta de la carpeta con archivos: {Colores.FIN}")
    
    if not os.path.isdir(ruta_entrada):
        print(f"{Colores.ROJO}✖ Carpeta no encontrada.{Colores.FIN}")
        input("\nPresiona Enter para continuar...")
        return

    ruta_salida = "/storage/emulated/0/CATA/SinDuplicados"
    os.makedirs(ruta_salida, exist_ok=True)
    contador = 0

    for archivo in os.listdir(ruta_entrada):
        archivo_path = os.path.join(ruta_entrada, archivo)
        if os.path.isfile(archivo_path):
            try:
                with open(archivo_path, "r", encoding="utf-8") as f:
                    lineas_unicas = list(set(f.read().splitlines()))
                
                salida_path = os.path.join(ruta_salida, archivo)
                with open(salida_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lineas_unicas))
                print(f"{Colores.VERDE}✓ Procesado: {archivo}{Colores.FIN}")
                contador += 1
            except Exception as e:
                print(f"{Colores.ROJO}Error en {archivo}: {e}{Colores.FIN}")

    print(f"\n{Colores.FUXIA}Proceso finalizado. Archivos limpios: {contador}{Colores.FIN}")
    print(f"{Colores.FUXIA}Guardados en: {ruta_salida}{Colores.FIN}")
    input("\nPresiona Enter para continuar...")

def menu_principal():
    while True:
        mostrar_titulo()
        print(f"{Colores.AZUL}[1] Crear Combo con contraseñas")
        print(f"{Colores.AZUL}[2] Eliminar Duplicados de archivos")
        print(f"{Colores.ROJO}[3] Salir{Colores.FIN}")
        print(f"{Colores.MORADO}{'-'*35}{Colores.FIN}")

        opcion = input(f"{Colores.VERDE}Selecciona una opción: {Colores.FIN}")

        if opcion == "1":
            crear_combo()
        elif opcion == "2":
            eliminar_duplicados()
        elif opcion == "3":
            print(f"{Colores.FUXIA}¡Hasta luego!{Colores.FIN}")
            break
        else:
            print(f"{Colores.ROJO}Opción no válida.{Colores.FIN}")
            input("Presiona Enter...")

if __name__ == "__main__":
    menu_principal()
