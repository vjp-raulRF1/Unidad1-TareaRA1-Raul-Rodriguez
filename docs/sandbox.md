# Prueba de la aplicación de notas en sandbox con Firejail y venv

## Objetivo

En este documento se describe cómo se ha ejecutado la aplicación de **notas** escrita en Python dentro de un entorno controlado (sandbox) usando **Firejail** y un entorno virtual de Python (`venv`).
---

## Paso 1. Preparar el proyecto fuera del sandbox

Antes de crear el sandbox se deja preparado el código de la aplicación en un directorio que luego se usará como “home” privado dentro de Firejail.

1. Clonar el repositorio de la asignatura (si no se tenía ya):

   ```
   cd PPS/Unidad1
   git clone https://github.com/jmmedinac03vjp/PuestaProduccionSegura.git
   ```

2. Crear un directorio que se usará como `$HOME` privado del sandbox y copiar dentro el proyecto de la actividad:

   ```
   mkdir -p ~/firejail-home
   cp -r ~/PPS/Unidad1/PPSUnidad1-ActividadSandboxingRRF ~/firejail-home/
   ```

De este modo, el directorio `PPSUnidad1-ActividadSandboxingRRF` quedará accesible dentro del sandbox cuando se lance Firejail con la opción `--private=~/firejail-home`.

---

## Paso 2. Crear y entrar en el sandbox con Firejail

En este paso se crea el entorno aislado usando Firejail, de forma que el “home” visible dentro del sandbox sea únicamente el contenido de `~/firejail-home`.

1. Lanzar Firejail indicando que use `~/firejail-home` como directorio home privado:

   ```
   firejail --private=~/firejail-home bash
   ```

   - `--private=directorio` hace que Firejail monte ese directorio como `$HOME` del usuario dentro del sandbox.  
   - Esto limita la vista del sistema de archivos a lo que haya dentro de ese directorio, aumentando el aislamiento de la aplicación. [web:28][web:26]

2. Verificar que estamos dentro del sandbox y que el proyecto es accesible:

   ```
   pwd
   ls
   ```

   En el listado (`ls`) debe aparecer la carpeta `PPSUnidad1-ActividadSandboxingRRF`, lo que confirma que el proyecto está disponible en el entorno aislado.

3. Entrar a la carpeta de la aplicación de notas desde dentro del sandbox:

   ```
   cd ~/PPSUnidad1-ActividadSandboxingRRF/notas/
   ls
   ```

   Aquí se debe ver el fichero `requirements.txt`, el script principal de la aplicación de notas está en src/notas
---

## Paso 3. Crear el entorno virtual de Python dentro del sandbox

Para evitar que las dependencias de la aplicación afecten al sistema global, se crea un entorno virtual (`venv`) dentro del propio sandbox.

1. Crear el entorno virtual llamado `sandbox`:

   ```
   python3 -m venv sandbox
   ```

   Este comando genera una carpeta `sandbox` que contiene una instalación aislada de Python y `pip`, independiente del Python del sistema.

2. Activar el entorno virtual:

   ```
   source sandbox/bin/activate
   ```

   Al activar el entorno virtual, el prompt del terminal suele cambiar (por ejemplo, apareciendo `(sandbox)` al inicio), indicando que cualquier paquete que se instale con `pip` se guardará en este entorno y no en el resto del sistema.

3. Comprobar la versión de Python en el entorno virtual:

   ```
   python --version
   ```

   Este paso ayuda a documentar que la aplicación se está ejecutando con el intérprete de Python dentro del venv, en el entorno controlado.

---

## Paso 4. Instalar las dependencias desde requirements.txt

Con el entorno virtual activo, se instalan las dependencias de la aplicación utilizando el fichero `requirements.txt` que se copió previamente.

1. Instalar paquetes con `pip` usando el fichero de requisitos:

   ```
   pip install -r requirements.txt
   ```

   Al haberse copiado el proyecto a `~/firejail-home`, el fichero `requirements.txt` es accesible desde dentro del sandbox, por lo que `pip` puede leerlo y descargar las dependencias dentro del entorno virtual `sandbox`.

---

## Paso 5. Ejecutar la aplicación de notas dentro del sandbox

Una vez que el entorno virtual está configurado y las dependencias instaladas, se ejecuta la aplicación de notas.

1. Con el entorno virtual aún activo, ejecutar la aplicación (sustituir por el nombre real del script principal):

   ```
   python src/notas/main.py
   ```

2. Interactuar con la aplicación desde el terminal:
   - Crear nuevas notas.
   - Listar notas.
   - Guardar cambios, etc.

   Todo esto ocurre dentro de:
   - Un sandbox de Firejail que restringe el acceso al sistema de archivos y a otros recursos del sistema.
   - Un entorno virtual de Python que aísla las dependencias de la aplicación.

---

## Paso 6. Salir del entorno controlado

Cuando se termina la prueba de la aplicación, se cierra la sesión del sandbox.

1. Salir de la shell de Firejail:

   ```
   exit
   ```

   Al ejecutar `exit`, se cierra el proceso `bash` que estaba dentro de Firejail, finalizando el sandbox. El directorio `~/firejail-home` sigue existiendo en el sistema anfitrión, por lo que puede reutilizarse en futuras ejecuciones o borrarse si ya no es necesario.

---

## Capturas

![Creando el firejail](image-1.png)

![Verificacion de estar dentro del sandbox](image-3.png)

![Ejecucion del codigo](image.png)