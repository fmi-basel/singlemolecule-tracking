# gchao_singlemolecule_tracking
# Initialize Micromamba
```shell
export MAMBA_EXE="$(pwd)/infrastructure/apps/micromamba/bin/micromamba"
export MAMBA_ROOT_PREFIX="$(pwd)/infrastructure/apps/micromamba"
export MAMBA_ROOT_ENVIRONMENT="$(pwd)/infrastructure/apps/micromamba"

eval "$($MAMBA_ROOT_ENVIRONMENT/bin/micromamba shell hook -s posix)"

export PIP_CACHE_DIR="$(pwd)/infrastructure/apps/micromamba/PIP_CACHE"
```

# Create environment from yaml file
Make sure that micromamba is initialized
```shell
micromamba env create -f infrastructure/env-yamls/tracking_analysis.yaml
```
