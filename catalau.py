            # -*- coding: utf-8 -*-
# Script: Combo Generator Cata Visual
# Compatible con QPython 3 y Termux en Android

import os
import random
import string
import sys
import time

# --- COLORES ---
PURPLE = "\033[95m"
FUCHSIA = "\033[35m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# --- LOGO NUEVO ---
ascii_cata = f"""
{CYAN}╔══════════════════════════════════════════════════╗
{PURPLE}▄▀ ▄▀▄ ▀█▀ ▄▀▄
{FUCHSIA}█░ █▀█ ░█░ █▀█
{PURPLE}░▀ ▀░▀ ░▀░ ▀░▀
{CYAN}╚══════════════════════════════════════════════════╝
{YELLOW}           💀 Combo Creator Tool 💀{RESET}
"""

# --- FUNCIONES ---
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_nombres(ruta):
    """Cargar lista de nombres evitando error de codificación"""
    if not os.path.exists(ruta):
        print(f"{RED}[!] Archivo no encontrado.{RESET}")
        return []
    try:
        # PRIMERO INTENTA CON UTF-8
        with open(ruta, 'r', encoding='utf-8') as f:
            nombres = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        # SI FALLA, USA LATIN-1 (FUNCIONA EN TERMUX)
        with open(ruta, 'r', encoding='latin-1') as f:
            nombres = [line.strip() for line in f if line.strip()]
    # Eliminar duplicados manteniendo orden
    nombres = list(dict.fromkeys(nombres))
    return nombres

def generar_contrasena(longitud):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(longitud))

def barra_progreso(iteracion, total, longitud=35):
    porcentaje = (iteracion / total)
    relleno = int(longitud * porcentaje)
    barra = f"[{'█'*relleno}{' '*(longitud-relleno)}] {int(porcentaje*100)}%"
    print(f"\r{GREEN}Progreso: {barra}{RESET}", end="")

def crear_combos(nombres, longitud_pass, combinacion="nombre+pass"):
    combos = []
    total = len(nombres)
    print(f"{BLUE}[*] Generando {total} combos...{RESET}")
    for idx, nombre in enumerate(nombres, 1):
        password = generar_contrasena(longitud_pass)
        if combinacion == "nombre+pass":
            combo = f"{nombre}:{password}"
        elif combinacion == "pass+nombre":
            combo = f"{password}:{nombre}"
        elif combinacion == "nombre_nombre+pass":
            combo = f"{nombre}_{nombre}:{password}"
        else:
            combo = f"{nombre}:{password}"
        combos.append(combo)
        barra_progreso(idx, total)
        time.sleep(0.005)
    print()
    return combos

def guardar_combos(combos, ruta, nombre_archivo):
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    ruta_completa = os.path.join(ruta, nombre_archivo)
    # Guardar siempre en UTF-8 para que se vea bien después
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        for combo in combos:
            f.write(combo + '\n')
    print(f"\n{GREEN}[✓] ARCHIVO GUARDADO EXITOSAMENTE!")
    print(f"[→] Ubicación: {ruta_completa}{RESET}")

def eliminar_duplicados():
    ruta_entrada = input(f"{YELLOW}[?] Ruta del archivo a limpiar: {RESET}").strip()
    if not os.path.isfile(ruta_entrada):
        print(f"{RED}[!] Archivo no existe.{RESET}")
        return
    try:
        with open(ruta_entrada, 'r', encoding='utf-8') as f:
            lineas = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        with open(ruta_entrada, 'r', encoding='latin-1') as f:
            lineas = [line.strip() for line in f if line.strip()]
    lineas_unicas = list(dict.fromkeys(lineas))
    eliminados = len(lineas) - len(lineas_unicas)
    ruta_salida = "/storage/emulated/0/CATA/SinDuplicados"
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    nombre_base = os.path.basename(ruta_entrada)
    archivo_salida = os.path.join(ruta_salida, f"LIMPIO_{nombre_base}")
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for linea in lineas_unicas:
            f.write(linea + '\n')
    print(f"{GREEN}[✓] Proceso terminado!")
    print(f"[→] Líneas eliminadas: {eliminados}")
    print(f"[→] Archivo guardado en: {archivo_salida}{RESET}")

