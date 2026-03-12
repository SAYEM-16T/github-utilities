#!/usr/bin/env python3

import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import requests


APP_NAME = "GitHub Profile Tree Visualizer"
APP_VERSION = "3.0.0"
GITHUB_API_BASE = "https://api.github.com"
DEFAULT_TIMEOUT = 30

IGNORE_NAMES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".terraform",
    ".venv",
    "venv",
    ".next",
    "dist",
    "build",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".cache",
    ".DS_Store",
}

ICON_SET = {
    "repo": "📦",
    "folder": "📁",
    "default_file": "📄",
    "hidden_file": "🙈",
    "config": "⚙️",
    "binary": "💾",
    "archive": "🗜️",
    "cert": "🔐",
    "key": "🗝️",
    "database": "🗃️",
    "code": "💻",
    "text": "📝",
    "image": "🖼️",
    "video": "🎞️",
    "audio": "🎵",
    "doc": "📘",
    "script": "🖥️",
    "package": "📦",
    "cloud": "☁️",
    "security": "🛡️",
    "docker": "🐳",
    "k8s": "☸️",
    "terraform": "🏗️",
    "ci": "🚀",
    "log": "📜",
    "shell": "🐚",
    "test": "🧪",
    "tools": "🧰",
    "workflow": "🚀",
    "book": "📚",
    "api": "🔌",
    "profile": "👤",
    "lock": "🔒",
    "warning": "⚠️",
    "success": "✅",
    "info": "ℹ️",
    "star": "⭐",
    "branch": "🌿",
    "clock": "🕒",
    "lang": "💻",
    "desc": "📝",
    "files": "📄",
    "folders": "📁",
}

FILE_ICONS = {
    ".py": "🐍",
    ".pyw": "🐍",
    ".pyc": "🐍",
    ".pyd": "🐍",
    ".ipynb": "📓",
    ".js": "🟨",
    ".mjs": "🟨",
    ".cjs": "🟨",
    ".jsx": "⚛️",
    ".ts": "🟦",
    ".tsx": "⚛️",
    ".html": "🌐",
    ".htm": "🌐",
    ".css": "🎨",
    ".scss": "🎨",
    ".sass": "🎨",
    ".less": "🎨",
    ".json": "🧾",
    ".jsonc": "🧾",
    ".yaml": "⚙️",
    ".yml": "⚙️",
    ".xml": "🧩",
    ".toml": "⚙️",
    ".ini": "⚙️",
    ".cfg": "⚙️",
    ".conf": "⚙️",
    ".properties": "⚙️",
    ".sh": "🐚",
    ".bash": "🐚",
    ".zsh": "🐚",
    ".fish": "🐚",
    ".ksh": "🐚",
    ".ps1": "💠",
    ".bat": "🪟",
    ".cmd": "🪟",
    ".c": "🔧",
    ".h": "🔧",
    ".cpp": "⚙️",
    ".cc": "⚙️",
    ".cxx": "⚙️",
    ".hpp": "⚙️",
    ".hh": "⚙️",
    ".java": "☕",
    ".class": "☕",
    ".jar": "🍵",
    ".gradle": "🐘",
    ".groovy": "🎼",
    ".kt": "🟪",
    ".kts": "🟪",
    ".go": "🐹",
    ".rs": "🦀",
    ".php": "🐘",
    ".rb": "💎",
    ".pl": "🐪",
    ".pm": "🐪",
    ".lua": "🌙",
    ".swift": "🕊️",
    ".dart": "🎯",
    ".r": "📊",
    ".jl": "🔮",
    ".m": "📐",
    ".sql": "🗃️",
    ".sqlite": "🗃️",
    ".db": "🗃️",
    ".db3": "🗃️",
    ".md": "📘",
    ".markdown": "📘",
    ".txt": "📝",
    ".rst": "📘",
    ".adoc": "📘",
    ".rtf": "📄",
    ".doc": "📄",
    ".docx": "📄",
    ".odt": "📄",
    ".pdf": "📕",
    ".ppt": "📊",
    ".pptx": "📊",
    ".odp": "📊",
    ".xls": "📗",
    ".xlsx": "📗",
    ".ods": "📗",
    ".csv": "📊",
    ".tsv": "📊",
    ".png": "🖼️",
    ".jpg": "🖼️",
    ".jpeg": "🖼️",
    ".gif": "🎞️",
    ".bmp": "🖼️",
    ".webp": "🖼️",
    ".svg": "🖼️",
    ".ico": "🖼️",
    ".tiff": "🖼️",
    ".psd": "🎨",
    ".ai": "🎨",
    ".mp3": "🎵",
    ".wav": "🎵",
    ".ogg": "🎵",
    ".flac": "🎵",
    ".aac": "🎵",
    ".m4a": "🎵",
    ".mp4": "🎞️",
    ".mkv": "🎞️",
    ".avi": "🎞️",
    ".mov": "🎞️",
    ".webm": "🎞️",
    ".flv": "🎞️",
    ".zip": "🗜️",
    ".tar": "🗜️",
    ".gz": "🗜️",
    ".bz2": "🗜️",
    ".xz": "🗜️",
    ".7z": "🗜️",
    ".rar": "🗜️",
    ".tgz": "🗜️",
    ".log": "📜",
    ".out": "📜",
    ".err": "📜",
    ".tf": "🏗️",
    ".tfvars": "🏗️",
    ".hcl": "🏗️",
    ".nomad": "🏗️",
    ".env": "🔐",
    ".pem": "🔐",
    ".crt": "🔐",
    ".cer": "🔐",
    ".key": "🗝️",
    ".pub": "🗝️",
    ".csr": "🔐",
    ".service": "⚙️",
    ".timer": "⏲️",
    ".socket": "🔌",
    ".lock": "🔒",
    ".sum": "📦",
    ".mod": "📦",
}

