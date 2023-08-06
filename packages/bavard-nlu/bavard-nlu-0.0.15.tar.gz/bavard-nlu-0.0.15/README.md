# bavard-nlu

## Releasing The Package

Releasing the package is automatically handled by CI, but two steps must be taken to trigger a successful release:

1. Increment the `VERSION` variable in `setup.py` to the new desired version (e.g. `VERSION="1.1.1"`)
2. Commit and tag the repo with the **exact same** value you populated the `VERSION` variable with (e.g. `git tag 1.1.1`)

CI will then release the package to pypi with that version once the commit is pushed.
