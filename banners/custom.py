"""
Custom Banner Specification, Standards Enforcement, and Icon Resolution.
Provides fine-grained banner customization with strict design standards:
- Single-row guardrail: 3 to 8 icons maximum (safe-zone alignment)
- Title length constraint: 3 to 45 characters
- Subtitle length constraint: 3 to 70 characters
- Smart icon resolution across 75+ curated tech icons with developer aliases
"""

import difflib
from typing import Any

from banners.constants import REPO_ROOT

# Design Standards & Guardrails
MIN_ICONS: int = 3
MAX_ICONS: int = 8
MIN_TITLE_LENGTH: int = 3
MAX_TITLE_LENGTH: int = 45
MIN_SUBTITLE_LENGTH: int = 3
MAX_SUBTITLE_LENGTH: int = 80

# Canonical 75 tech icons: stem -> (display_label, relative_path)
CANONICAL_ICONS: dict[str, tuple[str, str]] = {
    # AI & ML
    "airflow": ("Airflow", "assets/icons/ai-ml/airflow.svg"),
    "apachespark": ("Apache Spark", "assets/icons/ai-ml/apachespark.svg"),
    "huggingface": ("Hugging Face", "assets/icons/ai-ml/huggingface.svg"),
    "jax": ("JAX", "assets/icons/ai-ml/jax.svg"),
    "langchain": ("LangChain", "assets/icons/ai-ml/langchain.svg"),
    "langgraph": ("LangGraph", "assets/icons/ai-ml/langgraph.svg"),
    "langsmith": ("LangSmith", "assets/icons/ai-ml/langsmith.svg"),
    "mlflow": ("MLflow", "assets/icons/ai-ml/mlflow.svg"),
    "numpy": ("NumPy", "assets/icons/ai-ml/numpy.svg"),
    "nvidia": ("NVIDIA", "assets/icons/ai-ml/nvidia.svg"),
    "ollama": ("Ollama", "assets/icons/ai-ml/ollama.svg"),
    "openai": ("OpenAI", "assets/icons/ai-ml/openai.svg"),
    "pandas": ("Pandas", "assets/icons/ai-ml/pandas.svg"),
    "powerbi": ("Power BI", "assets/icons/ai-ml/powerbi.svg"),
    "pytorch": ("PyTorch", "assets/icons/ai-ml/pytorch.svg"),
    "r": ("R", "assets/icons/ai-ml/r.svg"),
    "scikitlearn": ("Scikit-Learn", "assets/icons/ai-ml/scikitlearn.svg"),
    "tableau": ("Tableau", "assets/icons/ai-ml/tableau.svg"),
    "tensorflow": ("TensorFlow", "assets/icons/ai-ml/tensorflow.svg"),
    "wandb": ("Weights & Biases", "assets/icons/ai-ml/wandb.svg"),
    # Backend
    "cplusplus": ("C++", "assets/icons/backend/cplusplus.svg"),
    "express": ("Express", "assets/icons/backend/express.svg"),
    "fastapi": ("FastAPI", "assets/icons/backend/fastapi.svg"),
    "flask": ("Flask", "assets/icons/backend/flask.svg"),
    "golang": ("Go", "assets/icons/backend/golang.svg"),
    "grpc": ("gRPC", "assets/icons/backend/grpc.svg"),
    "java": ("Java", "assets/icons/backend/java.svg"),
    "nodejs": ("Node.js", "assets/icons/backend/nodejs.svg"),
    "python": ("Python", "assets/icons/backend/python.svg"),
    "rust": ("Rust", "assets/icons/backend/rust.svg"),
    "spring": ("Spring", "assets/icons/backend/spring.svg"),
    # Cloud & DevOps
    "argocd": ("ArgoCD", "assets/icons/cloud-devops/argocd.svg"),
    "aws": ("AWS", "assets/icons/cloud-devops/aws.svg"),
    "azure": ("Azure", "assets/icons/cloud-devops/azure.svg"),
    "datadog": ("Datadog", "assets/icons/cloud-devops/datadog.svg"),
    "docker": ("Docker", "assets/icons/cloud-devops/docker.svg"),
    "githubactions": ("GitHub Actions", "assets/icons/cloud-devops/githubactions.svg"),
    "googlecloud": ("Google Cloud", "assets/icons/cloud-devops/googlecloud.svg"),
    "grafana": ("Grafana", "assets/icons/cloud-devops/grafana.svg"),
    "kubernetes": ("Kubernetes", "assets/icons/cloud-devops/kubernetes.svg"),
    "linux": ("Linux", "assets/icons/cloud-devops/linux.svg"),
    "prometheus": ("Prometheus", "assets/icons/cloud-devops/prometheus.svg"),
    "terraform": ("Terraform", "assets/icons/cloud-devops/terraform.svg"),
    # Databases
    "bigquery": ("BigQuery", "assets/icons/databases/bigquery.svg"),
    "cassandra": ("Cassandra", "assets/icons/databases/cassandra.svg"),
    "dbt": ("dbt", "assets/icons/databases/dbt.svg"),
    "elasticsearch": ("Elasticsearch", "assets/icons/databases/elasticsearch.svg"),
    "mongodb": ("MongoDB", "assets/icons/databases/mongodb.svg"),
    "mysql": ("MySQL", "assets/icons/databases/mysql.svg"),
    "postgresql": ("PostgreSQL", "assets/icons/databases/postgresql.svg"),
    "redis": ("Redis", "assets/icons/databases/redis.svg"),
    "snowflake": ("Snowflake", "assets/icons/databases/snowflake.svg"),
    # Frontend
    "angular": ("Angular", "assets/icons/frontend/angular.svg"),
    "css3": ("CSS3", "assets/icons/frontend/css3.svg"),
    "graphql": ("GraphQL", "assets/icons/frontend/graphql.svg"),
    "html5": ("HTML5", "assets/icons/frontend/html5.svg"),
    "javascript": ("JavaScript", "assets/icons/frontend/javascript.svg"),
    "nextjs": ("Next.js", "assets/icons/frontend/nextjs.svg"),
    "react": ("React", "assets/icons/frontend/react.svg"),
    "redux": ("Redux", "assets/icons/frontend/redux.svg"),
    "tailwindcss": ("Tailwind CSS", "assets/icons/frontend/tailwindcss.svg"),
    "typescript": ("TypeScript", "assets/icons/frontend/typescript.svg"),
    "vite": ("Vite", "assets/icons/frontend/vite.svg"),
    "vuejs": ("Vue.js", "assets/icons/frontend/vuejs.svg"),
    # Messaging
    "kafka": ("Kafka", "assets/icons/messaging/kafka.svg"),
    "rabbitmq": ("RabbitMQ", "assets/icons/messaging/rabbitmq.svg"),
    # Mobile
    "android": ("Android", "assets/icons/mobile/android.svg"),
    "androidstudio": ("Android Studio", "assets/icons/mobile/androidstudio.svg"),
    "apple": ("Apple", "assets/icons/mobile/apple.svg"),
    "expo": ("Expo", "assets/icons/mobile/expo.svg"),
    "flutter": ("Flutter", "assets/icons/mobile/flutter.svg"),
    "kotlin": ("Kotlin", "assets/icons/mobile/kotlin.svg"),
    "reactnative": ("React Native", "assets/icons/mobile/reactnative.svg"),
    "swift": ("Swift", "assets/icons/mobile/swift.svg"),
    "xcode": ("Xcode", "assets/icons/mobile/xcode.svg"),
}