SPECIAL_FILE_ICONS = {
    "readme": "📘",
    "readme.md": "📘",
    "readme.txt": "📘",
    "changelog": "📝",
    "changelog.md": "📝",
    "changes.md": "📝",
    "contributing": "🤝",
    "contributing.md": "🤝",
    "license": "📜",
    "license.txt": "📜",
    "license.md": "📜",
    "copying": "📜",
    "notice": "📢",
    "authors": "👥",
    "todo.md": "✅",
    ".gitignore": "🙈",
    ".gitattributes": "🔧",
    ".gitmodules": "🔗",
    "dockerfile": "🐳",
    "docker-compose.yml": "🐳",
    "docker-compose.yaml": "🐳",
    "compose.yml": "🐳",
    "compose.yaml": "🐳",
    ".dockerignore": "🙈",
    "chart.yaml": "☸️",
    "chart.yml": "☸️",
    "values.yaml": "☸️",
    "values.yml": "☸️",
    "kustomization.yaml": "☸️",
    "kustomization.yml": "☸️",
    "jenkinsfile": "🔧",
    ".gitlab-ci.yml": "🚀",
    "azure-pipelines.yml": "🚀",
    "azure-pipelines.yaml": "🚀",
    ".travis.yml": "🚀",
    "requirements.txt": "📋",
    "pyproject.toml": "🐍",
    "setup.py": "🐍",
    "setup.cfg": "🐍",
    "pipfile": "🐍",
    "pipfile.lock": "🔒",
    "poetry.lock": "🔒",
    ".python-version": "🐍",
    "package.json": "📦",
    "package-lock.json": "🔒",
    "yarn.lock": "🔒",
    "pnpm-lock.yaml": "🔒",
    "tsconfig.json": "🟦",
    "vite.config.js": "⚡",
    "vite.config.ts": "⚡",
    "webpack.config.js": "📦",
    "webpack.config.ts": "📦",
    ".eslintrc": "🧹",
    ".eslintrc.json": "🧹",
    ".prettierrc": "✨",
    "go.mod": "📦",
    "go.sum": "📦",
    "cargo.toml": "🦀",
    "cargo.lock": "🔒",
    "pom.xml": "☕",
    "build.gradle": "🐘",
    "settings.gradle": "🐘",
    "gradle.properties": "🐘",
    "mvnw": "☕",
    "mvnw.cmd": "☕",
    "main.tf": "🏗️",
    "variables.tf": "🏗️",
    "outputs.tf": "🏗️",
    "providers.tf": "🏗️",
    "versions.tf": "🏗️",
    "backend.tf": "🏗️",
    "terraform.tfvars": "🏗️",
    ".terraform.lock.hcl": "🔒",
    "inventory": "📋",
    "hosts": "🖧",
    "ansible.cfg": "⚙️",
    ".env": "🔐",
    ".env.example": "🔐",
    ".env.local": "🔐",
    ".bashrc": "🐚",
    ".zshrc": "🐚",
    ".profile": "👤",
    "makefile": "🛠️",
    "cmakelists.txt": "🛠️",
    "serverless.yml": "☁️",
    "serverless.yaml": "☁️",
    "template.yaml": "☁️",
    "template.yml": "☁️",
    "cloudformation.yaml": "☁️",
    "cloudformation.yml": "☁️",
    "id_rsa": "🗝️",
    "id_rsa.pub": "🗝️",
    "id_ed25519": "🗝️",
    "id_ed25519.pub": "🗝️",
}

