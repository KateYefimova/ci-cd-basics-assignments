# Cache measurements

Cache: `actions/cache` for `~/.cache/pip` (key `pip-<os>-<hash of requirements*.txt>`) and Docker layer cache (`type=gha`, `mode=max`).

| run | pip install step | build-and-push step | total |
|-----|------------------|---------------------|-------|
| cold | __ s | __ s | __ s |
| warm | __ s | __ s | __ s |

