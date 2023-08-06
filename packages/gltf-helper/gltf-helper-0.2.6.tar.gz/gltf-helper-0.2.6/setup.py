# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gltf_helper']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['gltf-helper = gltf_helper.main:app']}

setup_kwargs = {
    'name': 'gltf-helper',
    'version': '0.2.6',
    'description': '',
    'long_description': '# GLTF Helper\n\n```glb(web images) -> glb(basis images)```\n\nFor converting gltf/glb files with embedded jpgs/pngs to glb files with embedded basisu images.\n\n## `Features`\n\n- [x] glb (web images) -> glb (basisu images)\n- [ ] glb (web images) -> glb (ktx2 images)\n- [ ] glb (basisu images) -> glb (web images)\n- [ ] glb (ktx2 images) -> glb (web images)\n- [x] multiple files\n- [x] custom basisu compression flags\n- [x] custom gltf-pipeline flags\n\n\n## `Use cases`\n\nUnity gltf pipeline:\n- [GLTFUtility](https://github.com/Siccity/GLTFUtility) \n- [KTXUnity](https://github.com/atteneder/KtxUnity)\n\nSee [sample project](https://github.com/daverin/glTF-universal-tex-unity-demo) ✨\n\n## `Blue Pill Usage`\n\n#### Prerequisites\n\n1) docker\n\n#### Test\n```\nmake docker-test\n```\n\nmakefile ->  [check it](https://github.com/Beamm-Incorporated/gltf-helper/blob/master/makefile)\n\n## `Red Pill Usage`\n\n#### Prerequisites\n\n 1) build basisu -> [check it](https://github.com/BinomialLLC/basis_universal#command-line-compression-tool)\n\n 2) install gltf-pipeline -> [check it](https://github.com/CesiumGS/gltf-pipeline#getting-started)\n\n 3) Install PyPI package\n ```\n pip install --user gltf-helper\n ```\n\n#### Test\n```\nmake cli-test\n```\n```\ngltf-helper --help\n\nUsage: main.py [OPTIONS] COMMAND [ARGS]...\n\n  glb/gltf(web images) -> glb(basis images)\n\n  A CLI to convert gltf/glb assets with png/jpg textures into glb assets\n  with embedded basis/ktx2 textures.\n\n  Made with typer -> [check it](https://github.com/tiangolo/typer)\n\nOptions:\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n\n  --help                Show this message and exit.\n\nCommands:\n  convert     Convert a glb/gltf(web images) -> glb(basis images)\n  expand-glb  Expand a glb\n```\nCLI readme ->  [check it](CLI_README.md)',
    'author': 'Daverin Nadesan',
    'author_email': 'daverin@beamm.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