SPECIAL_FOLDER_ICONS = {
    ".github": "🐙",
    ".git": "🐙",
    ".vscode": "🧰",
    ".idea": "🧰",
    "src": "💻",
    "app": "📱",
    "apps": "📱",
    "bin": "📦",
    "build": "🏗️",
    "dist": "📦",
    "docs": "📚",
    "doc": "📚",
    "scripts": "🖥️",
    "script": "🖥️",
    "config": "⚙️",
    "configs": "⚙️",
    "k8s": "☸️",
    "helm": "☸️",
    "charts": "☸️",
    "terraform": "🏗️",
    "modules": "🧩",
    "tests": "🧪",
    "test": "🧪",
    "assets": "🎨",
    "images": "🖼️",
    "img": "🖼️",
    "static": "🖼️",
    "public": "🌐",
    "templates": "📄",
    "api": "🔌",
    "database": "🗃️",
    "db": "🗃️",
    "auth": "🔐",
    "security": "🛡️",
    "logs": "📜",
    "monitoring": "📈",
    "deploy": "🚀",
    "deployment": "🚀",
    "workflows": "🚀",
}


def ask_input(prompt: str, default: Optional[str] = None) -> str:
    if default is not None:
        value = input(f"{prompt} [{default}]: ").strip()
        return value if value else default
    return input(f"{prompt}: ").strip()


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    value = input(f"{prompt} [{suffix}]: ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes"}


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def safe_filename(value: str) -> str:
    out = []
    for ch in value:
        if ch.isalnum() or ch in {"-", "_", "."}:
            out.append(ch)
        else:
            out.append("_")
    return "".join(out)


def get_iso_now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def format_count(n: int) -> str:
    return f"{n:,}"


def get_headers(token: Optional[str]) -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": APP_NAME,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_repos(username: str, token: Optional[str] = None) -> List[Dict]:
    repos = []
    page = 1
    headers = get_headers(token)

    while True:
        url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page=100&page={page}&sort=updated"
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 404:
            raise Exception(f"GitHub user '{username}' not found")

        response.raise_for_status()
        data = response.json()

        if not data:
            break

        repos.extend(data)
        page += 1

    return repos


def get_repo_tree(owner: str, repo: str, branch: str, token: Optional[str] = None) -> Optional[Dict]:
    headers = get_headers(token)
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

    if response.status_code != 200:
        return None

    return response.json()


def build_nested_tree(paths: List[str], ignore_names: set) -> Dict:
    root: Dict = {}

    for path in paths:
        parts = path.split("/")
        current = root
        skip_path = False

        for part in parts:
            if part in ignore_names:
                skip_path = True
                break
            current = current.setdefault(part, {})

        if skip_path:
            continue

    return root


def count_tree_nodes(tree: Dict) -> Tuple[int, int]:
    folder_count = 0
    file_count = 0

    for _, subtree in tree.items():
        if subtree:
            folder_count += 1
            sub_folders, sub_files = count_tree_nodes(subtree)
            folder_count += sub_folders
            file_count += sub_files
        else:
            file_count += 1

    return folder_count, file_count


