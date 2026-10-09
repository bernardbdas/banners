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

# Generate all LinkedIn banners (both dark and light modes, SVG and PNG)
all:
    python3 -m banners all all all

# Generate all Dark mode banners (SVG & PNG)
dark:
    python3 -m banners all dark all

# Generate all Light mode banners (SVG & PNG)
light:
    python3 -m banners all light all

# Generate all SVG banners (dark & light)
svg:
    python3 -m banners all all svg

# Generate all PNG banners (dark & light)
png:
    python3 -m banners all all png

# Generate Backend & Distributed Systems banners (dark & light)
backend:
    python3 -m banners backend all all

# Generate Full-Stack Software Engineer banners (dark & light)
fullstack:
    python3 -m banners fullstack all all

# Generate AI & Machine Learning Engineer banners (dark & light)
ai-ml:
    python3 -m banners ai_ml all all

# Generate Cloud & DevOps / SRE banners (dark & light)
devops:
    python3 -m banners devops all all

# Generate Mobile Software Engineer banners (dark & light)
mobile:
    python3 -m banners mobile all all

# Generate Data Analyst banners (dark & light)
data-analyst:
    python3 -m banners data_analyst all all

# Generate Data Scientist banners (dark & light)
data-scientist:
    python3 -m banners data_scientist all all

# Generate Data Engineer banners (dark & light)
data-engineer:
    python3 -m banners data_engineer all all

# Generate AI Engineer banners (dark & light)
ai-engineer:
    python3 -m banners ai_engineer all all

# Generate Machine Learning Engineer banners (dark & light)
ml-engineer:
    python3 -m banners ml_engineer all all

# Generate MLOps Engineer banners (dark & light)
mlops-engineer:
    python3 -m banners mlops_engineer all all

# Generate all 6 specialized Data & AI/ML role banners (dark & light)
roles:
    python3 -m banners data_analyst all all
    python3 -m banners data_scientist all all
    python3 -m banners data_engineer all all
    python3 -m banners ai_engineer all all
    python3 -m banners ml_engineer all all
    python3 -m banners mlops_engineer all all

# Remove all generated banner files
clean:
    rm -rf exported/svg exported/png exported/dark exported/light banner_*.svg
    @echo "Cleaned generated banner assets in exported/."

# List all icons by category and total counts
list-icons:
    @python3 -c "import os; dirs = ['backend', 'frontend', 'ai-ml', 'cloud-devops', 'databases', 'messaging', 'mobile'];\
    print('Tech Stack Icons (in assets/):');\
    [print(f'  {d:<15} : {len(os.listdir(os.path.join(\"assets\", d)))} icons') for d in dirs if os.path.exists(os.path.join('assets', d))];\
    print(f'Total icons: {sum(len(os.listdir(os.path.join(\"assets\", d))) for d in dirs if os.path.exists(os.path.join(\"assets\", d)))}')"