# Developer nicknames and common aliases mapped to canonical icon stems
ICON_ALIASES: dict[str, str] = {
    # Programming languages & runtimes
    "c++": "cplusplus",
    "cpp": "cplusplus",
    "go": "golang",
    "golang": "golang",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "node": "nodejs",
    "node.js": "nodejs",
    "next": "nextjs",
    "next.js": "nextjs",
    "react.js": "react",
    "vue": "vuejs",
    "vue.js": "vuejs",
    "tailwind": "tailwindcss",
    "tailwind-css": "tailwindcss",
    "html": "html5",
    "css": "css3",
    # Cloud & DevOps
    "k8s": "kubernetes",
    "kube": "kubernetes",
    "gcp": "googlecloud",
    "google-cloud": "googlecloud",
    "google_cloud": "googlecloud",
    "gh-actions": "githubactions",
    "github-actions": "githubactions",
    "github_actions": "githubactions",
    "tf": "terraform",
    # Databases
    "postgres": "postgresql",
    "pgsql": "postgresql",
    "postgre": "postgresql",
    "mongo": "mongodb",
    "elastic": "elasticsearch",
    "es": "elasticsearch",
    # AI & ML
    "hf": "huggingface",
    "hugging-face": "huggingface",
    "hugging_face": "huggingface",
    "spark": "apachespark",
    "apache-spark": "apachespark",
    "apache_spark": "apachespark",
    "sklearn": "scikitlearn",
    "scikit": "scikitlearn",
    "scikit-learn": "scikitlearn",
    "tensor-flow": "tensorflow",
    "w&b": "wandb",
    "weights-and-biases": "wandb",
    # Mobile
    "rn": "reactnative",
    "react-native": "reactnative",
    "react_native": "reactnative",
    "android-studio": "androidstudio",
    "android_studio": "androidstudio",
}


