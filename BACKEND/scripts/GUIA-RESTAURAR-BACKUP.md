# Guía Completa: Cómo Restaurar tu Backup de la Base de Datos JOSNISHOP

**Fecha de creación:** 18 de Noviembre 2025  
**Archivo de backup:** `josnishop_20251118_162808.zip`  
**SHA256 del backup (origen):** `D619847341AFF699B162AE9C2827B8D978C7341A034E18069AB4A69D15FED984`  
**Tamaño:** 26 KB (contiene SQL de ~94 KB)

---

## PARTE 1: Preparación en la Máquina Destino

### Paso 1.1 — Verificar que tienes MySQL/MariaDB instalado

**En Windows (PowerShell):**
```powershell
# Verifica que mysql está accesible
Get-Command mysql -ErrorAction SilentlyContinue
# Si sale algo, MySQL está instalado. Si no aparece nada, instálalo.

# Verifica versión
mysql --version
```

**En Linux (terminal):**
```bash
mysql --version
# O si usas MariaDB
mariadb --version
```

Si no aparece instalado, descarga e instala:
- **Windows:** https://dev.mysql.com/downloads/mysql/ o MariaDB desde https://mariadb.org/download/
- **Linux:** `sudo apt-get install mysql-client` (Debian/Ubuntu) o `sudo yum install mysql` (RedHat/CentOS)

### Paso 1.2 — Copiar el ZIP a la máquina destino

