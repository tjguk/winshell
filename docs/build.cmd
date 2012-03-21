IF NOT EXIST _static mkdir _static
python -c "import sphinx; sphinx.main ([None, '-b', 'html', '.', '.\_build'])"
pause