def list_available_icon_names() -> list[str]:
    """Returns sorted list of all supported canonical icon names and common aliases."""
    return sorted(set(CANONICAL_ICONS.keys()) | set(ICON_ALIASES.keys()))


def resolve_icon(query: str) -> tuple[str, str]:
    """
    Resolves an icon identifier query to a canonical (display_label, relative_svg_path) tuple.
    Supports formats:
      - 'python' -> ('Python', 'assets/icons/backend/python.svg')
      - 'k8s' -> ('Kubernetes', 'assets/icons/cloud-devops/kubernetes.svg')
      - 'golang:Go' -> ('Go', 'assets/icons/backend/golang.svg') (custom label override)
      - Direct path: 'assets/icons/backend/python.svg'

    Raises ValueError with suggested matches if the icon cannot be found.
    """
    raw_query = query.strip()
    if not raw_query:
        raise ValueError("Icon identifier cannot be empty.")

    custom_label: str | None = None
    if ":" in raw_query:
        parts = raw_query.split(":", 1)
        raw_query = parts[0].strip()
        custom_label = parts[1].strip()

    clean_key = raw_query.lower().replace(" ", "").replace("-", "").replace("_", "")

    # 1. Check aliases first
    stem = ICON_ALIASES.get(raw_query.lower()) or ICON_ALIASES.get(clean_key)

    # 2. Check canonical dictionary
    if not stem:
        if raw_query.lower() in CANONICAL_ICONS:
            stem = raw_query.lower()
        elif clean_key in CANONICAL_ICONS:
            stem = clean_key

    # 3. Direct path or stem lookup in CANONICAL_ICONS
    if not stem:
        for s, (lbl, p) in CANONICAL_ICONS.items():
            if raw_query.lower() == s or raw_query.lower() == lbl.lower() or raw_query == p:
                stem = s
                break

    if stem and stem in CANONICAL_ICONS:
        canonical_label, path = CANONICAL_ICONS[stem]
        final_label = custom_label if custom_label else canonical_label
        # Verify file exists on disk
        full_path = REPO_ROOT / path
        if not full_path.is_file():
            raise FileNotFoundError(f"Icon file referenced by '{stem}' does not exist: {full_path}")
        return final_label, path

    # If not resolved, find suggestions using difflib
    candidates = list(CANONICAL_ICONS.keys()) + list(ICON_ALIASES.keys())
    matches = difflib.get_close_matches(raw_query.lower(), candidates, n=3, cutoff=0.5)
    suggestion_msg = f" Did you mean: {', '.join(matches)}?" if matches else ""
    raise ValueError(
        f"Unknown icon '{query}'.{suggestion_msg}\n"
        f"Available icons include: {', '.join(sorted(CANONICAL_ICONS.keys())[:15])} ... (75 total)."
    )


def parse_icons_arg(icons_spec: str | list[str] | list[tuple[str, str]]) -> list[tuple[str, str]]:
    """
    Parses a comma-separated string or list of icon queries into a list of (label, path) tuples.
    Example: 'go, python, react, docker, aws'
    """
    if isinstance(icons_spec, str):
        raw_items = [item.strip() for item in icons_spec.split(",") if item.strip()]
    elif isinstance(icons_spec, list):
        if not icons_spec:
            return []
        if isinstance(icons_spec[0], tuple):
            return list(icons_spec)  # type: ignore[return-value]
        raw_items = [str(item).strip() for item in icons_spec if str(item).strip()]
    else:
        raise ValueError(f"Invalid icons specification type: {type(icons_spec)}")

    resolved: list[tuple[str, str]] = []
    for item in raw_items:
        resolved.append(resolve_icon(item))
    return resolved


