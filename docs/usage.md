# Usage Guide

## Run the script

```bash
python github_tree_report.py
````

## Step-by-step flow

### 1. Enter GitHub username

Example:

```text
Enter GitHub username: aakkiiff
```

### 2. Choose GitHub token

* Choose `y` if you want private repository support or higher API limits
* Choose `n` if you only want public repositories

### 3. Enable emojis

* `y` for visual output
* `n` for plain output

### 4. Include repository metadata

This includes:

* Description
* Stars
* Language
* Default branch
* Updated date
* Folder count
* File count

### 5. Set max depth

* `0` = unlimited
* `2` = show only first 2 levels
* `3` = show 3 levels

### 6. Choose output format

Options:

* Text
* Markdown
* JSON

### 7. Choose mode

#### Mode 1: All repos

Shows full report for all repositories.

#### Mode 2: Selected repos

Shows repository table first, then lets you choose repo numbers.

Examples:

```text
1,3,5
```

```text
2-6
```

```text
1,3-5,8
```

### 8. Save the report

The script can save the final output to a file.

## Setup commands

### Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
python github_tree_report.py
```

## Tips

* Use a token for private repositories
* Use markdown output for GitHub-friendly reports
* Use JSON output for automation
* Use max depth for very large repositories