def sort_items(tree: Dict) -> List[Tuple[str, Dict]]:
    folders = []
    files = []

    for name, subtree in tree.items():
        if subtree:
            folders.append((name, subtree))
        else:
            files.append((name, subtree))

    folders.sort(key=lambda x: x[0].lower())
    files.sort(key=lambda x: x[0].lower())

    return folders + files


def get_folder_icon(name: str, emojis_enabled: bool) -> str:
    if not emojis_enabled:
        return ""

    lower_name = name.lower()

    if lower_name in SPECIAL_FOLDER_ICONS:
        return SPECIAL_FOLDER_ICONS[lower_name]

    if lower_name.startswith("."):
        return ICON_SET["tools"]
    if "test" in lower_name:
        return ICON_SET["test"]
    if "doc" in lower_name:
        return ICON_SET["book"]
    if "config" in lower_name:
        return ICON_SET["config"]
    if "script" in lower_name:
        return ICON_SET["script"]
    if "image" in lower_name or "asset" in lower_name or "static" in lower_name:
        return ICON_SET["image"]
    if "deploy" in lower_name or "workflow" in lower_name:
        return ICON_SET["workflow"]
    if "monitor" in lower_name:
        return "📈"
    if "log" in lower_name:
        return ICON_SET["log"]
    if "auth" in lower_name:
        return "🔐"
    if "data" in lower_name or "db" in lower_name:
        return ICON_SET["database"]
    if "api" in lower_name:
        return ICON_SET["api"]

    return ICON_SET["folder"]


def get_file_icon(name: str, emojis_enabled: bool) -> str:
    if not emojis_enabled:
        return ""

    lower_name = name.lower()

    if lower_name in SPECIAL_FILE_ICONS:
        return SPECIAL_FILE_ICONS[lower_name]

    if lower_name.startswith("."):
        return ICON_SET["hidden_file"]

    for ext, icon in FILE_ICONS.items():
        if lower_name.endswith(ext):
            return icon

    if "docker" in lower_name:
        return ICON_SET["docker"]
    if "k8s" in lower_name or "kube" in lower_name or "helm" in lower_name:
        return ICON_SET["k8s"]
    if "terraform" in lower_name or "tfvars" in lower_name:
        return ICON_SET["terraform"]
    if "jenkins" in lower_name or "pipeline" in lower_name or "workflow" in lower_name:
        return ICON_SET["ci"]
    if "config" in lower_name or "setting" in lower_name:
        return ICON_SET["config"]
    if "secret" in lower_name or "token" in lower_name or "auth" in lower_name:
        return ICON_SET["security"]
    if "cert" in lower_name or "pem" in lower_name or "crt" in lower_name:
        return ICON_SET["cert"]
    if "key" in lower_name:
        return ICON_SET["key"]
    if "log" in lower_name:
        return ICON_SET["log"]
    if "test" in lower_name:
        return ICON_SET["test"]
    if "demo" in lower_name or "sample" in lower_name or "example" in lower_name:
        return "🧩"
    if "db" in lower_name or "data" in lower_name:
        return ICON_SET["database"]
    if "api" in lower_name:
        return ICON_SET["api"]
    if "script" in lower_name:
        return ICON_SET["script"]
    if "doc" in lower_name or "guide" in lower_name:
        return ICON_SET["doc"]
    if "cloud" in lower_name or "aws" in lower_name or "gcp" in lower_name or "azure" in lower_name:
        return ICON_SET["cloud"]
    if "package" in lower_name:
        return ICON_SET["package"]
    if "binary" in lower_name or lower_name.endswith(".bin"):
        return ICON_SET["binary"]
    if "archive" in lower_name:
        return ICON_SET["archive"]
    if "note" in lower_name or "text" in lower_name:
        return ICON_SET["text"]
    if "image" in lower_name or "logo" in lower_name or "icon" in lower_name:
        return ICON_SET["image"]
    if "video" in lower_name:
        return ICON_SET["video"]
    if "audio" in lower_name:
        return ICON_SET["audio"]
    if "code" in lower_name:
        return ICON_SET["code"]

    return ICON_SET["default_file"]


