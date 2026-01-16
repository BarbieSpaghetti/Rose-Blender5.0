# RoseBlend
A [Blender](https://blender.org) add-on for importing ROSE Online 3D assets
For Blender 5.0

## Features
* Map import (only heightmaps)[WIP]
* ROSE Mesh Import (ZMS)

## Installation
Copy the `io_rose` directory into your blender `scripts/addons` directory.

- __Ubuntu 16.04+__: `~/.config/blender/<version>/scripts/addons`
- __Windows__: `C:\Program Files\Blender Foundation\blender\[version]\script\addons`

Activate the plugin by opening blender and navigating to `Edit > settings > addons`

## Development
### Testing
- `python3 -m unittest discover tests`
