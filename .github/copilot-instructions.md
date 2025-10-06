# Copilot Instructions for RekDeck

## Project Overview
This is a cross-platform Kivy-based application for creating a streamdeck device using raspberry pi as the main screen, and pc as a controller. The codebase is organized for both raspberry pi app and desktop controller app, with clear separation of UI, logic, and assets.

## Architecture & Key Components
- **Entry Points**: 
  - `main.py`: Main app launcher (likely mobile/touch).
  - `desktop_app/desktop_main.py`: Desktop-specific entry point.
- **UI Layouts**:
  - `.kv` files define Kivy layouts. Example: `desktop_app/desktop_main.kv` for desktop UI.
  - Screens are modular: see `screens/` for WiFi connection, password, and selection screens.
- **Widgets**:
  - Custom widgets (e.g., `virtual_keyboard.py`, `networks_recycle_view.py`) are in `widgets/`.
- **Interaction Managers**:
  - `interaction_managers/network_manager.py` handles network logic and communication.
- **Assets**:
  - Images, GIFs, and other resources are in `assets/`.

## Developer Workflows
- **Run Desktop App**: 
  - `python desktop_app/desktop_main.py`
- **Run Main App**:
  - `python main.py`
- **KV File Hot Reload**: Kivy auto-reloads `.kv` files on app restart.
- **Debugging**: Use print statements or Kivy's logging. No custom debug tooling detected.

## Patterns & Conventions
- **Screen Navigation**: Each screen is a separate Python file + `.kv` file in `screens/`.
- **Widget Reuse**: Custom widgets are defined in `widgets/` and referenced in screens/layouts.
- **Network Logic**: Centralized in `interaction_managers/network_manager.py`.
- **File Naming**: Follows Kivy convention: `screen_name_screen.py`/`.kv`, `widget_name.py`/`.kv`.
- **No build system or tests detected**: Manual running only.

## Integration Points
- **Kivy Framework**: All UI and event handling is via Kivy.
- **No external APIs or cloud services detected**.
- **Assets**: Referenced in `.kv` files and loaded by screens/widgets.

## Examples
- To add a new screen: create `screens/new_screen.py` and `screens/new_screen.kv`, then update navigation logic in the main app file.
- To add a widget: create in `widgets/`, reference in relevant `.kv` files.

## Key Files & Directories
- `main.py`, `desktop_app/desktop_main.py`: App entry points
- `screens/`: All screen logic and layouts
- `widgets/`: Custom reusable widgets
- `interaction_managers/`: Network and other interaction logic
- `assets/`: Images, GIFs, etc.
- `desktop_app/`: Desktop-specific app
---
For questions or missing conventions, ask the user for clarification or examples from their workflow.
