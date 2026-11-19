# Cache measurements

Cache: `actions/cache` for `~/.cache/pip` (key `pip-<os>-<hash of requirements*.txt>`) and Docker layer cache (`type=gha`, `mode=max`).

| run | pip install step | build-and-push step | total |
|-----|------------------|---------------------|-------|
| cold (`Cache not found`) | 6 s | 28s | 1m 19 s |
| warm (`Cache restored successfully`) | 5 s | 8s | 31s |

pip barely got faster (6 s -> 5 s) because the dependencies are small; the real saving is in Docker: on the warm run all 8 layer steps were `CACHED`, the cache manifest was imported in 0.5 s and nothing was rebuilt.