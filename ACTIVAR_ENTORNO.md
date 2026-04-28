# 🔧 Activar Entorno Virtual

## ¿Qué es un entorno virtual?

Un entorno virtual es un espacio aislado donde se instalan las dependencias del proyecto sin afectar tu instalación global de Python. Esto evita conflictos entre proyectos.

---

## 🚀 Cómo Activar el Entorno Virtual

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## ✅ Verificar que está Activado

Cuando el entorno virtual está activado, verás `(.venv)` al inicio de tu línea de comandos:

```
(.venv) PS C:\...\solar_leads_system>
```

---

## 🎯 Uso Diario

### Cada vez que trabajes en el proyecto:

1. **Abrir terminal** en la carpeta del proyecto

2. **Activar entorno virtual**:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. **Trabajar normalmente**:
   ```powershell
   # Iniciar aplicación
   streamlit run app.py
   
   # O enviar WhatsApp
   python messenger.py
   
   # O verificar sistema
   python verificar_sistema.py
   ```

4. **Desactivar cuando termines** (opcional):
   ```powershell
   deactivate
   ```

---

## 🔄 Si Cierras la Terminal

Cada vez que cierres y vuelvas a abrir la terminal, necesitas **reactivar** el entorno virtual:

```powershell
# Navegar a la carpeta del proyecto
cd C:\Users\proyectos.lean\Desktop\Codigos.py\solar_leads_system

# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Ahora puedes usar la aplicación
streamlit run app.py
```

---

## ❌ Error: "No se puede cargar el archivo"

Si ves este error en PowerShell:

```
.venv\Scripts\Activate.ps1 : No se puede cargar el archivo...
porque la ejecución de scripts está deshabilitada en este sistema.
```

**Solución**:

1. Abrir PowerShell **como Administrador**

2. Ejecutar:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Confirmar con `S` (Sí)

4. Cerrar PowerShell de administrador

5. Abrir PowerShell normal y activar entorno:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

---

## 🆘 Alternativa: Usar CMD en lugar de PowerShell

Si PowerShell da problemas, usa CMD:

1. Abrir **CMD** (no PowerShell)

2. Navegar al proyecto:
   ```cmd
   cd C:\Users\proyectos.lean\Desktop\Codigos.py\solar_leads_system
   ```

3. Activar entorno:
   ```cmd
   .venv\Scripts\activate.bat
   ```

4. Usar normalmente:
   ```cmd
   streamlit run app.py
   ```

---

## 📝 Script de Inicio Rápido

Para facilitar el inicio, puedes crear un archivo `iniciar.bat`:

```batch
@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run app.py
```

Luego solo haz doble clic en `iniciar.bat` para iniciar la aplicación.

---

## 🔍 Verificar Instalación

Con el entorno activado, verifica que todo esté bien:

```powershell
# Ver paquetes instalados
pip list

# Verificar sistema completo
python verificar_sistema.py

# Probar aplicación
streamlit run app.py
```

---

## 💡 Tips

### ✅ Siempre activa el entorno antes de trabajar
```powershell
.venv\Scripts\Activate.ps1
```

### ✅ Verifica que esté activado
Busca `(.venv)` al inicio de la línea

### ✅ Si instalas nuevas dependencias
```powershell
pip install nombre-paquete
pip freeze > requirements.txt  # Actualizar requirements
```

### ✅ Si algo no funciona
```powershell
# Desactivar
deactivate

# Reactivar
.venv\Scripts\Activate.ps1

# Verificar
python verificar_sistema.py
```

---

## 🎓 Comandos Útiles

```powershell
# Activar entorno
.venv\Scripts\Activate.ps1

# Desactivar entorno
deactivate

# Ver paquetes instalados
pip list

# Actualizar paquete
pip install --upgrade nombre-paquete

# Reinstalar todas las dependencias
pip install -r requirements.txt

# Verificar sistema
python verificar_sistema.py

# Iniciar aplicación
streamlit run app.py
```

---

## 🚨 Problemas Comunes

### "python: command not found"
**Solución**: Usa `python` o `py` según tu instalación

### "pip: command not found"
**Solución**: Usa `python -m pip` en lugar de `pip`

### "streamlit: command not found"
**Solución**: 
1. Verifica que el entorno esté activado `(.venv)`
2. Reinstala: `pip install streamlit`

### Entorno no se activa
**Solución**:
1. Verifica que `.venv` exista
2. Si no existe, créalo: `python -m venv .venv`
3. Instala dependencias: `pip install -r requirements.txt`

---

## 📚 Más Información

- **Documentación oficial**: https://docs.python.org/es/3/library/venv.html
- **Guía completa del proyecto**: Ver `README.md`
- **Solución de problemas**: Ver `TROUBLESHOOTING.md`

---

**CySlean Lead Solar** | Guía de Entorno Virtual | 2024
