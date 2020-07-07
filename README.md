# paper-template

My template for LaTeX papers.

Features include:
- template for latex paper
- template for beamer poster
- easy compilation management with pyinvoke/latexmk
- automatic preparation of submission file for arXiv

## Usage

0. (Optional) create a blank project on overleaf, delete the provided tex file, and copy the
   project ID (last segment of URL).

1. Install cookiecutter.

    ```
    pip install cookiecutter
    ```

2. Render the template by following the prompts.

    ```
    cookiecutter gh:micahjsmith/paper-template
    ```

3. Install project dependencies.

    ```
    pip install -r requirements.txt
    ```
