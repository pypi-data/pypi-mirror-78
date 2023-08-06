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
    'version': '0.2.3',
    'description': '',
    'long_description': '# GLTF Helper\n\n```glb(web images) -> glb(basis images)```\n\n\n##\n\nAllows converting gltf/glb files with embedded jpgs/pngs to glb files with embedded basisu images.\n\n## Features\n*System*\n- [x] glb (web images) -> glb (basisu images)\n- [ ] glb (web images) -> glb (ktx2 images)\n- [ ] glb (basisu images) -> glb (web images)\n- [ ] glb (ktx2 images) -> glb (web images)\n- [x] multiple files\n- [x] custom basisu compression flags\n\n## Use cases\n\nUnity gltf pipeline:\n- [GLTFUtility](https://github.com/Siccity/GLTFUtility) \n- [KTXUnity](https://github.com/atteneder/KtxUnity)\n\nSee [sample project](https://github.com/daverin/glTF-universal-tex-unity-demo) ✨\n\n## Usage \n\n### **Blue Pill Usage**\n#\n\n\n#### Test\n```\ndocker run -t \\\n    -v $(pwd)/samples:/samples \\\n    beamm/gltf-helper convert \\\n        /samples/Avocado/avo.gltf/asset.gltf \\\n        /samples/Avocado/avo_binary.glb \\\n    -bf "-y_flip" \\\n    --tag basisutest\n```\n\n#### Help \n\n```\ndocker run -t \\\n    -v $$(pwd)/samples:/samples \\\n    beamm/gltf-helper --help\n```\n\nTIP: Checkout `makefile` for other useful commands\n\n### **Red Pill Usage**\n#\n\n 1) build basisu -> [check it](https://github.com/BinomialLLC/basis_universal#command-line-compression-tool)\n\n 2) install gltf-pipeline -> [check it](https://github.com/CesiumGS/gltf-pipeline#getting-started)\n\n ```\n pip install --user gltf-helper\n ```\n3) CLI readme ->  [check it](CLI_README.md)',
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
