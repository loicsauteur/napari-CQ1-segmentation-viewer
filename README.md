# napari-CQ1-segementation-viewer

[![License BSD-3](https://img.shields.io/pypi/l/napari-CQ1-segmentation-viewer.svg?color=green)](https://github.com/loicsauteur/napari-CQ1-segmentation-viewer/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-CQ1-segmentation-viewer.svg?color=green)](https://pypi.org/project/napari-CQ1-segmentation-viewer)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-CQ1-segmentation-viewer.svg?color=green)](https://python.org)
[![tests](https://github.com/loicsauteur/napari-CQ1-segmentation-viewer/workflows/tests/badge.svg)](https://github.com/loicsauteur/napari-CQ1-segmentation-viewer/actions)
[![codecov](https://codecov.io/gh/loicsauteur/napari-CQ1-segmentation-viewer/branch/main/graph/badge.svg)](https://codecov.io/gh/loicsauteur/napari-CQ1-segmentation-viewer)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-CQ1-segmentation-viewer)](https://napari-hub.org/plugins/napari-CQ1-segmentation-viewer)

Opens CQ1 segmentations with the corresponding channel image-stacks.

Quickload CQ1 image stacks via drag and drop.

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

<!--
You can install `napari-CQ1-segmentation-viewer` via [pip]:

    pip install napari-CQ1-segmentation-viewer
-->
You can install `napari-CQ1-segmentation-viewer` from source:

Download the code.

In a terminal cd to the folder

    pip install -e .

## Usage
### Segmentation Viewer
Select a folder with the raw CQ1 TIF images (expects that the files start with a 'W' 
and at least one file ends with 'C1.tif'). **Only works with 384 well plates.**

Select a folder with the corresponding segmentation label images (expects that the files start with a 'W' 
and at least one file ends with '_nuclei.tif').

You can then choose a well ID and an available field of view (FOV).

Press the 'Load images' button to load all the available channel stacks and the segmentations.

### Quickload CQ1 series
Drag and drop a CQ1 tif file onto the drop area.

All the CQ1 channel stacks corresponding to the well ID and FOV will be loaded.

Works with stacks and single planes (no timelapse).



## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-CQ1-segmentation-viewer" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[file an issue]: https://github.com/loicsauteur/napari-CQ1-segmentation-viewer/issues
[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
