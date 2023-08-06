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
    'version': '0.2.4',
    'description': '',
    'long_description': '# GLTF Helper\n\n```glb(web images) -> glb(basis images)```\n\nFor converting gltf/glb files with embedded jpgs/pngs to glb files with embedded basisu images.\n\n## `Features`\n\n- [x] glb (web images) -> glb (basisu images)\n- [ ] glb (web images) -> glb (ktx2 images)\n- [ ] glb (basisu images) -> glb (web images)\n- [ ] glb (ktx2 images) -> glb (web images)\n- [x] multiple files\n- [x] custom basisu compression flags\n\n## `Use cases`\n\nUnity gltf pipeline:\n- [GLTFUtility](https://github.com/Siccity/GLTFUtility) \n- [KTXUnity](https://github.com/atteneder/KtxUnity)\n\nSee [sample project](https://github.com/daverin/glTF-universal-tex-unity-demo) ✨\n\n## `Blue Pill Usage`\n\n#### Test\n```\nmake docker-test\n```\n\n#### Help \n\n```\nmake docker-help\n```\nmakefile ->  [check it](https://github.com/Beamm-Incorporated/gltf-helper/blob/master/makefile)\n\n## `Red Pill Usage`\n\n 1) build basisu -> [check it](https://github.com/BinomialLLC/basis_universal#command-line-compression-tool)\n\n 2) install gltf-pipeline -> [check it](https://github.com/CesiumGS/gltf-pipeline#getting-started)\n\n 3) Install PyPI package\n ```\n pip install --user gltf-helper\n ```\n\n#### Test\n```\nmake cli-test\n```\n\n#### Help \n\n```\nmake cli-help\n```\nCLI readme ->  [check it](CLI_README.md)',
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