def render_tree_lines(
    tree: Dict,
    prefix: str = "",
    current_depth: int = 1,
    max_depth: int = 0,
    emojis_enabled: bool = True,
) -> List[str]:
    lines = []
    items = sort_items(tree)

    for i, (name, subtree) in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "

        if subtree:
            icon = get_folder_icon(name, emojis_enabled)
            label = f"{icon} {name}" if icon else name
            lines.append(f"{prefix}{connector}{label}")

            if max_depth == 0 or current_depth < max_depth:
                extension = "    " if is_last else "│   "
                lines.extend(
                    render_tree_lines(
                        subtree,
                        prefix + extension,
                        current_depth=current_depth + 1,
                        max_depth=max_depth,
                        emojis_enabled=emojis_enabled,
                    )
                )
        else:
            icon = get_file_icon(name, emojis_enabled)
            label = f"{icon} {name}" if icon else name
            lines.append(f"{prefix}{connector}{label}")

    return lines


def repo_metadata_lines(repo: Dict, emojis_enabled: bool = True) -> List[str]:
    desc_icon = ICON_SET["desc"] + " " if emojis_enabled else ""
    star_icon = ICON_SET["star"] + " " if emojis_enabled else ""
    lang_icon = ICON_SET["lang"] + " " if emojis_enabled else ""
    branch_icon = ICON_SET["branch"] + " " if emojis_enabled else ""
    clock_icon = ICON_SET["clock"] + " " if emojis_enabled else ""

    description = repo.get("description") or "No description"
    stars = repo.get("stargazers_count", 0)
    language = repo.get("language") or "N/A"
    branch = repo.get("default_branch") or "N/A"
    updated = repo.get("updated_at") or "N/A"

    return [
        f"    • {desc_icon}Description: {description}",
        f"    • {star_icon}Stars: {stars}",
        f"    • {lang_icon}Language: {language}",
        f"    • {branch_icon}Default Branch: {branch}",
        f"    • {clock_icon}Updated At: {updated}",
    ]


def prepare_repo_data(
    username: str,
    repos: List[Dict],
    token: Optional[str],
    ignore_names: set,
) -> List[Dict]:
    prepared = []

    for repo in repos:
        repo_name = repo["name"]
        default_branch = repo.get("default_branch", "main")
        tree_data = get_repo_tree(username, repo_name, default_branch, token=token)

        if not tree_data or "tree" not in tree_data:
            prepared.append(
                {
                    "repo": repo,
                    "nested_tree": {},
                    "folder_count": 0,
                    "file_count": 0,
                    "fetch_error": True,
                }
            )
            continue

        paths = [
            item["path"]
            for item in tree_data["tree"]
            if item.get("type") in ("blob", "tree")
        ]

        nested_tree = build_nested_tree(paths, ignore_names=ignore_names)
        folder_count, file_count = count_tree_nodes(nested_tree)

        prepared.append(
            {
                "repo": repo,
                "nested_tree": nested_tree,
                "folder_count": folder_count,
                "file_count": file_count,
                "fetch_error": False,
            }
        )

    return prepared


def print_banner() -> None:
    print(f"\n🌳 {APP_NAME} v{APP_VERSION}")
    print("=" * 60)


def get_token_from_user() -> Optional[str]:
    use_token = ask_yes_no("Do you want to use a GitHub token", default=False)
    if not use_token:
        return None
    token = ask_input("Enter GitHub token").strip()
    return token or None


def choose_mode() -> str:
    print("\nChoose mode:")
    print("1. Show full tree for all repos")
    print("2. Show repo names first, then select repos")

    while True:
        choice = input("Enter choice [1/2]: ").strip()
        if choice == "1":
            return "all repos"
        if choice == "2":
            return "selected repos"
        print("❌ Invalid choice. Please enter 1 or 2.")


def choose_output_format() -> str:
    print("\nChoose output format:")
    print("1. Text")
    print("2. Markdown")
    print("3. JSON")

    while True:
        choice = input("Enter choice [1/2/3]: ").strip()
        if choice == "1":
            return "text"
        if choice == "2":
            return "markdown"
        if choice == "3":
            return "json"
        print("❌ Invalid choice. Please enter 1, 2, or 3.")


