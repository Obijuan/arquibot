import os
import sys
import re
import requests
import subprocess
import arquibot.util as util
import arquibot.ansi as ansi


# ── VERSION DE ARQUITBOT
VERSION = 0.7


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

    # Tipo enumerado para indicar el tipo de bonus
    BONUS_INSTRUCCIONES = 0
    BONUS_CICLOS = 1

    # ────── SEGMENTO DE CODIGO
    # ── Fichero donde volcar el segmento de código
    TEXT = "text.hex"

    # ────── SEGMENTO DE DATOS
    # ── Fichero donde volcar el segmento de datos
    DATA = "data.hex"

    # ── Numero de bytes a volcar del segmento de datos
    DATA_SIZE = 256

    # ───────────────────────────────────────────────────────────────────────
    # ── CONSTRUCTOR
    # ── Entradas:
    # ──  * main: Nombre del fichero ensamblador principal
    # ──  * include: Nombre del fichero a incluir
    # ──  * expected_data: Indicar si el programa debe tener segmento de datos
    # ──  * input: Texto a enviar por la entrada estandar
    # ──  * tipo_bonus: Tipo de bonus
    # ──    * Rars.BONUS_INSTRUCCIONES
    # ──    * Rars.BONUS_CILOS
    # ──  * bonus: valor maximo para conseguir los bonus
    # ──     (instrucciones o ciclos)
    # ───────────────────────────────────────────────────────────────────────
    def __init__(self,
                 main: str,
                 include: str = "",
                 deps: list = [],
                 expected_data: bool = False,
                 input: str = "",
                 tipo_bonus: int = BONUS_INSTRUCCIONES,
                 bonus: int = 0):

        # ──────── Guardar los parametros pasados
        self.main_asm = main
        self.expected_data = expected_data
        self.input = input
        self.include_asm = include
        self.tipo_bonus = tipo_bonus
        self.bonus = bonus
        self.deps = deps

        # ── Estado del test
        self.ok = False

        # ── Indica si se han producido errores
        self.errors = False

        # ── El programa analizado tiene segmento de Codigo
        self.has_text = False

        # ── El programa analizado tiene segmento de datos
        self.has_data = False

        # ── Guardar las salidas del rars y del programa
        # ── Al ejecutar el Rars
        self.stderr = ""
        self.stdout = ""

        # ── ciclos
        self.ciclos = 0

        # ── Numero de instrucciones
        self.instrucciones = 0

        # ── Registros
        self.regs = []

        # ── Variables
        self.variables = []

        # ── Mostrar el encabezado
        Rars.show_header()

        # -- Comprobar si el rars existe
        # -- Si no es asi se descarga
        self.check()

        # -- Borrar los archivos temporales generados
        # -- en ejecuciones anteriores
        Rars.delete_data()
        Rars.delete_text()

        # --- Comprobar si el fichero asm existe
        ok = self.check_main_asm()
        if not ok:
            return

        # --- Comprobar si existen las dependencias
        ok = self.check_deps()
        if not ok:
            return

        # --- Comprobar si el fichero a incluir existe
        ok = self.check_include_asm()
        if not ok:
            return

        # -- Ejecutar el Rars!
        self.exec()

        # -- Comprobar si hay runtime error
        # -- Lo suyo seria comprobar primero si hay errores de ensamblado,
        # -- pero al ejecutar se realizan las dos operaciones a la vez:
        # -- ensamblar y ejecutar. El mensaje de error es común, pero en
        # -- el caso de runtime error, el mensaje contiene la palabra clave
        # -- "Runtime exception". Por eso se comprueba primero este tipo
        # -- de error
        ok = self.check_runtime_error()
        if not ok:
            return

        # -- Comprobar si es un error de ensamblado
        ok = self.check_asm_errors()
        if not ok:
            return

        # -- Comprobar si se ha generado el fichero con el volcado de memoria
        # -- si no se ha generado es porque no se ha declaro el segmento
        # --- de datos
        self.check_data()

        # --- Comprobar si se ha generado el segmento de codigo
        ok = self.check_text()
        if not ok:
            return

        # ---- Leer la salida del Rars para obtener los registros y los ciclos
        # ---- Actualiza Rars.ciclos y Rars.regs
        self.process_output()

        # -- Analizar el segmento de codigo
        self.process_code()

        # -- Leer todas las variables del segmento de datos
        self.read_variables()

    # ────────────────────────────────────────────────────────
    # ── Imprimir el encabezado de ARQUI-BOTS
    # ────────────────────────────────────────────────────────
    @staticmethod
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
    def print_error(self, emsg: str, violation: bool = False):

        print(f"> ❌️ {ansi.RED}ERROR: {ansi.LWHITE}{emsg}{ansi.DEFAULT}")
        self.errors = True
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
    @staticmethod
    def exists() -> bool:
        return os.path.exists(Rars.NAME)

    # ──────────────────────────────────────────────────
    # ── DOWNLOAD.  Descargar el ejecutable del RARS
    # ── No se comprueba si ya existe en el directorio
    # ── el ejecutable
    # ──────────────────────────────────────────────────
    def download(self):

        # ── Realizar la descarga!
        print("  > Descargando RARS")
        try:
            response = requests.get(Rars.URL)
        except requests.exceptions.ConnectionError:

            # -- No hay Rars. Terminar!
            # -- NO hay conexion a Internet
            self.print_error("No se puede descargar el RARs")
            print("> Abortando...\n")
            sys.exit(1)

        # ── Parece que sí hay internet, pero
        # ── Ha ocurrido otro error en la descarga
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
    def check(self):
        if not self.exists():
            print("> 🤚 RARS no existe")
            self.download()

        print("> ☑️  RARS EXISTE")

    # ──────────────────────────────────────────────────
    # ── DELETE_DATA.  Borrar el archivo donde esta
    # ── el volcado el segmento de datos
    # ──────────────────────────────────────────────────
    @staticmethod
    def delete_data(verbose: bool = False):
        if os.path.exists(Rars.DATA):
            os.remove(Rars.DATA)
            if verbose:
                print(f"🧹️Eliminado {Rars.DATA} antiguo")

    # ──────────────────────────────────────────────────
    # ── DELETE_TEXT.  Borrar el archivo donde esta
    # ── el volcado el segmento de codigo
    # ──────────────────────────────────────────────────
    @staticmethod
    def delete_text(verbose: bool = False):
        if os.path.exists(Rars.TEXT):
            os.remove(Rars.TEXT)
            if verbose:
                print(f"🧹️Eliminado {Rars.TEXT} antiguo")

    # ──────────────────────────────────────────────────
    # ── CHECK_MAIN_ASM.  Comprobar si el fichero asm
    # ── principal existe
    # ──────────────────────────────────────────────────
    def check_main_asm(self) -> bool:
        if os.path.exists(self.main_asm):
            print(f"> ✅️ {self.main_asm} existe")
            return True
        else:
            self.print_error(f"{ansi.YELLOW}{self.main_asm}{ansi.LWHITE}"
                             " no encontrado", violation=True)
            self.abort()
            return False

    def check_deps(self) -> bool:
        for fich in self.deps:
            if os.path.exists(fich):
                print(f"> ✅️ {fich} existe")
            else:
                self.print_error(f"{ansi.YELLOW}{fich}{ansi.LWHITE}"
                                 " no encontrado", violation=True)
                self.abort()
                return False
        return True

    # ──────────────────────────────────────────────────
    # ── CHECK_INCLUDE_ASM.  Comprobar si el fichero
    # ── a incluir existe
    # ──────────────────────────────────────────────────
    def check_include_asm(self) -> bool:

        # --- Comprobar si el fichero a incluir existe
        if self.include_asm != "":
            if os.path.exists(self.include_asm):
                print(f"> ✅️ {self.include_asm} existe")
            else:
                self.print_error(f"{ansi.YELLOW}{self.include_asm}"
                                 f"{ansi.LWHITE}"
                                 f" no encontrado", violation=True)
                self.abort()
                return False
        return True

    # ──────────────────────────────────────────────────
    # ── EXEC.  Ejecutar el RARs
    # ──────────────────────────────────────────────────
    def exec(self):

        # -- Obtener la direccion final del segmento de datos
        data_orig = 0x10010000  # -- Direccion inicial seg. datos
        data_end = data_orig + Rars.DATA_SIZE

        # -- Probando fichero fuente
        print(f"> Probando: {self.main_asm}")

        # -- Obtener una cadena con las dependencias
        deps = " ".join(self.deps)

        # -- Comando a ejecutar
        cmd_str = f"java -jar {Rars.NAME} "\
                  f"x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 "\
                  f"x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 "\
                  f"x25 x26 x27 x28 x29 x30 x31 "\
                  f"nc me ic {Rars.MAX_STEPS} "\
                  f"dump 0x10010000-0x{data_end:x} HexText {Rars.DATA} "\
                  f"dump .text HexText {Rars.TEXT} {self.main_asm}"

        # -- Añadir las dependencias
        if deps:
            cmd_str = cmd_str + ' ' + deps

        # -- Convertirlo a lista, colocando cada argumento en un item
        # -- Necesario para ejecutar el comando con subprocess.run()
        cmd = cmd_str.split(" ")

        # -- Mostrar el comando que se ejecuta
        print("> Ejecutando: ", end="")
        print(ansi.CYAN + cmd_str + ansi.DEFAULT)

        # -- Ejecutar el comando!
        resultado = subprocess.run(
            cmd,
            text=True,         # -- Entrada y salida son cadenas de texto
            input=self.input,  # -- Cadena para la entrada estandar
            stdout=subprocess.PIPE,  # -- Salida estandar
            stderr=subprocess.PIPE   # -- Salida de error
        )

        # -- Guardar la salidas estandar y de error
        # --  Salida: mensajes emitidos por el programa ensamblador
        # --  error: Mensajes emitidos por el RARs (informativos o
        # --         de error)
        self.stdout = resultado.stdout
        self.stderr = resultado.stderr

    # ────────────────────────────────────────────────────────────
    # ── CHECK_runtime_error.  Comprobar los errores en tiempo
    # ── de ejecucion al ejecutar el RARs
    # ────────────────────────────────────────────────────────────
    def check_runtime_error(self) -> bool:

        # -- Comprobar si hay runtime error
        patron = r"Error in .*/([^/]+)\sline\s(\d+): "\
                r"Runtime exception at (0x[0-9a-fA-F]+): (.+)"
        resultado = re.search(patron, self.stderr)

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

            # -- Debug
            # error_output_list = Rars.stderr.split("\n")
            # print(ansi.RED + f"{error_output_list[0]}\n" + ansi.DEFAULT)

            # -- Si hay un error de runtime, se aborta
            self.abort()
            return False

        # -- No hay errores de runtime. Prueba ok
        return True

    # ────────────────────────────────────────────────────────────
    # ── CHECK_asm_errors.  Comprobar errores de ensamblado
    # ── DEVUELVE:
    # ──   * true: Hay errores de ensamblado
    # ─   * false: No hay errores de ensamblado (aunque puede haber
    # ──            warnings)
    # ────────────────────────────────────────────────────────────
    def check_asm_errors(self) -> bool:

        # -- Detectar Warnings
        # Patrón de expresión regular:
        # Grupo 1: 'line ' seguido de uno o más dígitos (\d+)
        # Grupo 2: Mensaje de error
        patron = r"Warning in .*/[^/]+\sline\s+(\d+)\s+column\s+\d+:\s+(.*)"

        # Buscar el patrón en la cadena
        coincidencia = re.search(patron, self.stderr)

        if coincidencia:
            print(f"> ⚠️  {ansi.YELLOW}WARNING: {ansi.DEFAULT}"
                  "Problemas con el ensamblado 😱️😱️")
            linea = int(coincidencia.group(1))
            msg = coincidencia.group(2).strip()
            print(f"  🔹️ {ansi.YELLOW}{msg}{ansi.DEFAULT}")
            print(f"  🔹️ {ansi.BLUE}Línea: {linea}{ansi.DEFAULT}")
            self.errors = True

        # -- Detectar errores
        patron = r"Error in .*/[^/]+\sline\s(\d+).+: (.+)"
        resultado = re.search(patron, self.stderr)
        if resultado:
            self.print_error("El programa NO ensambla 😱️😱️")
            linea = resultado.group(1)
            msg = resultado.group(2)
            print(f"  🔹️ {ansi.RED}{msg}{ansi.DEFAULT}")
            print(f"  🔹️ {ansi.BLUE}Línea: {linea}{ansi.DEFAULT}")
            self.errors = True

            # -- Si hay un error de ensamblado, se aborta
            self.abort()
            return False

        # -- No hay errores de ensamblado
        return True

    # ────────────────────────────────────────────────────────────
    # ── CHECK_DATA.  Comprobar si se ha generado el fichero
    # ── con el volcado del segmento de datos
    # ────────────────────────────────────────────────────────────
    def check_data(self):
        # -- Comprobar si se ha generado el fichero con el volcado
        # -- de memoria. Si no se ha generado es porque no se ha declaro
        #  el segmento de datos
        if os.path.exists(Rars.DATA):

            # -- Tiene segmento de datos
            self.has_data = True

            # -- Imprimir mensaje según si se espera o no que tenga
            # -- segmento de datos
            if self.expected_data:
                # -- Se espera que tenga segmento de datos: OK
                print("> ✅️ ", end='')

            else:
                # -- No es obligatorio que tengo segmento de datos
                print("> ☑️  ", end='')

            print("Hay segmento de datos")

        # -- NO HAY Segmento de datos
        # -- No tiene por qué ser un error. Depende de si se ha especificado
        # -- o no en el enunciado
        else:

            # -- El enunciado requiere que HAYA segmento de datos
            if self.expected_data:
                self.print_error("No hay segmento de DATOS", violation=True)
                self.errors = True

            # -- No tiene segmento de datos, y el enunciado NO lo requiere
            else:
                print("> ✅️ NO hay segmento de datos")

    # ────────────────────────────────────────────────────────────
    # ── CHECK_TEXT.  Comprobar si se ha generado el fichero
    # ── con el volcado del segmento de codigo
    # ────────────────────────────────────────────────────────────
    def check_text(self) -> bool:
        # -- Comprobar si se ha generado el fichero con el volcado
        # -- del segmento de codigo. Si no se ha generado es porque
        # -- el programa no tiene la directiva .text
        if os.path.exists(Rars.TEXT):
            print("> ✅️ Hay segmento de código")
            self.has_text = True
            self.ok = True
            return True
        else:
            self.print_error("No hay segmento de CODIGO!", violation=True)
            self.errors = True
            self.ok = False
            self.abort()
            return False

    # ────────────────────────────────────────────────────────────
    # ── READ_VARIABLES. Leer el segmento de datos del fichero
    # ── generado y devolver una lista con ellas
    # ────────────────────────────────────────────────────────────
    def read_variables(self):
        try:
            # -- Leer el fichero con el segmento de datos
            # -- Se lee como una cadena de texto
            with open(Rars.DATA, "r") as data_file:
                data_str = data_file.read()

            # -- Obtener una lista (de texto) con los valores de la
            # -- memoria
            mem_str = data_str.split("\n")

        except FileNotFoundError:
            # -- NO hay segmento de datos
            # -- No se genera error porque ya se ha mostrado previamente
            mem_str = ''

        # -- Meter todas las variables en una lista, convertidos
        # -- a enteros
        variables = []
        for val in mem_str:
            if val != '':
                variables.append(int(val, 16))

        # -- Guardar las variables
        self.variables = variables

        # -- Devolver la lista de variables
        return variables

    # ────────────────────────────────────────────────────────────
    # ── READ_REGS. Leer los registros
    # ────────────────────────────────────────────────────────────
    def read_regs(self):
        return self.regs

    # ──────────────────────────────────────────────────────────────────────
    # ── PROCESS_OUTPUT. Procesar la salida del RARs (NO la del programa)
    # ── A partir de esta salida se determina si la salida se ha realizado
    # ── llamando a exit, el número de ciclos y los registros
    # ──────────────────────────────────────────────────────────────────────
    def process_output(self):

        # -- Obtener la salida de error del RARs
        # -- como una lista. Una linea en cada posicion
        contenido = self.stderr.strip().split("\n")
        # print(contenido)

        # -- Leer los ciclos
        # -- Se encuentran en la linea 2
        try:
            self.ciclos = int(contenido[2])
        except ValueError:
            # -- Si hay error en su lectura,
            # -- ponemos los ciclos a 0
            self.ciclos = 0

        # -- Lectura de los registros
        # -- Los registros empiezan en la linea 3
        regs_str = contenido[3:]

        # -- Recorrer los registros
        for val in regs_str:

            # -- Parsear el registro actual y
            # -- almacenarlo
            try:
                x_str = val.split("\t")[1]
                self.regs.append(int(x_str, 16))
            except IndexError:
                # -- Lo parseado no es un registro
                # -- es un mensaje diferente
                # -- No hacemos nada
                pass

    # ──────────────────────────────────────────────────────────────────────
    # ── PROCESS_CODE. Procesar el segmento de codigo
    # ── Se actualiza el numero de instrucciones
    # ──────────────────────────────────────────────────────────────────────
    def process_code(self):
        # -- Leer el fichero del codigo
        try:
            with open(Rars.TEXT, "r") as code_file:
                contenido = code_file.read()
                code = contenido.strip().split("\n")
                self.instrucciones = len(code)

        except FileNotFoundError:
            # -- No hay segmento de codigo
            # -- No se muestra mensaje de error porque ya se ha
            # -- hecho previamente
            pass

    # ──────────────────────────────────────────────────────────────────────
    # ── CHECK_EXIT. Comprobar la terminacion del programa
    # ── y emitir los mensajes de error correspondientes
    # ──────────────────────────────────────────────────────────────────────
    def check_exit(self):
        # --- Comprobar si el programa no termina de forma controlada
        if "dropping off" in self.stderr:
            self.print_error("No hay EXIT")
            self.errors = True

        # --- Comprobar si el programa termina con normalidad, llamando a EXIT
        if "calling exit" in self.stderr:
            print("> ✅️ Se termina con EXIT")

    # ──────────────────────────────────────────────────────────────────────
    # ── PRINT_SECTION
    # ── Imprimir el comienzo de la sección
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def print_section(title: str):
        print(f"  {ansi.BLUE}──────── {title}{ansi.DEFAULT}")

    # ──────────────────────────────────────────────────────────────────────
    # ── CHECK_VARIABLES. Comprobar si las variables tienen los valores
    # ── correctos
    # ── ENTRADA:
    # ──   * data_ok: Diccionario con las variables y sus valores correctos
    # ──────────────────────────────────────────────────────────────────────
    def check_variables(self, data_ok: dict):

        self.print_section("Comprobando variables")

        i = 0
        for var, value_ok in data_ok.items():

            data = self.variables[i]
            if data == value_ok:
                print(f"> ✅️ {var} = {data} ({hex(data)}) ")
            else:
                print(f"> ❌️ {var}: {hex(data)}."
                      f"Debería ser: {hex(value_ok)}")
                self.errors = True

            i += 1

    # ──────────────────────────────────────────────────────────────────────
    # ── SHOW_CONSOLE_OUTPUT(). Imprimir la salida en la consola
    # ── Función de depuración
    # ──────────────────────────────────────────────────────────────────────
    def show_console_output(self):

        Rars.print_section("Salida en consola")
        if self.stdout:
            print(self.stdout)

    # ──────────────────────────────────────────────────────────────────────
    # ── CHECK_CONSOLE_OUTPUT. Comprobar si la salida de la consola es la
    # ── correcta
    # ── ENTRADA:
    # ──   * posible_outputs: Lista con las posibles salidas esperadas. Si
    # ──       niguna coincide, se considera error. En ese caso la que se
    # ──       imprime como esperada es la primera (que se considera la
    # ──         que debería ser)
    # ──────────────────────────────────────────────────────────────────────
    def check_console_output(self, posible_outputs: list[str],
                             verbose: bool = True) -> bool:

        # -- Si la ejecución se había abortado, no hacer nada
        if not self.ok:
            return False

        if verbose:
            self.print_section("Comprobando salida en consola")

        # -- Eliminar saltos de linea para mostrar en consola
        salida_esperada = posible_outputs[0].replace("\n", "\\n")
        salida_generada = self.stdout.replace("\n", "\\n")

        # -- Comprobar salida del programa
        if self.stdout in posible_outputs:
            if verbose:
                print(f"{ansi.GREEN}{self.stdout}{ansi.DEFAULT}")
                print("> ✅️ ¡Salida exacta!")
            return True
        else:
            self.errors = True
            if verbose:
                print(f'>  {ansi.GREEN}Salida esperada{ansi.DEFAULT}: \n'
                      f'"{salida_esperada}"')
                print(f'>  {ansi.RED}Salida generada{ansi.DEFAULT}: \n'
                      f'"{salida_generada}"')
                print("> ❌️ Salida NO exacta")
            return False

    # ──────────────────────────────────────────────────────
    # ── LOAD_BYTE(off)
    # ──
    # ──  Leer un byte del offset de memoria
    # ──  de datos indicado. Ej. offset 0 = dir 0x10010000
    # ──────────────────────────────────────────────────────
    def load_byte(self, off: int) -> int:

        # -- Obtener direccion de palabra
        dir_word = off >> 2

        # -- Obtener el numero de byte dentro de la palabra
        nbyte = off & 0x3

        # -- Leer la palabra
        word = self.variables[dir_word]

        # -- Obtener el byte
        byte = (word >> (nbyte * 8)) & 0xFF

        # -- Devolver el byte
        return byte

    # ──────────────────────────────────────────────────────
    # ── LOAD_STRING(off)
    # ──
    # ──  Leer una cadena a partir del offset indicado del
    # ──  segmento de datos. Ej. offset 0 = dir 0x10010000
    # ──────────────────────────────────────────────────────
    def load_string(self, offset: int) -> str:
        cad = ""
        while True:
            byte = self.load_byte(offset)
            if byte == 0:
                break
            # print(f"Offset: {offset:x}, Byte: {byte:x}")
            cad = cad + chr(byte)
            offset = offset + 1

        return cad

    # ──────────────────────────────────────────────────────────────────────
    # ── CHECK_STRING()
    # ──
    # ──  ENTRADAS:
    # ──    - offset: Byte donde comienza la cadena en el segmento de datos
    # ──    - cadena_esperada: Valor correcto de la cadena
    # ──    - var_name: Nombre de la variable cadena
    # ──    - only_check: Solo se realiza la comparación, y se devuelve
    # ──      el resultado. Pero no se muestra en la consola
    # ──────────────────────────────────────────────────────────────────────
    def check_string(self,
                     offset,
                     cadena_esperada,
                     var_name="cad",
                     only_check=False) -> bool:

        # -- Leer la cadena
        cad = self.load_string(offset)

        # -- Realizar la comprobacion
        check_result = (cad == cadena_esperada)

        # -- Modo solo comprobacion
        if only_check:
            return check_result

        # -- Eliminar saltos de linea para mostrar en consola
        cadena_esperada = cadena_esperada.replace("\n", "\\n")

        # -- Modo normal: Comprobar y mostrar salida
        if check_result:
            print(f'> ✅️ {var_name}: "{cadena_esperada}" ')
        else:
            print(f'> ❌️ {var_name}: "{cad}"\n'
                  f'     Debería ser: "{cadena_esperada}"')
            self.errors = True

        return check_result

    # ──────────────────────────────────────────────────────────────────────
    # ── ABORT. Abortar la prueba, porque se ha producido un error
    # ── grave
    # ──────────────────────────────────────────────────────────────────────
    def abort(self):
        print("> 💔  Prueba abortada...")
        util.line(ansi.YELLOW, Rars.WIDTH)
        print(ansi.DEFAULT)
        self.ok = False

    # ──────────────────────────────────────────────────────────────────────
    # ── CLOSE_LINE. Imprimir la linea de cierre
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def close_line():
        util.line(ansi.YELLOW, Rars.WIDTH)
        print(ansi.DEFAULT)

    # ──────────────────────────────────────────────────────────────────────
    # ── EXIT. Terminar. Mostrar las instrucciones, ciclos y bonus
    # ──────────────────────────────────────────────────────────────────────
    def exit(self):

        # -- Si la ejecución se había abortado, no hacer nada
        if not self.ok:
            return

        self.print_section("Comprobaciones finales")

        # -- Comprobar como se ha realizado la salida del programa
        self.check_exit()

        # -- Mostrar informacion
        print(f"> Instrucciones totales: {self.instrucciones}")
        print(f"> Ciclos de ejecución: {self.ciclos}")

        # -- Comprobar si se superan los ciclos máximo
        # -- Si es asi, significa que hay un bucle infinito
        if self.ciclos >= Rars.MAX_STEPS:
            self.print_error("Ciclos máximos excedidos. BUCLE INFINITO")

        # -- Comprobar BONUS
        # -- Solo si no hay errores previos
        if not self.errors and self.bonus > 0:
            print("> Comprobando BONUS...")
            ok_bonus = False

            # -- Comprobar los bonus segun el tipo
            if self.tipo_bonus == Rars.BONUS_INSTRUCCIONES:

                # -- Comprobar instrucciones
                if self.instrucciones <= self.bonus:
                    print(f"  > ✅️ Máximo de {self.bonus} instrucciones")
                    ok_bonus = True
                else:
                    print(f"  > ❌️ Más de {self.bonus} instrucciones...")

            if self.tipo_bonus == Rars.BONUS_CICLOS:

                # -- Comprobar ciclos
                if self.ciclos <= self.bonus:
                    print(f"  > ✅️ Máximo de {self.bonus} ciclos")
                    ok_bonus = True
                else:
                    print(f"  > ❌️ Más de {self.bonus} ciclos...")

            # -- Comprobacion final de Bonus
            if ok_bonus:
                print(f"  > 🎖️  {ansi.YELLOW}BONUS CONSEGUIDO!!!"
                      f"{ansi.DEFAULT}")
            else:
                print("  > No conseguidos...")

        self.close_line()
