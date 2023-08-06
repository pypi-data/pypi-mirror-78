# GLTF Helper

```glb(web images) -> glb(basis images)```

For converting gltf/glb files with embedded jpgs/pngs to glb files with embedded basisu images.

## `Features`

- [x] glb (web images) -> glb (basisu images)
- [ ] glb (web images) -> glb (ktx2 images)
- [ ] glb (basisu images) -> glb (web images)
- [ ] glb (ktx2 images) -> glb (web images)
- [x] multiple files
- [x] custom basisu compression flags
- [x] custom gltf-pipeline flags


## `Use cases`

Unity gltf pipeline:
- [GLTFUtility](https://github.com/Siccity/GLTFUtility) 
- [KTXUnity](https://github.com/atteneder/KtxUnity)

See [sample project](https://github.com/daverin/glTF-universal-tex-unity-demo) ✨

## `Blue Pill Usage`

#### Prerequisites

1) docker

#### Test
```
make docker-test
```

makefile ->  [check it](https://github.com/Beamm-Incorporated/gltf-helper/blob/master/makefile)

## `Red Pill Usage`

#### Prerequisites

 1) build basisu -> [check it](https://github.com/BinomialLLC/basis_universal#command-line-compression-tool)

 2) install gltf-pipeline -> [check it](https://github.com/CesiumGS/gltf-pipeline#getting-started)

 3) Install PyPI package
 ```
 pip install --user gltf-helper
 ```

#### Test
```
make cli-test
```
```
gltf-helper --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

  glb/gltf(web images) -> glb(basis images)

  A CLI to convert gltf/glb assets with png/jpg textures into glb assets
  with embedded basis/ktx2 textures.

  Made with typer -> [check it](https://github.com/tiangolo/typer)

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  convert     Convert a glb/gltf(web images) -> glb(basis images)
  expand-glb  Expand a glb
```
CLI readme ->  [check it](CLI_README.md)