def get_depth_limit() -> int:
    value = ask_input("Enter max depth (0 = unlimited)", "0")
    depth = parse_int(value, 0)
    if depth < 0:
        return 0
    return depth


def parse_repo_selection(selection: str, total: int) -> List[int]:
    selected = set()

    if not selection.strip():
        return []

    parts = [p.strip() for p in selection.split(",") if p.strip()]

    for part in parts:
        if "-" in part:
            try:
                start_s, end_s = part.split("-", 1)
                start_n = int(start_s)
                end_n = int(end_s)
                if start_n > end_n:
                    start_n, end_n = end_n, start_n
                for n in range(start_n, end_n + 1):
                    if 1 <= n <= total:
                        selected.add(n)
            except ValueError:
                continue
        else:
            try:
                n = int(part)
                if 1 <= n <= total:
                    selected.add(n)
            except ValueError:
                continue

    return sorted(selected)


def make_table(headers: List[str], rows: List[List[str]]) -> str:
    if not rows:
        widths = [len(h) for h in headers]
    else:
        widths = [len(h) for h in headers]
        for row in rows:
            for i, value in enumerate(row):
                widths[i] = max(widths[i], len(str(value)))

    def border(sep: str = "-") -> str:
        return "+" + "+".join(sep * (w + 2) for w in widths) + "+"

    def row_line(values: List[str]) -> str:
        return "|" + "|".join(f" {str(v).ljust(widths[i])} " for i, v in enumerate(values)) + "|"

    lines = [border(), row_line(headers), border("=")]
    for row in rows:
        lines.append(row_line(row))
    lines.append(border())
    return "\n".join(lines)


def display_repo_list(repos: List[Dict], emojis_enabled: bool = True) -> None:
    headers = ["No", "Repo Name", "Language", "Updated", "Stars", "Branch"]

    rows = []
    for idx, repo in enumerate(repos, start=1):
        repo_name = repo.get("name", "unknown")
        if emojis_enabled:
            repo_name = f"{ICON_SET['repo']} {repo_name}"

        language = repo.get("language") or "N/A"
        updated = repo.get("updated_at", "")
        updated_short = updated[:10] if updated else "N/A"
        stars = str(repo.get("stargazers_count", 0))
        branch = repo.get("default_branch") or "N/A"

        rows.append([
            str(idx),
            repo_name,
            language,
            updated_short,
            stars,
            branch,
        ])

    print("\nAvailable repositories:")
    print(make_table(headers, rows))
    print("Tip: You can select like 1,3,5 or range 2-6 or mixed 1,3-5,8")


def choose_repos(repos: List[Dict], emojis_enabled: bool = True) -> List[Dict]:
    while True:
        display_repo_list(repos, emojis_enabled=emojis_enabled)
        selection = input("\nEnter repo numbers: ").strip()

        selected_indexes = parse_repo_selection(selection, len(repos))
        if not selected_indexes:
            print("❌ Invalid selection. Please try again.")
            continue

        chosen = [repos[i - 1] for i in selected_indexes]
        print(f"✅ Selected {len(chosen)} repositories.")
        return chosen


