# Templates

Files ending in `.j2` are rendered with Jinja2. Others are copied
verbatim.

## Template: `init`

Bootstraps a new analysis repo with the minimal skeleton.

Creates:

- `README.md`
- `pyproject.toml`
- `.gitignore`
- `.pre-commit-config.yaml`
- `.markdownlint.yaml`
- `.pylintrc`
- `src/{module}/__init__.py`
- `src/{module}/cli.py`
- `src/{module}/env.py`
- `src/{module}/config.py`
- `src/{module}/schemas/config.schema.yaml`
- `src/{module}/schemas/profile.schema.yaml`
- `src/{module}/core/options.py`
- `src/{module}/core/snakemake.py`
- `src/{module}/core/wrappers.py`

## Template: `add command`

Add a subcommand to an existing command group or make standalone
command file.

Creates/modifies:

- `src/{module}/commands/{command}.py`

## Template: `add command-group`

Add the main entry point for a command to an existing file.

Modifies:

- `src/{module}/commands/{command}.py`

## Template: `add diary`

Add a diary template.

Creates:

- `docs/diary/index.qmd`
- `docs/assets/static/title-slide.html`
- `docs/assets/static/tikzfig.tex`
- `docs/assets/logos/nbis-scilifelab.svg`
- `docs/assets/css/nbis.scss`

## Template: `add running-slides`

Add running slides template.

Creates:

- `docs/running_slides/index.qmd`
- `docs/assets/static/title-slide.html`
- `docs/assets/static/tikzfig.tex`
- `docs/assets/logos/nbis-scilifelab.svg`
- `docs/assets/css/nbis.scss`

## Template: `add template`

Add one individual template from a list of choices.

Creates:

- `pyproject.toml`
- `.gitiginore`
- `.prettierignore`
- `.markdownlint.yaml`
- `.prettierrc.yml`
- `.editorconfig`
- `README.md`
- `.pre-commit-config.yaml`
- `docs/_quarto.yml`

## Template: `add tool`

Add a command line tool that can be called with `{module} tools {tool}`

Creates:

- `src/{module}/tools/{tool}.py`
- `src/{module}/commands/tools.py`

## Template: `smk init`

Initialize configuration files for Snakemake analyses.

Creates:

- `src/{module}/snakemake/config.py`
- `src/{module}/config/local/config.yaml`
- `src/{module}/config/config.yaml`
- `src/{module}/workflow/schemas/config.schema.yaml`
- `src/{module}/workflow/schemas/samples.schema.yaml`
- `resources/samples.tsv`

## Template: `smk add`

Add Snakefile and Python helper code.

Creates:

- `src/{module}/commands/{command}.py`
- `src/{module}/workflow/snakemake/commands/{command}.smk`
