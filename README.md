# MCP para DaVinci Resolve Studio 21

Configuración para controlar **DaVinci Resolve Studio 21** desde Claude (Claude Code o Claude Desktop) mediante el protocolo MCP, usando el servidor open-source [`samuelgursky/davinci-resolve-mcp`](https://github.com/samuelgursky/davinci-resolve-mcp) (MIT, API oficial de scripting de Resolve).

> El MCP corre **en tu computadora**, junto a Resolve. No funciona desde un servidor en la nube porque necesita comunicarse con la aplicación abierta.

## Contenido

| Archivo | Uso |
| --- | --- |
| `.mcp.json` | Configuración de proyecto para **Claude Code** (se carga al abrir esta carpeta). |
| `config/claude_desktop_config.*.json` | Plantillas para **Claude Desktop** en macOS, Windows y Linux. |
| `scripts/check_resolve.py` | Prueba la conexión con Resolve antes de usar el MCP. |

## 1. Requisitos

- **DaVinci Resolve Studio 21** (la versión gratuita bloquea el scripting externo).
- **Python 3.10 – 3.12** (recomendado; 3.13+ puede funcionar pero da más problemas).
- **Node.js 18+** (solo para el instalador `npx`).
- Opcional: **ffmpeg** en el PATH (detección de silencios, niveles de audio).

## 2. Preparar Resolve

1. Abre DaVinci Resolve Studio 21.
2. Si existe, pon **DaVinci Resolve ▸ Preferences ▸ System ▸ General ▸ External scripting using** en **Local** y reinicia Resolve.
   - En **Resolve Studio 21.1** esta opción ya no aparece en Preferencias y el scripting externo funciona sin configurarla (verificado en 21.1.0.17, macOS).
3. Abre un proyecto.

## 3. Instalar el servidor MCP

Con Resolve abierto:

```bash
npx davinci-resolve-mcp setup
```

El instalador crea un entorno virtual, detecta las rutas de Resolve y puede configurar automáticamente Claude Code, Claude Desktop, Cursor, VS Code, etc. Para revisar el entorno sin escribir nada:

```bash
npx davinci-resolve-mcp doctor
```

## 4. Verificar la conexión

```bash
python scripts/check_resolve.py
```

Salida esperada:

```
Conectado a: DaVinci Resolve Studio 21.x.x
Proyecto actual: Mi Proyecto
```

## 5. Conectar el cliente

### Claude Code

Este repo ya incluye `.mcp.json`. Abre Claude Code en esta carpeta y acepta el servidor `davinci-resolve` cuando lo pida. Verifica con:

```bash
claude mcp list
```

Alternativa (global, para todos tus proyectos):

```bash
claude mcp add davinci-resolve --scope user -- npx -y davinci-resolve-mcp server
```

### Claude Desktop

1. Copia la plantilla de tu sistema desde `config/`.
2. Reemplaza `/RUTA/A/davinci-resolve-mcp` por la ruta de la instalación (la muestra `npx davinci-resolve-mcp doctor`).
3. Pégala en el archivo de configuración:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json` — si Claude Desktop se instaló como MSIX, usa `%LOCALAPPDATA%\Packages\Claude_<hash>\LocalCache\Roaming\Claude\claude_desktop_config.json`
4. Reinicia Claude Desktop.

Rutas de la API de Resolve por sistema:

| Sistema | `RESOLVE_SCRIPT_API` | `RESOLVE_SCRIPT_LIB` |
| --- | --- | --- |
| macOS | `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting` | `/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so` |
| Windows | `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting` | `C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll` |
| Linux | `/opt/resolve/Developer/Scripting` | `/opt/resolve/libs/Fusion/fusionscript.so` |

## 6. Ejemplos de uso

```
"Lista mis proyectos y abre 'Documental 2026'"
"Crea una línea de tiempo 'Assembly Cut' con todos los clips del bin actual"
"Agrega marcadores rojos en cada cambio de plano de la línea de tiempo"
"Revisa la línea de tiempo buscando huecos, solapamientos y media offline"
"Prepara un render ProRes 422 HQ a 3840x2160 y ponlo en cola"
"Exporta un reporte de marcadores de revisión para el cliente"
```

## Solución de problemas

| Síntoma | Solución |
| --- | --- |
| `scriptapp("Resolve")` devuelve `None` | Resolve no está abierto, no es Studio, o *External scripting* no está en **Local**. |
| El instalador dice *"Running, but the scripting bridge returned no connection"* | Puede ser una falsa alarma: prueba la conexión con `scripts/check_resolve.py` antes de cambiar de Python. Python 3.13 funciona con Resolve Studio 21.1. |
| Falla con Python 3.13/3.14 | Instala Python 3.12 y define `DAVINCI_RESOLVE_MCP_PYTHON=/ruta/a/python3.12`. |
| El servidor no aparece en Claude Desktop (Windows) | Revisa la ruta MSIX indicada arriba. |
| Error de `PYTHONPATH` / módulo no encontrado | Verifica las rutas de la tabla; en Windows el instalador añade `PYTHONHOME` automáticamente. |

## Seguridad

- Mantén el scripting en modo **Local**; el modo **Network** permite control remoto de Resolve.
- Haz respaldo del proyecto (**File ▸ Export Project**) antes de pedir ediciones masivas.