def build_text_report(
    username: str,
    prepared_repos: List[Dict],
    selected_mode: str,
    token_used: bool,
    max_depth: int,
    emojis_enabled: bool,
    include_metadata: bool,
) -> str:
    lines = []
    profile_icon = ICON_SET["profile"] + " " if emojis_enabled else ""

    lines.append(f"{profile_icon}GitHub Profile: {username}")
    lines.append(f"Generated At: {get_iso_now()}")
    lines.append(f"Mode: {selected_mode}")
    lines.append(f"Total Repositories in Report: {len(prepared_repos)}")
    lines.append(f"Token Used: {'Yes' if token_used else 'No'}")
    lines.append(f"Max Depth: {'Unlimited' if max_depth == 0 else max_depth}")
    lines.append(f"Emojis: {'Enabled' if emojis_enabled else 'Disabled'}")
    lines.append("")
    lines.append(f"{username}/")

    for idx, repo_data in enumerate(prepared_repos):
        repo = repo_data["repo"]
        repo_name = repo["name"]
        connector = "└── " if idx == len(prepared_repos) - 1 else "├── "
        repo_icon = ICON_SET["repo"] if emojis_enabled else ""
        repo_label = f"{repo_icon} {repo_name}" if repo_icon else repo_name
        lines.append(f"{connector}{repo_label}")

        child_prefix = "    " if idx == len(prepared_repos) - 1 else "│   "

        if include_metadata:
            for meta_line in repo_metadata_lines(repo, emojis_enabled=emojis_enabled):
                lines.append(f"{child_prefix}{meta_line}")

            folders_icon = ICON_SET["folders"] + " " if emojis_enabled else ""
            files_icon = ICON_SET["files"] + " " if emojis_enabled else ""
            lines.append(f"{child_prefix}    • {folders_icon}Folders: {format_count(repo_data.get('folder_count', 0))}")
            lines.append(f"{child_prefix}    • {files_icon}Files: {format_count(repo_data.get('file_count', 0))}")

        if repo_data.get("fetch_error"):
            warning_icon = ICON_SET["warning"] if emojis_enabled else "!"
            lines.append(f"{child_prefix}└── {warning_icon} [Could not fetch tree]")
            continue

        tree_lines = render_tree_lines(
            repo_data["nested_tree"],
            prefix=child_prefix,
            current_depth=1,
            max_depth=max_depth,
            emojis_enabled=emojis_enabled,
        )
        lines.extend(tree_lines)

    return "\n".join(lines)


def build_markdown_report(
    username: str,
    prepared_repos: List[Dict],
    selected_mode: str,
    token_used: bool,
    max_depth: int,
    emojis_enabled: bool,
    include_metadata: bool,
) -> str:
    lines = []
    lines.append(f"# GitHub Profile Report: {username}")
    lines.append("")
    lines.append(f"- Generated At: {get_iso_now()}")
    lines.append(f"- Mode: {selected_mode}")
    lines.append(f"- Total Repositories in Report: {len(prepared_repos)}")
    lines.append(f"- Token Used: {'Yes' if token_used else 'No'}")
    lines.append(f"- Max Depth: {'Unlimited' if max_depth == 0 else max_depth}")
    lines.append(f"- Emojis: {'Enabled' if emojis_enabled else 'Disabled'}")
    lines.append("")

    summary_headers = ["Repo Name", "Language", "Stars", "Updated", "Folders", "Files"]
    summary_rows = []
    for repo_data in prepared_repos:
        repo = repo_data["repo"]
        summary_rows.append([
            repo.get("name", ""),
            repo.get("language") or "N/A",
            str(repo.get("stargazers_count", 0)),
            (repo.get("updated_at") or "")[:10] if repo.get("updated_at") else "N/A",
            str(repo_data.get("folder_count", 0)),
            str(repo_data.get("file_count", 0)),
        ])

    lines.append("## Repository Summary")
    lines.append("")
    lines.append("```text")
    lines.append(make_table(summary_headers, summary_rows))
    lines.append("```")
    lines.append("")

    for repo_data in prepared_repos:
        repo = repo_data["repo"]
        lines.append(f"## {repo['name']}")
        lines.append("")

        if include_metadata:
            desc = repo.get("description") or "No description"
            lang = repo.get("language") or "N/A"
            stars = repo.get("stargazers_count", 0)
            branch = repo.get("default_branch") or "N/A"
            updated = repo.get("updated_at") or "N/A"
            folder_count = repo_data.get("folder_count", 0)
            file_count = repo_data.get("file_count", 0)

            lines.append(f"- Description: {desc}")
            lines.append(f"- Language: {lang}")
            lines.append(f"- Stars: {stars}")
            lines.append(f"- Default Branch: {branch}")
            lines.append(f"- Updated At: {updated}")
            lines.append(f"- Folders: {folder_count}")
            lines.append(f"- Files: {file_count}")
            lines.append("")

        if repo_data.get("fetch_error"):
            lines.append("```text")
            lines.append("[Could not fetch tree]")
            lines.append("```")
            lines.append("")
            continue

        tree_lines = render_tree_lines(
            repo_data["nested_tree"],
            prefix="",
            current_depth=1,
            max_depth=max_depth,
            emojis_enabled=emojis_enabled,
        )

        lines.append("```text")
        lines.append(repo["name"])
        for item in tree_lines:
            lines.append(item)
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def build_json_report(
    username: str,
    prepared_repos: List[Dict],
    selected_mode: str,
    token_used: bool,
    max_depth: int,
    emojis_enabled: bool,
    include_metadata: bool,
) -> str:
    payload = {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "generated_at": get_iso_now(),
        "username": username,
        "mode": selected_mode,
        "token_used": token_used,
        "max_depth": max_depth,
        "emojis_enabled": emojis_enabled,
        "include_metadata": include_metadata,
        "repositories": [],
    }

    for repo_data in prepared_repos:
        repo = repo_data["repo"]
        payload["repositories"].append({
            "name": repo.get("name"),
            "description": repo.get("description"),
            "language": repo.get("language"),
            "stargazers_count": repo.get("stargazers_count"),
            "default_branch": repo.get("default_branch"),
            "updated_at": repo.get("updated_at"),
            "folder_count": repo_data.get("folder_count", 0),
            "file_count": repo_data.get("file_count", 0),
            "fetch_error": repo_data.get("fetch_error", False),
            "tree": repo_data.get("nested_tree", {}),
        })

    return json.dumps(payload, indent=2, ensure_ascii=False)