**Por USB/Pendrive:**
1. Inserta el pendrive en la máquina destino.
2. Copia el archivo `josnishop_20251118_162808.zip` a una carpeta local (ej. `C:\backups\` en Windows o `~/backups/` en Linux).

**Por red (si ambas máquinas están conectadas):**
```powershell
# Windows PowerShell (desde máquina destino)
Copy-Item '\\NOMBRE_MAQUINA_ORIGEN\backups\josnishop_20251118_162808.zip' -Destination 'C:\backups\'
```

**Por email/Google Drive/Dropbox:**
1. Descarga el archivo desde la nube a una carpeta local (ej. `C:\backups\`).

---

## PARTE 2: Verificación de Integridad (IMPORTANTE — ANTES DE RESTAURAR)

### Paso 2.1 — Calcular SHA256 en la máquina destino

**En Windows (PowerShell):**
```powershell
# Reemplaza la ruta con donde copiaste el archivo
Get-FileHash 'C:\backups\josnishop_20251118_162808.zip' -Algorithm SHA256 | Format-List
```

**Salida esperada:**
```
Algorithm : SHA256
Hash      : D619847341AFF699B162AE9C2827B8D978C7341A034E18069AB4A69D15FED984
Path      : C:\backups\josnishop_20251118_162808.zip
```

**En Linux (terminal):**
```bash
sha256sum ~/backups/josnishop_20251118_162808.zip
```

**Salida esperada:**
```
d619847341aff699b162ae9c2827b8d978c7341a034e18069ab4a69d15fed984  ~/backups/josnishop_20251118_162808.zip
```

### Paso 2.2 — Comparar hashes

- Hash origen: `D619847341AFF699B162AE9C2827B8D978C7341A034E18069AB4A69D15FED984`
- Hash en destino: [pega aquí el que obtuviste en Paso 2.1]

✅ **Si coinciden:** el archivo está íntegro, procede al Paso 3.  
❌ **Si no coinciden:** el archivo se dañó durante la copia. Borra la copia y vuelve a copiar desde el pendrive u otra fuente.

---

## PARTE 3: Restauración en Windows

### Opción A: Usar el script `restore-db.ps1` (RECOMENDADO)

#### Paso 3A.1 — Preparar el script

1. En la máquina destino, coloca el ZIP en `BACKEND\backups\` o en una carpeta conocida.
2. Abre PowerShell y navega a la carpeta `BACKEND`:

```powershell
cd 'C:\ruta\a\tu\proyecto\BACKEND'
# O si ya estás en BACKEND:
cd .
```

#### Paso 3A.2 — Ejecutar el script con bypass

**Opción A1: ZIP en la carpeta `BACKEND\backups\` (automático):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\restore-db.ps1 -User root -Password 'admin' -DbHost localhost -Port 3315 -Database josnishop
```

**Opción A2: ZIP en otra carpeta (especifica la ruta completa):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\restore-db.ps1 -ZipPath 'C:\backups\josnishop_20251118_162808.zip' -User root -Password 'admin' -DbHost localhost -Port 3315 -Database josnishop
```

**Opción A3: Sin pasar la contraseña (el script la pedirá de forma segura):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\restore-db.ps1 -ZipPath 'C:\backups\josnishop_20251118_162808.zip' -User root -DbHost localhost -Port 3315 -Database josnishop
```

#### Salida esperada (si todo va bien):
```
Usando ZIP: C:\backups\josnishop_20251118_162808.zip
Introduce la contraseña de MySQL (oculta):  [escribes 'admin' y presionas Enter]
Extrayendo ZIP a: C:\Users\...\AppData\Local\Temp\restore_xxxxx
Importando SQL: ... -> localhost:3315 / josnishop
Restauración completada correctamente.
```

---

### Opción B: Restauración Manual (si prefieres control total)

#### Paso 3B.1 — Descomprimir el ZIP

```powershell
# En PowerShell, desde donde esté el ZIP
Expand-Archive -Path 'C:\backups\josnishop_20251118_162808.zip' -DestinationPath 'C:\backups\temp_restore' -Force

# Verifica que se extrajo el SQL
Get-ChildItem 'C:\backups\temp_restore' -Filter *.sql
```

Salida esperada:
```
    Directory: C:\backups\temp_restore

Mode                 LastWriteTime         Length Name
----                 -----------           ------ ----
-a----          11/18/2025   4:28 PM       94547 josnishop_20251118_162808.sql
```

#### Paso 3B.2 — Importar el SQL usando `mysql`

```powershell
# Opción B1: con contraseña en línea (cuidado en sistemas multiusuario)
mysql -u root -p'admin' -h localhost -P 3315 josnishop < 'C:\backups\temp_restore\josnishop_20251118_162808.sql'

# Opción B2: sin pasar contraseña (el comando te la pedirá)
mysql -u root -p -h localhost -P 3315 josnishop < 'C:\backups\temp_restore\josnishop_20251118_162808.sql'
# [Se abrirá un prompt pidiendo contraseña, escribe 'admin' y presiona Enter]

# Opción B3: si mysql está en una carpeta no reconocida, usa la ruta completa
'C:\Program Files\MariaDB 12.0\bin\mysql.exe' -u root -p'admin' -h localhost -P 3315 josnishop < 'C:\backups\temp_restore\josnishop_20251118_162808.sql'
```

#### Salida esperada:
- Sin mensaje = éxito (MySQL ejecutó silenciosamente).
- Si ves errores, ve a la sección **TROUBLESHOOTING** más abajo.

#### Paso 3B.3 — Limpieza (opcional)
```powershell
# Eliminar carpeta temporal descomprimida
Remove-Item 'C:\backups\temp_restore' -Recurse -Force
```

---

## PARTE 4: Restauración en Linux/macOS

### Paso 4.1 — Descomprimir el ZIP

```bash
cd ~/backups
unzip josnishop_20251118_162808.zip
# Verifica
ls -la *.sql
```

### Paso 4.2 — Importar el SQL

**Opción 1: con contraseña (ten cuidado, aparece en historial):**
```bash
mysql -u root -p'admin' -h localhost -P 3315 josnishop < josnishop_20251118_162808.sql
```

**Opción 2: sin pasar contraseña (te la pedirá de forma segura):**
```bash
mysql -u root -p -h localhost -P 3315 josnishop < josnishop_20251118_162808.sql
# [Presiona Enter, se abrirá un prompt para la contraseña]
```

**Opción 3: si usas .my.cnf (archivo de credenciales seguro):**
```bash
# Primero crea ~/.my.cnf con permisos restrictivos
cat > ~/.my.cnf << 'EOF'
[client]
user=root
password=admin
host=localhost
port=3315
EOF

chmod 600 ~/.my.cnf

# Luego ejecuta sin credenciales
mysql josnishop < josnishop_20251118_162808.sql
```

---

## PARTE 5: Verificación Post-Restauración

### Paso 5.1 — Conectarse a la BD y revisar tablas

**En Windows o Linux (PowerShell o terminal):**

**Opción 1: Línea de comandos interactiva:**
```bash
mysql -u root -p -h localhost -P 3315 josnishop
# [Escribe contraseña 'admin' y presiona Enter]

# Una vez dentro (deberías ver el prompt mysql>):
USE josnishop;
SHOW TABLES;
SELECT COUNT(*) FROM usuarios;
SELECT COUNT(*) FROM productos;
SELECT COUNT(*) FROM pedidos;
EXIT;
```

**Opción 2: Ejecutar verificación sin entrar en la consola interactiva:**

```bash
# Windows (PowerShell)
mysql -u root -p'admin' -h localhost -P 3315 -e "USE josnishop; SHOW TABLES; SELECT 'Usuarios:', COUNT(*) FROM usuarios; SELECT 'Productos:', COUNT(*) FROM productos; SELECT 'Pedidos:', COUNT(*) FROM pedidos;"

# Linux (terminal)
mysql -u root -p'admin' -h localhost -P 3315 -e "USE josnishop; SHOW TABLES; SELECT 'Usuarios:', COUNT(*) FROM usuarios; SELECT 'Productos:', COUNT(*) FROM productos; SELECT 'Pedidos:', COUNT(*) FROM pedidos;"
```

**Salida esperada:**
```
+---------------------+
| Tables_in_josnishop |
+---------------------+
| categorias          |
| chat_messages       |
| detallepedido       |
| inventario          |
| item                |
| notificaciones      |
| pagos               |
| pedido              |
| productos           |
| resenas             |
| roles               |
| usuarios            |
| videos              |
+---------------------+
Usuarios: 15
Productos: 42
Pedidos: 8
```

✅ **Si ves las tablas y los conteos:** restauración exitosa.  
❌ **Si ves errores o conteos = 0:** ve a la sección **TROUBLESHOOTING**.

---

## PARTE 6: TROUBLESHOOTING (¿Qué hacer si falla?)

### Error: "Access denied for user 'root'@'localhost'"

**Causa:** Contraseña incorrecta o usuario no existe.

**Soluciones:**
1. Verifica que la contraseña sea correcta (en la máquina origen era `admin`).
2. Si olvidaste la contraseña, resetéala (procedimiento varía por OS, busca "reset MySQL root password Windows" o "reset MySQL root password Linux").
3. Verifica el puerto: en tu caso es `3315`, no el default `3306`.

**Comando para verificar que el servidor está corriendo:**
```bash
# Windows
netstat -an | findstr :3315

# Linux
netstat -an | grep :3315
```

Si no muestra nada, el servidor MySQL no está corriendo. Inicia el servicio.

---

### Error: "Can't connect to MySQL server on 'localhost' (10061)"

**Causa:** MySQL/MariaDB no está corriendo o el host/puerto es incorrecto.

**Soluciones:**
1. Verifica que MySQL está corriendo:
   - **Windows:** Services → busca "MySQL" o "MariaDB" → debe estar "Running".
   - **Linux:** `sudo systemctl status mysql` o `sudo systemctl status mariadb`

2. Si no está corriendo, inicia el servicio:
   - **Windows:** `net start MySQL80` (cambia la versión según la tuya)
   - **Linux:** `sudo systemctl start mysql`

3. Verifica el puerto y host:
   - En `BACKEND\db\database.py` está la conexión: `localhost:3315`
   - Usa exactamente esos valores en los comandos de restauración.

---

### Error: "The file ... does not exist" (al descomprimir)

**Causa:** La ruta del ZIP es incorrecta o no existe.

**Soluciones:**
1. Verifica que el archivo existe:
   ```powershell
   # Windows
   Test-Path 'C:\ruta\a\tu\archivo.zip'
   
   # Linux
   ls -la ~/backups/josnishop_20251118_162808.zip
   ```

2. Si no existe, cópialo de nuevo desde el pendrive o descárgalo de la nube.

3. Usa rutas completas y entre comillas si contienen espacios:
   ```powershell
   'C:\Program Files\My Folder\backup.zip'
   ```

---

### Error: "ERROR 1064: Syntax error near ..." (durante la importación)

**Causa:** Incompatibilidad de versión de MySQL o archivo SQL corrupto.

**Soluciones:**
1. Verifica que el SHA256 coincide (Paso 2.2). Si no coincide, vuelve a copiar el archivo.

2. Verifica versión de MySQL en destino vs origen:
   ```bash
   mysql --version
   ```
   Debe ser igual o mayor a la versión origen.

3. Si el error persiste, intenta descomprimir manualmente y revisar el archivo SQL:
   ```powershell
   # Descomprimir
   Expand-Archive -Path 'archivo.zip' -DestinationPath 'temp' -Force
   
   # Ver primeras líneas del SQL
   Get-Content 'temp\*.sql' -TotalCount 20
   ```
   Si ves caracteres raros o el archivo está vacío, es corrupto.

---

### Error: "Script execution is disabled" (en PowerShell)

**Causa:** La política de ejecución sigue bloqueando scripts.

**Soluciones:**
1. Usa el comando con `-ExecutionPolicy Bypass` (ya incluido en los comandos recomendados).

2. Si aún así falla, abre PowerShell como Administrador y ejecuta:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Confirma con `Yes`. Luego intenta de nuevo.

3. Para revertir después:
   ```powershell
   Set-ExecutionPolicy Restricted -Scope CurrentUser
   ```

---

### Error: "File is in use" o "Cannot delete"

**Causa:** Carpeta temporal no se pudo limpiar porque algunos procesos la bloquean.

**Soluciones:**
1. Espera un momento y vuelve a intentar la restauración.

2. Cierra cualquier conexión abierta a la BD:
   ```bash
   mysql -u root -p'admin' -h localhost -P 3315 -e "SHOW PROCESSLIST;"
   ```

3. Limpia manualmente:
   ```powershell
   # Windows
   Remove-Item 'C:\Users\tu_usuario\AppData\Local\Temp\restore_*' -Recurse -Force -ErrorAction SilentlyContinue
   
   # Linux
   rm -rf /tmp/restore_*
   ```

---

### Restauración se completó pero los datos no aparecen

**Causa:** La restauración se ejecutó sobre una BD ya existente; posibles conflictos.

**Soluciones:**
1. Verifica que estás conectado a la BD correcta:
   ```bash
   USE josnishop;
   SHOW DATABASES;
   ```

2. Borra la BD antigua (⚠️ cuidado, perderás datos) y vuelve a restaurar:
   ```bash
   mysql -u root -p'admin' -h localhost -P 3315 -e "DROP DATABASE IF EXISTS josnishop; CREATE DATABASE josnishop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   ```
   Luego repite el paso de restauración.

3. Verifica que no hay errores ocultos en la restauración. Redirige a un archivo de log:
   ```bash
   # Windows
   mysql -u root -p'admin' -h localhost -P 3315 josnishop < 'ruta\al\sql' > 'C:\restore_log.txt' 2>&1
   cat 'C:\restore_log.txt'
   
   # Linux
   mysql -u root -p'admin' -h localhost -P 3315 josnishop < ruta/al/sql > restore_log.txt 2>&1
   cat restore_log.txt
   ```

---

## PARTE 7: Resumen de Pasos Rápido (Cheat Sheet)

```powershell
# === WINDOWS ===
# 1. Verifica integridad
Get-FileHash 'C:\backups\josnishop_20251118_162808.zip' -Algorithm SHA256

# 2. Restaura (opción simple)
powershell -NoProfile -ExecutionPolicy Bypass -File '.\scripts\restore-db.ps1' -ZipPath 'C:\backups\josnishop_20251118_162808.zip' -User root -Password 'admin' -DbHost localhost -Port 3315 -Database josnishop

# 3. Verifica
mysql -u root -p'admin' -h localhost -P 3315 -e "USE josnishop; SHOW TABLES;"
```

```bash
# === LINUX ===
# 1. Verifica integridad
sha256sum ~/backups/josnishop_20251118_162808.zip

# 2. Descomprime
unzip ~/backups/josnishop_20251118_162808.zip

# 3. Restaura
mysql -u root -p'admin' -h localhost -P 3315 josnishop < josnishop_20251118_162808.sql

# 4. Verifica
mysql -u root -p'admin' -h localhost -P 3315 -e "USE josnishop; SHOW TABLES;"
```

---

## PARTE 8: Contacto / Ayuda Adicional

Si encuentras problemas:

1. **Revisa el log de errores de MySQL:**
   - Windows: `C:\ProgramData\MySQL\MySQL Server 8.0\Data\error.log`
   - Linux: `/var/log/mysql/error.log`

2. **Haz una copia de seguridad de la BD antes de restaurar:**
   - Nunca restaures directamente en producción sin backup local.

3. **Documenta cualquier error:** copia el mensaje exacto de error y los pasos que seguiste, facilita el diagnóstico.

---

**Documento creado:** 18 de Noviembre 2025  
**Última actualización:** Hoy  
**Estado:** Listo para usar
