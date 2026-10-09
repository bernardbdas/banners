# Justfile for Tech Stacks Banner Generator

# Default recipe: display available commands
default:
    @just --list

# Run unit tests
test:
    python3 -m unittest discover -s tests -v

# Check linting with ruff
lint:
    uv run ruff check .

# Format code with ruff
format:
    uv run ruff format .

# Check formatting with ruff
format-check:
    uv run ruff format --check .

# Run all verification checks (lint, format, tests, CLI check)
check: lint format-check test
    @python3 -m banners --help > /dev/null
    @echo "All verification checks passed."

# Generate banners for all roles (uses configured theme from local.env or optional theme argument)
all theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners all {{theme}} all; else python3 -m banners all; fi

# Generate all banners for a specific theme (e.g. just theme topographical png)
theme name format="all":
    python3 -m banners all {{name}} {{format}}

# Theme shortcuts:
topographical format="all":
    python3 -m banners all topographical {{format}}

topographical-light format="all":
    python3 -m banners all topographical_light {{format}}

topographical-dense format="all":
    python3 -m banners all topographical_dense {{format}}

topographical-pastel format="all":
    python3 -m banners all topographical_pastel {{format}}

topographical-crimson format="all":
    python3 -m banners all topographical_crimson {{format}}

topographical-crimson-light format="all":
    python3 -m banners all topographical_crimson_light {{format}}

topographical-cyber format="all":
    python3 -m banners all topographical_cyber {{format}}

topographical-vintage format="all":
    python3 -m banners all topographical_vintage {{format}}

dark format="all":
    python3 -m banners all dark {{format}}

light format="all":
    python3 -m banners all light {{format}}

pastel format="all":
    python3 -m banners all pastel_aurora {{format}}

linkedin format="all":
    python3 -m banners all linkedin {{format}}

network-nodes format="all":
    python3 -m banners all network_nodes {{format}}

tortoiseshell format="all":
    python3 -m banners all tortoiseshell {{format}}

leopard format="all":
    python3 -m banners all leopard {{format}}

tiger format="all":
    python3 -m banners all tiger {{format}}

# Generate all SVG banners (for configured theme or optional theme argument)
svg theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners all {{theme}} svg; else python3 -m banners all all svg; fi

# Generate all PNG banners (for configured theme or optional theme argument)
png theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners all {{theme}} png; else python3 -m banners all all png; fi

# Role shortcuts (uses theme from local.env or optional theme argument):
backend theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners backend {{theme}} all; else python3 -m banners backend; fi

fullstack theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners fullstack {{theme}} all; else python3 -m banners fullstack; fi

ai-ml theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners ai_ml {{theme}} all; else python3 -m banners ai_ml; fi

devops theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners devops {{theme}} all; else python3 -m banners devops; fi

mobile theme="":
    @if [ -n "{{theme}}" ]; then python3 -m banners mobile {{theme}} all; else python3 -m banners mobile; fi

# Generate custom banner (configured via local.env or flags):
custom theme="" format="all":
    @if [ -n "{{theme}}" ]; then python3 -m banners custom {{theme}} {{format}}; else python3 -m banners custom; fi


# Generate all 6 specialized Data & AI/ML role banners:
roles theme="":
    @if [ -n "{{theme}}" ]; then \
        python3 -m banners data_analyst {{theme}} all && \
        python3 -m banners data_scientist {{theme}} all && \
        python3 -m banners data_engineer {{theme}} all && \
        python3 -m banners ai_engineer {{theme}} all && \
        python3 -m banners ml_engineer {{theme}} all && \
        python3 -m banners mlops_engineer {{theme}} all; \
    else \
        python3 -m banners data_analyst && \
        python3 -m banners data_scientist && \
        python3 -m banners data_engineer && \
        python3 -m banners ai_engineer && \
        python3 -m banners ml_engineer && \
        python3 -m banners mlops_engineer; \
    fi

# Clean exported/ directory completely
clean-exported:
    rm -rf exported/*
    @echo "Cleaned exported/ directory."

# Remove all generated banner files in exported/
clean: clean-exported

# Clean exported/ and regenerate banners directly using the banners CLI (accepts any CLI flags)
recreate *args: clean-exported
    python3 -m banners {{args}}

# Clean exported/ and regenerate all banners across all presets and themes
recreate-all: clean-exported
    python3 -m banners all all all

# Run the banners CLI directly with any arguments (e.g. just generate backend topographical png)
generate *args:
    python3 -m banners {{args}}

# List all available themes
list-themes:
    @python3 -c "from banners.themes import get_available_themes; print('Available Themes (exported to exported/<theme>/):'); [print(f'  - {t}') for t in get_available_themes()]"

# List all icons by category and total counts
list-icons:
    @python3 -c "import os; dirs = ['backend', 'frontend', 'ai-ml', 'cloud-devops', 'databases', 'messaging', 'mobile']; print('Tech Stack Icons (in assets/icons/):'); [print(f'  {d:<15} : {len(os.listdir(os.path.join(\"assets\", \"icons\", d)))} icons') for d in dirs if os.path.exists(os.path.join('assets', 'icons', d))]; print(f'Total icons: {sum(len(os.listdir(os.path.join(\"assets\", \"icons\", d))) for d in dirs if os.path.exists(os.path.join(\"assets\", \"icons\", d)))}')"
