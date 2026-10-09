# Contributing to Tech Stacks Banner Generator

Thank you for your interest in contributing! Whether you are adding a new tech stack icon, introducing a role preset, designing a background theme, or fixing a bug, contributions are welcome.

---

## Development Setup

### Prerequisites

- **Python**: `>= 3.10`
- **[uv](https://github.com/astral-sh/uv)** (recommended package manager)
- **librsvg** (required for PNG rasterization):
  - macOS: `brew install librsvg`
  - Linux (Ubuntu/Debian): `sudo apt-get install -y librsvg2-bin`

### Initializing the Project

```bash
# Clone the repository
git clone https://github.com/bernardbdas/banners.git
cd banners

# Install dependencies into virtual environment
uv sync --all-groups

# Install pre-commit hooks
uv run pre-commit install
```

---

## Development Workflow

We use [`just`](https://github.com/casey/just) to manage common development tasks:

```bash
# Run the complete test suite and verification checks
just check

# Run unit tests only
just test

# Format code with ruff
just format

# Check formatting with ruff
just format-check

# Run linter with ruff
just lint
```

Make sure `just check` passes before opening a pull request.

---

## Adding Content

### 1. Adding a New Tech Stack Icon

1. Place the SVG icon in the appropriate category under `assets/icons/`:
   - `assets/icons/backend/`
   - `assets/icons/frontend/`
   - `assets/icons/ai-ml/`
   - `assets/icons/cloud-devops/`
   - `assets/icons/databases/`
   - `assets/icons/messaging/`
   - `assets/icons/mobile/`
2. Ensure the icon SVG is clean, uses a standard `viewBox`, and has no external dependencies.
3. List your icon in relevant presets in `banners/presets.py`.
4. Run `just test` to verify that `test_all_preset_icons_exist_on_disk` passes.

### 2. Adding or Modifying a Role Preset

1. Open `banners/presets.py`.
2. Add a new dictionary entry under `PRESETS`:
   ```python
   "my_role": {
       "title": "Title to Display",
       "subtitle": "Subtitle or specializations",
       "icons": [
           ("Label", "assets/icons/<category>/<icon>.svg"),
           # ...
       ],
   },
   ```
3. Run `just test` to verify structure and icon existence.

### 3. Adding a Custom Background or Theme

- **Background SVGs**: Place in `assets/backgrounds/patterns/`, `assets/backgrounds/gradients/`, or `assets/backgrounds/solids/`.
- **Built-in Themes**: Define styling tokens in `banners/themes.py` under `THEMES` (background gradients, card surface stops, stroke colors, typography colors, etc.).

---

## Pull Request Guidelines

1. **Create a topic branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. **Ensure tests and linters pass**:
   ```bash
   just check
   ```
3. **Commit your changes**:
   Write clear, concise commit messages.
4. **Push and open a PR**:
   Describe the motivation behind your changes and include generated banner samples if visual elements were changed.
