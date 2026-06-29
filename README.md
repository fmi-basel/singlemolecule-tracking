# Single-molecule tracking

This package is a compilation of tasks revolving around single molecule tracking in diverse iPSC-derived cell types. It involves image restoration with denoising, cell mask generation, spot detection, tracking and distance feature extractions.

## Installation

The base dependencies for this project are managed with pixi. Please install pixi into infrastructure/apps/pixi by executing:

```shell
export PIXI_HOME="$(pwd)/infrastructure/apps/pixi"
export PIXI_NO_PATH_UPDATE=1
export TMP_DIR="$(pwd)/infrastructure/.tmp_$USER"
mkdir -p "$TMP_DIR"
curl -fsSL https://pixi.sh/install.sh | bash
```

and initialize your shell accordingly (see below). For detailed installation instructions visit pixi.sh.

### Linux

For Linux systems an installation script is provided, which will download and install pixi into the correct location and configure PIXI_CACHE_DIR and TMPDIR environment variables. To run the installation script, execute the following command in your shell from the root of the project:


```shell
sh ./install.sh
```

## Initialization

Everytime you open a new shell you need to initialize it with the correct environment variables. You can do this by sourcing the init.sh from the root of the project:

```shell
source init.sh
```

## Execution

For Intel Macs, run the code from the main branch, for Apple Silicon Macs run the code from the osxarm64 branch.

To see detailed documentation on the available tasks and how to execute them run:
```shell
pixi run show_docs
```
and open the link.
