# Spec — `tool_install`

Fecha de cierre: 2026-08-23 · Estado: cerrado

## Purpose

Cuando una fuente `system_app` falla con `TOOL_NOT_FOUND` (un binario Kali
que no está en el sistema), el operador quiere instalar la tool **desde la
propia GUI**, no desde un terminal. Este módulo instala una tool ausente de
forma segura, con recetas estilo **LazyOwn lazyaddon** (`tool_recipes/*.yaml`),
y con elevación gráfica de privilegios vía `run0` (Estorides es una app GUI;
la gestión de usuarios debe ser gráfica, no una contraseña de `sudo` por
terminal).

## Inputs

- `tool_name` / `binary`: nombre del binario a instalar (de `meta.tool_binary`).
- Receta YAML `tool_recipes/<name>.yaml` con el contrato lazyaddon:
  ```yaml
  name: sherlock
  apt: sherlock                      # opcional: paquete Debian/Kali
  git:                               # opcional: clon + install_command
    repo_url: https://github.com/sherlock-project/sherlock.git
    install_path: sherlock
    install_command: pip install -r requirements.txt
  ```
  Al menos `apt` o `git` debe estar presente.

## Outputs

`InstallResult` (dataclass frozen, JSON-serialisable):
```json
{ "tool_name": "nmap", "success": true, "method": "verify",
  "output": "resolved /usr/bin/nmap", "error": null, "duration_s": 12.3 }
```
- `method` ∈ {`none` (ya instalado), `apt`, `git`, `verify`}.
- Fallos como **valores**, nunca excepciones.

## Métodos de instalación (orden)

1. `apt` — `run0 apt-get update -y` + `run0 apt-get install -y <pkg>`.
2. `git` — clona `repo_url` en `.tools/<install_path>` (como operador, sin
   elevación), luego ejecuta `install_command` shlex-split con `shell=False`
   (elevado solo si hace una instalación a nivel de sistema).
3. `verify` — comprueba `_resolve_binary`; si sigue faltando → error.

## Elevación (regla gráfica)

`_elevate(cmd)`:
- ya root → sin wrapper;
- si existe `run0` → `run0 <cmd>` (prompt polkit de escritorio);
- si no, fallback `sudo`; si no existe ninguno → sin elevación.

## Tabla de errores

| Código | Condición | Mensaje |
| --- | --- | --- |
| `ALREADY_INSTALLED` (method=none, success=True) | binario resuelve | — |
| `not-in-allowlist` (error) | binario fuera de `TOOL_ALLOWLIST` | `tool '<b>' not in allowlist` |
| `no-recipe` (error) | no hay `tool_recipes/<name>.yaml` | `no install recipe found for '<n>'` |
| `install-failed` (error) | apt/git fallaron y el binario sigue ausente | `all install methods failed for '<n>'` |
| `forbidden-command` (ValueError) | `install_command` con tokens hostiles | rechazado antes de ejecutar |

## Garantías de seguridad

- Todo subprocess es **argument-list** (`shell=False`); `install_command` se
  shlex-split — cero inyección de subcomando.
- El binario debe pasar `TOOL_ALLOWLIST`.
- `install_command` se escanea contra tokens hostiles (`;|`, `rm -rf /`, …).
- Output limitado y cada run con timeout.
- `run0` para elevación (gráfico), nunca `sudo` por defecto.
- **Doctrina**: todo input del operador/remoto es hostil.

## Out of scope

- No decide **qué** tools instalar: solo ejecuta recetas existentes.
- No ejecuta código externo arbitrario ni descarga binarios de URLs remotas
  no declaradas en la receta.
- No toca el pipeline de agregación; alimenta solo la reparación de la fuente.

## Escenarios BDD

- **G1 happy**: tool ausente con receta apt → se instala y `verify` la
  encuentra en PATH.
- **G2 edge**: tool ya instalada → `method=none`, sin red ni elevación.
- **G3 error**: sin receta (en allowlist) → `no install recipe`.
- **G4 security**: binario fuera de allowlist → rechazado.
- **G5 security**: `install_command` con token hostil → rechazado sin ejecutar.
- **G6 security**: elevación prefiere `run0` sobre `sudo`; nada si root.
