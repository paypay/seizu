# Managing Dependencies

## Python dependencies

Seizu's python dependencies are managed by pipenv. However, we're only using pipenv to manage the lockfile. After updating pipenv dependencies, please also update the requirements.txt via the make command:

```bash
$> make lock
```

## Node dependencies

Seizu's node dependencies are managed by yarn. If your system is setup to use yarn directly, you can do so. Otherwise, you can use use docker to manage the node resources:

```bash
$> make yarn <yarn-commands>
```
