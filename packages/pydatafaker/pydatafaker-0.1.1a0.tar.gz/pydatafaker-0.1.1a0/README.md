# pydatafaker
A python package to create fake data with relationships between tables.

## Notes for developers

Helpful reminders for PyDataFaker developers

### Create a new release

```bash
poetry version patch # see https://python-poetry.org/docs/cli/#version
poetry run pytest
poetry build
poetry publish
```

### Updating the documentation

```bash
poetry run sphinx-apidoc -f -o docs/source pydatafaker
cd docs
poetry run make html
```
