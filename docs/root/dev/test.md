# Running Tests

## Lint tests

Seizu uses pre-commit for its linting. To have the lint run automatically upon committing, you'll need to install pre-commit for the repo:

```bash
$> pre-commit install
```

If you don't have pre-commit installed, you'll need to install it first. You can do so with brew:

```bash
$> brew install pre-commit
```

## Unit tests

To run the unit tests, use the make target:

```bash
$> make test_unit
```
