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
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── github_tree_report.py
├── docs/
│   └── usage.md
├── output-samples/
│   └── sample_report.txt
├── CHANGELOG.md
└── CONTRIBUTING.md
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
python github_tree_report.py
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

See:

```text
CONTRIBUTING.md
```

## Changelog

See:

```text
CHANGELOG.md
```

## License

This project is licensed under the MIT License.

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```