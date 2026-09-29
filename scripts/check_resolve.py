#!/usr/bin/env python3
"""Verifica que la API de scripting de DaVinci Resolve Studio sea accesible.

Uso (con Resolve Studio abierto y "External scripting using" = Local):
    python scripts/check_resolve.py
"""
import os
import platform
import sys

DEFAULT_PATHS = {
    "Darwin": (
        "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting",
        "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",
    ),
    "Windows": (
        os.path.join(os.environ.get("PROGRAMDATA", r"C:\ProgramData"),
                     "Blackmagic Design", "DaVinci Resolve", "Support", "Developer", "Scripting"),
        r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll",
    ),
    "Linux": (
        "/opt/resolve/Developer/Scripting",
        "/opt/resolve/libs/Fusion/fusionscript.so",
    ),
}


def main() -> int:
    system = platform.system()
    if system not in DEFAULT_PATHS:
        print(f"Sistema no soportado: {system}")
        return 1

    api_default, lib_default = DEFAULT_PATHS[system]
    api = os.environ.setdefault("RESOLVE_SCRIPT_API", api_default)
    lib = os.environ.setdefault("RESOLVE_SCRIPT_LIB", lib_default)
    modules = os.path.join(api, "Modules")

    print(f"Python:             {sys.version.split()[0]}")
    print(f"RESOLVE_SCRIPT_API: {api} {'[OK]' if os.path.isdir(api) else '[NO EXISTE]'}")
    print(f"RESOLVE_SCRIPT_LIB: {lib} {'[OK]' if os.path.isfile(lib) else '[NO EXISTE]'}")

    if sys.version_info < (3, 10):
        print("ERROR: se requiere Python 3.10+ (recomendado 3.10-3.12).")
        return 1

    sys.path.append(modules)
    try:
        import DaVinciResolveScript as dvr  # noqa: N813
    except ImportError as exc:
        print(f"ERROR: no se pudo importar DaVinciResolveScript desde {modules}: {exc}")
        return 1

    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        print("ERROR: Resolve no respondió. Revisa que:")
        print("  1. DaVinci Resolve STUDIO esté abierto (la versión gratuita bloquea el scripting externo).")
        print("  2. Preferencias > General > 'External scripting using' = Local.")
        print("  3. Tu Python sea 3.10-3.12 si usas una build antigua de Resolve.")
        return 1

    print(f"Conectado a: {resolve.GetProductName()} {resolve.GetVersionString()}")
    project = resolve.GetProjectManager().GetCurrentProject()
    print(f"Proyecto actual: {project.GetName() if project else '(ninguno abierto)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