# --- PROGRAMA PRINCIPAL ---
def main():
    longitud_pass = 8
    combinacion = "nombre+pass"
    while True:
        limpiar_pantalla()
        print(ascii_cata)
        print(f"{BLUE}════════════════════ MENU PRINCIPAL ════════════════════{RESET}")
        print(f"{GREEN}[1] Crear Combo con Lista de Nombres")
        print(f"{CYAN}[2] Eliminar Duplicados de un Archivo")
        print(f"{YELLOW}[3] Configurar Longitud de Contraseña")
        print(f"{PURPLE}[4] Cambiar Formato de Combinación")
        print(f"{RED}[0] Salir del Programa{RESET}")
        print(f"{BLUE}════════════════════════════════════════════════════════{RESET}")
        opcion = input(f"\n{GREEN}[+] Elige una opción: {RESET}").strip()

        if opcion == "1":
            print(f"\n{BLUE}--- MODO CREAR COMBO ---{RESET}")
            ruta_nombres = input(f"{YELLOW}[?] Ruta del archivo de nombres: {RESET}").strip()
            nombres = cargar_nombres(ruta_nombres)
            if not nombres:
                input(f"\n{RED}Presiona Enter para volver...{RESET}")
                continue
            print(f"{GREEN}[✓] Se cargaron {len(nombres)} nombres únicos.{RESET}")
            combos = crear_combos(nombres, longitud_pass, combinacion)
            nombre_archivo = input(f"{YELLOW}[?] Nombre para guardar (ej: combos.txt): {RESET}").strip()
            if not nombre_archivo.endswith('.txt'):
                nombre_archivo += '.txt'
            guardar_combos(combos, "/storage/emulated/0/CATA/Combos", nombre_archivo)
            input(f"\n{GREEN}Presiona Enter para continuar...{RESET}")

        elif opcion == "2":
            print(f"\n{CYAN}--- MODO ELIMINAR DUPLICADOS ---{RESET}")
            eliminar_duplicados()
            input(f"\n{GREEN}Presiona Enter para continuar...{RESET}")

        elif opcion == "3":
            print(f"\n{YELLOW}--- CONFIGURAR LONGITUD ---{RESET}")
            try:
                valor = int(input(f"[?] Ingresa nueva longitud (actual: {longitud_pass}): {RESET}"))
                if valor > 0:
                    longitud_pass = valor
                    print(f"{GREEN}[✓] Longitud cambiada a: {longitud_pass} caracteres{RESET}")
                else:
                    print(f"{RED}[!] Debe ser un número positivo.{RESET}")
            except ValueError:
                print(f"{RED}[!] Valor no válido.{RESET}")
            input(f"\nPresiona Enter para continuar...{RESET}")

        elif opcion == "4":
            print(f"\n{PURPLE}--- CONFIGURAR FORMATO ---{RESET}")
            print(f"[1] nombre:contraseña   (ej: cata:1234)")
            print(f"[2] contraseña:nombre   (ej: 1234:cata)")
            print(f"[3] nombre_nombre:pass  (ej: cata_cata:1234)")
            subop = input(f"\n{GREEN}[+] Elige formato: {RESET}")
            if subop == "1":
                combinacion = "nombre+pass"
            elif subop == "2":
                combinacion = "pass+nombre"
            elif subop == "3":
                combinacion = "nombre_nombre+pass"
            else:
                combinacion = "nombre+pass"
            print(f"{GREEN}[✓] Formato establecido: {combinacion}{RESET}")
            input(f"\nPresiona Enter para continuar...{RESET}")

        elif opcion == "0":
            limpiar_pantalla()
            print(f"{GREEN}[✓] Saliendo del programa... ¡Hasta luego! 👋{RESET}")
            sys.exit()

        else:
            print(f"{RED}[!] Opción inválida, intenta de nuevo.{RESET}")
            input(f"Presiona Enter...{RESET}")

if __name__ == "__main__":
    main()