def validate_banner_standards(
    title: str,
    subtitle: str,
    icons: list[tuple[str, str]],
) -> None:
    """
    Strictly enforces visual excellence guidelines and safe-zone constraints:
    - Icon count: 3 to 8 icons (prevents profile avatar overlap and right-edge clipping)
    - Title length: 3 to 45 characters (prevents headline text overflow)
    - Subtitle length: 3 to 70 characters (prevents description text overflow)
    - Icon validity: Every icon must have a valid label and existing file path
    """
    # 1. Icon Count Standards
    num_icons = len(icons)
    if num_icons < MIN_ICONS:
        raise ValueError(
            f"Visual Standard Violation: Banner must contain at least {MIN_ICONS} icons (provided: {num_icons}). "
            f"Banners with fewer than {MIN_ICONS} icons leave excessive empty space and look substandard."
        )
    if num_icons > MAX_ICONS:
        raise ValueError(
            f"Layout Constraint Violation: Banner cannot contain more than {MAX_ICONS} icons (provided: {num_icons}). "
            f"Single-row layout is capped at {MAX_ICONS} icons (912px width) to guarantee safe margins against "
            f"the LinkedIn profile photo safe zone (520px offset)."
        )

    # 2. Title Standards
    clean_title = title.strip()
    if len(clean_title) < MIN_TITLE_LENGTH:
        raise ValueError(
            f"Title '{title}' is too short ({len(clean_title)} chars). Minimum length is {MIN_TITLE_LENGTH} characters."
        )
    if len(clean_title) > MAX_TITLE_LENGTH:
        raise ValueError(
            f"Layout Constraint Violation: Title '{title}' is {len(clean_title)} characters. "
            f"Maximum allowed length is {MAX_TITLE_LENGTH} characters to prevent headline overflow at 48px font size."
        )

    # 3. Subtitle Standards
    clean_sub = subtitle.strip()
    if len(clean_sub) < MIN_SUBTITLE_LENGTH:
        raise ValueError(
            f"Subtitle is too short ({len(clean_sub)} chars). Minimum length is {MIN_SUBTITLE_LENGTH} characters."
        )
    if len(clean_sub) > MAX_SUBTITLE_LENGTH:
        raise ValueError(
            f"Layout Constraint Violation: Subtitle is {len(clean_sub)} characters. "
            f"Maximum allowed length is {MAX_SUBTITLE_LENGTH} characters to prevent description overflow at 22px font size."
        )

    # 4. Icon Integrity
    for idx, item in enumerate(icons):
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError(
                f"Invalid icon tuple at index {idx}: {item}. Expected (label, file_path)."
            )
        lbl, p = item
        if not lbl or not p:
            raise ValueError(f"Icon at index {idx} has empty label or path: {item}")
        full = REPO_ROOT / p
        if not full.is_file():
            raise FileNotFoundError(f"Icon '{lbl}' references nonexistent file: {full}")


def build_custom_preset(
    title: str | None = None,
    subtitle: str | None = None,
    icons_spec: str | list[str] | list[tuple[str, str]] | None = None,
    base_preset: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Constructs and validates a banner specification dictionary.
    Inherits from base_preset if provided, applying fine-grained overrides.
    """
    final_title = (
        title.strip()
        if title
        else (base_preset.get("title", "Software Engineer") if base_preset else "Software Engineer")
    )
    final_subtitle = (
        subtitle.strip()
        if subtitle
        else (
            base_preset.get("subtitle", "Engineering • Architecture • Cloud Native")
            if base_preset
            else "Engineering • Architecture • Cloud Native"
        )
    )

    if icons_spec:
        final_icons = parse_icons_arg(icons_spec)
    elif base_preset and "icons" in base_preset:
        final_icons = list(base_preset["icons"])
    else:
        # Default fallback
        final_icons = [
            CANONICAL_ICONS["python"],
            CANONICAL_ICONS["golang"],
            CANONICAL_ICONS["typescript"],
            CANONICAL_ICONS["docker"],
            CANONICAL_ICONS["kubernetes"],
            CANONICAL_ICONS["aws"],
        ]

    # Enforce strict visual standards
    validate_banner_standards(final_title, final_subtitle, final_icons)

    return {
        "title": final_title,
        "subtitle": final_subtitle,
        "icons": final_icons,
    }
