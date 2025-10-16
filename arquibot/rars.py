import os
import sys
import re
import requests
import subprocess
import arquibot.util as util
import arquibot.ansi as ansi


# ── VERSION DE ARQUITBOT
VERSION = 0.2


# ──────────────────────────────────────────
# ── MODULO RARS
# ──────────────────────────────────────────
class Rars:

    # ─── Anchura de las lineas del encabezado
    WIDTH = 40

    # ── Nombre del ejecutable del Rars
    NAME = "rars1_6.jar"

    # ── URL de descarga del RARs
    URL = "https://github.com/TheThirdOne/rars/releases/download/v1.6/"\
          f"{NAME}"

    # ── Numero maximo de ciclos a probar
    MAX_STEPS = 10000

    # ── Nombre del fichero MAIN a ensamblar
    MAIN_ASM = "main.s"

    # ────── SEGMENTO DE CODIGO
    # ── Fichero donde volcar el segmento de código
    TEXT = "text.hex"

    # ── El programa analizado tiene segmento de Codigo
    HAS_TEXT = False

    # ────── SEGMENTO DE DATOS
    # ── Fichero donde volcar el segmento de datos
    DATA = "data.hex"

    # ── Indicar si el programa debe tener segmento de datos o no
    EXPECTED_DATA = False

    # ── El programa analizado tiene segmento de datos
    HAS_DATA = False

    # ── Guardar las salidas del rars y del programa
    # ── Al ejecutar el Rars
    stderr = ""
    stdout = ""

    # ── Indica si se han producido errores
    errors = False

    # ── ciclos
    ciclos = 0

    # ── Registros
    regs = []

    # ── Numero de instrucciones
    instrucciones = 0

    # ── Variables
    variables = []

    # ───────────────────────────────────────────────────────────────────────
    # ── CONSTRUCTOR
    # ── Entradas:
    # ──  * main: Nombre del fichero ensamblador principal
    # ──  * expected_data: Indicar si el programa debe tener segmento de datos
    # ──  * bonus: Numero de instrucciones maximo para conseguir
    # ──           los bonus
    # ───────────────────────────────────────────────────────────────────────
    def __init__(self,
                 main: str,
                 expected_data: bool = False,
                 bonus: int = 2):

        # -- Guardar los parametros pasados
        Rars.MAIN_ASM = main
        Rars.EXPECTED_DATA = expected_data
        Rars.bonus = bonus

        # ── Mostrar el encabezado
        Rars.show_header()

        # -- Comprobar si el rars existe
        # -- Si no es asi se descarga
        Rars.check()

        # -- Borrar los archivos temporales generados
        # -- en ejecuciones anteriores
        Rars.delete_data()
        Rars.delete_text()

        # --- Comprobar si el fichero asm existe
        Rars.check_main_asm()

        # -- Ejecutar el Rars!
        Rars.exec()

        # -- Comprobar si hay runtime error
        Rars.check_runtime_error()

        # -- Comprobar si es un error de ensamblado
        Rars.check_asm_errors()

        # -- Comprobar si se ha generado el fichero con el volcado de memoria
        # -- si no se ha generado es porque no se ha declaro el segmento
        # --- de datos
        Rars.check_data()

        # --- Comprobar si se ha generado el segmento de codigo
        Rars.check_text()

        # ---- Leer la salida del Rars para obtener los registros y los ciclos
        # ---- Actualiza Rars.ciclos y Rars.regs
        Rars.process_output()

        # -- Analizar el segmento de codigo
        Rars.process_code()

        # -- Comprobar como se ha realizado la salida del programa
        Rars.check_exit()

        # -- Leer todas las variables del segmento de datos
        Rars.read_variables()

    # ────────────────────────────────────────────────────────
    # ── Imprimir el encabezado de ARQUI-BOTS
    # ────────────────────────────────────────────────────────
    def show_header():
        util.line(ansi.YELLOW, Rars.WIDTH)
        print(f"{ansi.YELLOW}ARQUI-BOT {VERSION}")
        util.line(ansi.YELLOW, Rars.WIDTH)

        # ── Volver a color normal
        print(ansi.DEFAULT, end="")

    # ────────────────────────────────────────────────────────────────────────
    # ── Imprimir un mensaje de error
    # ──  ENTRADAS:
    # ──    * emsg:  Mensaje de error a mostrar
    # ──    * violation: Indica si mostrar mensaje dicion de violacion de
    # ──                 especificaciones
    # ────────────────────────────────────────────────────────────────────────
    def print_error(emsg: str, violation: bool = False):

        print(f"> ❌️ {ansi.RED}ERROR: {ansi.LWHITE}{emsg}{ansi.DEFAULT}")
        if violation:
            print(f"{ansi.LMAGENTA}     🔥️ VIOLACION DE ESPECIFICACIONES")
            print(f"{ansi.DEFAULT}", end='', flush=True)

    # ──────────────────────────────────────────────────
    # ── EXISTS()  Comprobar si el fichero ejecutable
    # ── del rars se encuentra en el directorio actual
    # ── Devuelve:
    # ──   * true: Existe!
    # ──   * false: No existe
    # ──────────────────────────────────────────────────
    def exists() -> bool:
        return os.path.exists(Rars.NAME)

    # ──────────────────────────────────────────────────
    # ── DOWNLOAD.  Descargar el ejecutable del RARS
    # ── No se comprueba si ya existe en el directorio
    # ── el ejecutable
    # ──────────────────────────────────────────────────
    def download():

        # ── Realizar la descarga!
        print("  > Descargando RARS")
        response = requests.get(Rars.URL)

        # ── Ha ocurrido un error en la descarga
        # ── Mostrar un error y terminar!
        if response.status_code != 200:

            util.line(ansi.LRED, 20)
            print(f"{ansi.LRED}ERROR {ansi.DEFAULT}")
            util.line(ansi.LRED, 20)
            print("No se ha podido realizar la descarga")
            print(f"Respuesta: {response.status_code} ({response.text})")
            print(ansi.DEFAULT)
            sys.exit(1)

        # ── Descarga completada!
        contenido = response.content

        # ── Escribir el contenido del archivo en un fichero
        with open(Rars.NAME, 'wb') as archivo:
            archivo.write(contenido)

        print(f"  > {ansi.LGREEN}OK! {ansi.DEFAULT}")
        print()

    # ──────────────────────────────────────────────────
    # ── CHECK. Comprobar si el rars existe
    # ── si es así, se descarga!
    # ──────────────────────────────────────────────────
    def check():
        if not Rars.exists():
            print("> 🤚 RARS no existe")
            Rars.download()

        print("> ☑️  RARS EXISTE")

    # ──────────────────────────────────────────────────
    # ── DELETE_DATA.  Borrar el archivo donde esta
    # ── el volcado el segmento de datos
    # ──────────────────────────────────────────────────
    def delete_data():
        if os.path.exists(Rars.DATA):
            os.remove(Rars.DATA)
            print(f"🧹️Eliminado {Rars.DATA} antiguo")

    # ──────────────────────────────────────────────────
    # ── DELETE_TEXT.  Borrar el archivo donde esta
    # ── el volcado el segmento de codigo
    # ──────────────────────────────────────────────────
    def delete_text():
        if os.path.exists(Rars.TEXT):
            os.remove(Rars.TEXT)
            print(f"🧹️Eliminado {Rars.TEXT} antiguo")

    # ──────────────────────────────────────────────────
    # ── CHECK_MAIN_ASM.  Comprobar si el fichero asm
    # ── principal existe
    # ──────────────────────────────────────────────────
    def check_main_asm():
        if os.path.exists(Rars.MAIN_ASM):
            print(f"> ✅️ {Rars.MAIN_ASM} existe")
        else:
            Rars.print_error(f"{ansi.YELLOW}{Rars.MAIN_ASM}{ansi.LWHITE}"
                             " no encontrado", violation=True)
            print()
            sys.exit()

    # ──────────────────────────────────────────────────
    # ── EXEC.  Ejecutar el RARs
    # ──────────────────────────────────────────────────
    def exec():

        # -- Probando fichero fuente
        print(f"> Probando: {Rars.MAIN_ASM}")

        # -- Comando a ejecutar
        cmd_str = f"java -jar {Rars.NAME} "\
                  f"x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 "\
                  f"x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 "\
                  f"x25 x26 x27 x28 x29 x30 x31 "\
                  f"nc me ic {Rars.MAX_STEPS} "\
                  f"dump 0x10010000-0x10010010 HexText {Rars.DATA} "\
                  f"dump .text HexText {Rars.TEXT} {Rars.MAIN_ASM}"

        # -- Convertirlo a lista, colocando cada argumento en un item
        # -- Necesario para ejecutar el comando con subprocess.run()
        cmd = cmd_str.split(" ")

        # -- Mostrar el comando que se ejecuta
        print("> Ejecutando: ", end="")
        print(ansi.CYAN + cmd_str + ansi.DEFAULT)

        # -- Ejecutar el comando!
        resultado = subprocess.run(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # -- Guardar la salidas estandar y de error
        # --  Salida: mensajes emitidos por el programa ensamblador
        # --  error: Mensajes emitidos por el RARs (informativos o de error)
        Rars.stdout = resultado.stdout.decode()
        Rars.stderr = resultado.stderr.decode()

    # ────────────────────────────────────────────────────────────
    # ── CHECK_runtime_error.  Comprobar los errores en tiempo
    # ── de ejecucion al ejecutar el RARs
    # ────────────────────────────────────────────────────────────
    def check_runtime_error():

        # -- Comprobar si hay runtime error
        patron = r"Error in .*/([^/]+)\sline\s(\d+): "\
                r"Runtime exception at (0x[0-9a-fA-F]+): (.+)"
        resultado = re.search(patron, Rars.stderr)

        if resultado:
            print("> ❌️ ERROR en tiempo de ejecución. Ha PETADO 😱️😱️")
            archivo = resultado.group(1)
            linea = resultado.group(2)
            address = resultado.group(3)
            msg = resultado.group(4)
            print(f"🔹️Fichero: {archivo}")
            print(f"🔹️Línea: {linea}")
            print(f"🔹️Dirección: {address}")
            print(f"🔹️Error: {msg}")
            print()
            error_output_list = Rars.stderr.split("\n")
            print(ansi.RED + f"{error_output_list[0]}\n" + ansi.DEFAULT)
            sys.exit(1)

    # ────────────────────────────────────────────────────────────
    # ── CHECK_asm_errors.  Comprobar errores de ensamblado
    # ────────────────────────────────────────────────────────────
    def check_asm_errors():
        patron = r"Error in .*/[^/]+\sline\s(\d+).+: (.+)"
        resultado = re.search(patron, Rars.stderr)
        if resultado:
            print("> ❌️ ERROR: El programa NO ensambla 😱️😱️")
            linea = resultado.group(1)
            msg = resultado.group(2)
            print(f"🔹️Línea: {linea}")
            print(f"🔹️Error: {msg}")
            print()
            error_output_list = Rars.stderr.split("\n")
            print(ansi.RED + f"{error_output_list[0]}\n" + ansi.DEFAULT)
            sys.exit(1)

    # ────────────────────────────────────────────────────────────
    # ── CHECK_DATA.  Comprobar si se ha generado el fichero
    # ── con el volcado del segmento de datos
    # ────────────────────────────────────────────────────────────
    def check_data():
        # -- Comprobar si se ha generado el fichero con el volcado
        # -- de memoria. Si no se ha generado es porque no se ha declaro
        #  el segmento de datos
        if os.path.exists(Rars.DATA):

            # -- Tiene segmento de datos
            Rars.HAS_DATA = True

            # -- Imprimir mensaje según si se espera o no que tenga
            # -- segmento de datos
            if Rars.EXPECTED_DATA:
                # -- Se espera que tenga segmento de datos: OK
                print("> ✅️ ", end='')

            else:
                # -- No es obligatorio que tengo segmento de datos
                print("> ☑️ ", end='')

            print(f"Hay segmento de datos{Rars.DATA}")

        # -- NO HAY Segmento de datos
        # -- No tiene por qué ser un error. Depende de si se ha especificado
        # -- o no en el enunciado
        else:

            # -- El enunciado requiere que HAYA segmento de datos
            if Rars.EXPECTED_DATA:
                Rars.print_error("No hay segmento de DATOS", violation=True)
                Rars.errors = True

            # -- No tiene segmento de datos, y el enunciado NO lo requiere
            else:
                print("> ✅️ NO hay segmento de datos")

    # ────────────────────────────────────────────────────────────
    # ── CHECK_TEXT.  Comprobar si se ha generado el fichero
    # ── con el volcado del segmento de codigo
    # ────────────────────────────────────────────────────────────
    def check_text():
        # -- Comprobar si se ha generado el fichero con el volcado
        # -- del segmento de codigo. Si no se ha generado es porque
        # -- el programa no tiene la directiva .text
        if os.path.exists(Rars.TEXT):
            print(f"> ✅️ {Rars.TEXT} generado")
            Rars.HAS_TEXT = True
        else:
            Rars.print_error("No hay segmento de CODIGO!", violation=True)
            Rars.errors = True

    # ────────────────────────────────────────────────────────────
    # ── READ_VARIABLES. Leer el segmento de datos del fichero
    # ── generado y devolver una lista con ellas
    # ────────────────────────────────────────────────────────────
    def read_variables():
        try:
            # -- Leer el fichero con el segmento de datos
            # -- Se lee como una cadena de texto
            with open(Rars.DATA, "r") as data_file:
                data_str = data_file.read()

        except FileNotFoundError:
            print("> ❌️ ERROR: Fichero data.hex NO generado")

        # -- Obtener una lista (de texto) con los valores de la
        # -- memoria
        try:
            mem_str = data_str.split("\n")
        except UnboundLocalError:
            print("ERROR DESCONOCIDO!")
            mem_str = ""

        # -- Meter todas las variables en una lista, convertidos
        # -- a enteros
        variables = []
        for val in mem_str:
            if val != '':
                variables.append(int(val, 16))

        # -- Guardar las variables
        Rars.variables = variables

        # -- Devolver la lista de variables
        return variables

    # ────────────────────────────────────────────────────────────
    # ── READ_REGS. Leer los registros
    # ────────────────────────────────────────────────────────────
    def read_regs():
        return Rars.regs

    # ──────────────────────────────────────────────────────────────────────
    # ── PROCESS_OUTPUT. Procesar la salida del RARs (NO la del programa)
    # ── A partir de esta salida se determina si la salida se ha realizado
    # ── llamando a exit, el número de ciclos y los registros
    # ──────────────────────────────────────────────────────────────────────
    def process_output():

        # -- Obtener la salida de error del RARs
        # -- como una lista. Una linea en cada posicion
        contenido = Rars.stderr.strip().split("\n")
        # print(contenido)

        # -- Leer los ciclos
        # -- Se encuentran en la linea 2
        Rars.ciclos = contenido[2]

        # -- Lectura de los registros
        # -- Los registros empiezan en la linea 3
        regs_str = contenido[3:]

        # -- Recorrer los registros
        for val in regs_str:

            # -- Parsear el registro actual y
            # -- almacenarlo
            try:
                x_str = val.split("\t")[1]
                Rars.regs.append(int(x_str, 16))
            except IndexError:
                # -- Lo parseado no es un registro
                # -- es un mensaje diferente
                # -- No hacemos nada
                pass

    # ──────────────────────────────────────────────────────────────────────
    # ── PROCESS_CODE. Procesar el segmento de codigo
    # ── Se actualiza el numero de instrucciones
    # ──────────────────────────────────────────────────────────────────────
    def process_code():
        # -- Leer el fichero del codigo
        try:
            with open(Rars.TEXT, "r") as code_file:
                contenido = code_file.read()
                code = contenido.strip().split("\n")
                Rars.instrucciones = len(code)

        except FileNotFoundError:
            # -- No hay segmento de codigo
            # -- No se muestra mensaje de error porque ya se ha
            # -- hecho previamente
            pass

    # ──────────────────────────────────────────────────────────────────────
    # ── CHECK_EXIT. Comprobar la terminacion del programa
    # ── y emitir los mensajes de error correspondientes
    # ──────────────────────────────────────────────────────────────────────
    def check_exit():
        # --- Comprobar si el programa no termina de forma controlada
        if "dropping off" in Rars.stderr:
            Rars.print_error("No hay EXIT")
            Rars.errors = True

        # --- Comprobar si el programa termina con normalidad, llamando a EXIT
        if "calling exit" in Rars.stderr:
            print("> ✅️ El programa termina llamando a EXIT")

    # ──────────────────────────────────────────────────────────────────────
    # ── CHECK_VARIABLES. Comprobar si las variables tienen los valores
    # ── correctos
    # ── ENTRADA:
    # ──   * data_ok: Diccionario con las variables y sus valores correctos
    # ──────────────────────────────────────────────────────────────────────
    def check_variables(data_ok: dict):
        i = 0
        for var, value_ok in data_ok.items():

            data = Rars.variables[i]
            if data == value_ok:
                print(f"> ✅️ {var}: {hex(data)}")
            else:
                print(f"> ❌️ {var}: {hex(data)}."
                      f"Debería ser: {hex(value_ok)}")
                Rars.errors = True

            i += 1

    # ──────────────────────────────────────────────────────────────────────
    # ── EXIT. Terminar. Mostrar las instrucciones, ciclos y bonus
    # ──────────────────────────────────────────────────────────────────────
    def exit():
        # -- Mostrar informacion
        print(f"> Instrucciones totales: {Rars.instrucciones}")
        print(f"> Ciclos de ejecución: {Rars.ciclos}")

        # -- Comprobar BONUS
        # -- Solo si no hay errores previos
        if not Rars.errors:
            print("> Comprobando BONUS...")
            ok_inst = False

            # -- Comprobar instrucciones
            if Rars.instrucciones <= Rars.bonus:
                print(f"  > ✅️ Máximo de {Rars.bonus} instrucciones")
                ok_inst = True
            else:
                print(f"  > ❌️ Más de {Rars.bonus} instrucciones...")

            # -- Comprobacion final de Bonus
            if ok_inst:
                print(f"  > 🎖️  {ansi.YELLOW}BONUS CONSEGUIDO!!!"
                      f"{ansi.DEFAULT}")
            else:
                print("  > No conseguidos...")

        util.line(ansi.YELLOW, Rars.WIDTH)

        print()
        if Rars.stdout:
            print("SALIDA programa:\n", Rars.stdout)

        # print(f"{ansi.WHITE}Pulsa ENTER...")
        # input()
