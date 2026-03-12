# GitHub Utilities

An interactive Python utility for visualizing GitHub repository structures and generating structured reports.

## Features

- Interactive GitHub username input
- Optional GitHub token support
- Show all repositories or select specific repositories
- Clean repository table view
- Tree structure visualization
- File and folder icons with emoji support
- Optional repository metadata
- Depth limit support
- Export reports as:
  - Text
  - Markdown
  - JSON

## Project Structure

```text
github-utilities/
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
├── docs/
│   └── usage.md
├── output-samples/
│   └── sample_report.txt
├── tools/
│   └── github_tree_report.py
└── tests/
    └── test_placeholder.txt
```
## Requirements

* Python 3.10 or higher
* requests library

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SAYEM-16T/github-utilities.git
cd github-utilities
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python tools/github_tree_report.py
```

## What the script does

The script will ask you for:

1. GitHub username
2. Whether you want to use a GitHub token
3. Whether to enable emojis
4. Whether to include repository metadata
5. Maximum tree depth
6. Output format
7. Mode:

   * all repos
   * selected repos only

Then it will:

* fetch repositories
* show them in a table
* generate tree output
* optionally save the report to a file

## Example Use Cases

* Explore a GitHub profile
* Generate repository structure reports
* Visualize selected repositories only
* Create documentation-friendly output
* Export JSON for automation

## Output Formats

### Text

Best for terminal and plain reports.

### Markdown

Best for GitHub documentation.

### JSON

Best for automation and integrations.

## Sample Output

A sample output file is available in:

```text
output-samples/sample_report.txt
```

## Notes

* Public repositories work without a token
* Private repositories require a valid GitHub token
* Very large repositories may take longer to process
* GitHub API rate limits may apply without authentication

## Future Improvements

* HTML report export
* CSV export
* Filter repositories by stack
* Detect Docker / Terraform / Kubernetes repositories
* Support GitHub organizations
* Add CLI flags mode


## Contributing

See [`CONTRIBUTING.md`](https://github.com/SAYEM-16T/github-utilities/blob/main/CONTRIBUTING.md)

## Changelog

See [`CHANGELOG.md`](https://github.com/SAYEM-16T/github-utilities/blob/main/CHANGELOG.md)


## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/SAYEM-16T/github-utilities/blob/main/LICENSE)  file for details.```