def save_report(content: str, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_output_filename(username: str, output_format: str, mode: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_user = safe_filename(username)
    safe_mode = safe_filename(mode.replace(" ", "_").lower())

    extension_map = {
        "text": "txt",
        "markdown": "md",
        "json": "json",
    }

    ext = extension_map.get(output_format, "txt")
    return f"{safe_user}_{safe_mode}_{timestamp}.{ext}"


def main() -> None:
    print_banner()

    username = ask_input("👤 Enter GitHub username").strip()
    if not username:
        print("❌ Username cannot be empty.")
        sys.exit(1)

    token = get_token_from_user()
    emojis_enabled = ask_yes_no("Enable emojis", default=True)
    include_metadata = ask_yes_no("Include repo metadata", default=True)
    max_depth = get_depth_limit()
    output_format = choose_output_format()

    try:
        repos = get_repos(username, token=token)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    if not repos:
        print(f"⚠️ No repositories found for '{username}'.")
        sys.exit(0)

    repos = sorted(repos, key=lambda x: x["name"].lower())

    print(f"\n✅ Found {len(repos)} repositories.")

    mode = choose_mode()

    if mode == "selected repos":
        chosen_repos = choose_repos(repos, emojis_enabled=emojis_enabled)
    else:
        display_repo_list(repos, emojis_enabled=emojis_enabled)
        chosen_repos = repos

    print(f"\nℹ️ Preparing report for {len(chosen_repos)} repositories...")

    prepared_repos = prepare_repo_data(
        username=username,
        repos=chosen_repos,
        token=token,
        ignore_names=IGNORE_NAMES,
    )

    if output_format == "text":
        report = build_text_report(
            username=username,
            prepared_repos=prepared_repos,
            selected_mode=mode,
            token_used=bool(token),
            max_depth=max_depth,
            emojis_enabled=emojis_enabled,
            include_metadata=include_metadata,
        )
    elif output_format == "markdown":
        report = build_markdown_report(
            username=username,
            prepared_repos=prepared_repos,
            selected_mode=mode,
            token_used=bool(token),
            max_depth=max_depth,
            emojis_enabled=emojis_enabled,
            include_metadata=include_metadata,
        )
    else:
        report = build_json_report(
            username=username,
            prepared_repos=prepared_repos,
            selected_mode=mode,
            token_used=bool(token),
            max_depth=max_depth,
            emojis_enabled=emojis_enabled,
            include_metadata=include_metadata,
        )

    print("\n" + report)

    if ask_yes_no("\nDo you want to save the report to a file", default=True):
        default_name = generate_output_filename(username, output_format, mode)
        output_path = ask_input("Enter output file name", default_name)
        save_report(report, output_path)
        print(f"✅ Saved to: {output_path}")


if __name__ == "__main__":
    main()