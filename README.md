# Dash Picture Annotation

<p><img alt="Banner" src="https://repository-images.githubusercontent.com/883421149/10c3593c-2d90-4eff-a3b5-761946985243"></p>

<p align="center">
  <a href="https://github.com/cainmagi/dash-picture-annotation/releases/latest"><img alt="GitHub release (latest SemVer)" src="https://img.shields.io/github/v/release/cainmagi/dash-picture-annotation?logo=github&sort=semver&style=flat-square"></a>
  <a href="https://github.com/cainmagi/dash-picture-annotation/releases"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/cainmagi/dash-picture-annotation/total?logo=github&style=flat-square"></a>
  <a href="https://github.com/cainmagi/dash-picture-annotation/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/cainmagi/dash-picture-annotation?style=flat-square&logo=opensourceinitiative&logoColor=white"></a>
  <a href="https://pypi.org/project/dash-picture-annotation"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/dash-picture-annotation?style=flat-square&logo=pypi&logoColor=white&label=pypi"></a>
</p>
<p align="center">
  <a href="https://github.com/cainmagi/dash-picture-annotation/actions/workflows/python-package.yml"><img alt="GitHub Actions (Build)" src="https://img.shields.io/github/actions/workflow/status/cainmagi/dash-picture-annotation/python-package.yml?style=flat-square&logo=githubactions&logoColor=white&label=build"></a>
  <a href="https://github.com/cainmagi/dash-picture-annotation/actions/workflows/python-publish.yml"><img alt="GitHub Actions (Release)" src="https://img.shields.io/github/actions/workflow/status/cainmagi/dash-picture-annotation/python-publish.yml?style=flat-square&logo=githubactions&logoColor=white&label=release"></a>
</p>

Dash Picture Annotation is a Dash component library.

Dash porting version of the React project [React Picture Annotation :link:][git-react-picture-annotation]. Provide a simple annotation window for a single picture.

The following two figures compare the demos of the original React version and the ported Dash version. Since this project is just a dash component wrapper on the original React component, the performance is the same.

|   React Picture Annotation    |   Dash Picture Annotation   |
| :---------------------------: | :-------------------------: |
| ![demo-react][pic-demo-react] | ![demo-dash][pic-demo-dash] |

Compared to the original project, this project has the following special features that the original React project does not support:

1. Responsive sizing: The width of the annotator can be automatically adjusted according to the parent web element.
2. Different modes: When selecting an annotation, the modifier can be configured as an input box or a dropdown menu box.
3. Data sanitized: The data is simply sanitized. Even if a not standardized data is passed to the annotator, it still works.
4. Anti-mistakes: A threshold of the annotation size can be configured to prevent users create a tiny annotation item by mistake.
5. Disabled: A flag can be configured to make the annotator disabled.
6. Specified colors: A special color can be configured for an annotator with a specific comment. Different comments can have different colors.
7. Dynamic colors: Without specifying colors manually, a flag can enable the colors to be automatically calculated based on the hash code of the annotation comments.

Preview a quick video demo here:

https://raw.githubusercontent.com/cainmagi/dash-picture-annotation/main/display/demo.mp4

## 1. Install

Intall the **latest released version** of this package by using the PyPI source:

``` sh
python -m pip install dash-picture-annotation
```

Or use the following commands to install **the developing version** from the GitHub Source when you have already installed [Git :hammer:][tool-git], [NodeJS :hammer:][tool-nodejs], and [Yarn :hammer:][tool-yarn]:

```bash
git clone https://github.com/cainmagi/dash-picture-annotation
cd dash-picture-annotation
python -m pip install -r requirements-dev.txt
yarn install
yarn build
python -m pip install .
```

## 2. Usage

The following signature shows the basic usage of this component.

``` python
import dash_picture_annotation as dpa

dpa.DashPictureAnnotation(
    id="annotator",
    style={"height": "80vh"},
    data=default_data,  # Can be `None`
    image="/assets/test_image.svg",  # Can be `None`
    options=None,
)
```

where the `data` is typed by `dpa.Annotations`. It should be formatted like this:

```json
{
  "timestamp": 0,
  "data": [
    {
      "id": "N5fewQ",
      "mark": {
        "x": -224.45, "y": 62.76, "width": 125.53, "height": 125.53, "type": "RECT"
      },
      "comment": "has-a-type"
    },
    {
      "id": "ibJMdK",
      "mark": {
        "x": -36.15, "y": 62.76, "width": 125.53, "height": 125.53, "type": "RECT"
      },
    },
    {
      "id": "...",
      "...": "...",
    }
  ]
}
```

A full demo for a minimal example can be found [here :link:][link-demo-minimal].

A full demo for an integrated application can be found [here :link:][link-demo-usage], where the basic usages are displayed.

## 3. Documentation

To be done...

## 4. Contributing

See [CONTRIBUTING.md :book:][link-contributing]

## 5. Changelog

See [Changelog.md :book:][link-changelog]

## 6. Acknowledgements

- [Kunduin/react-picture-annotation :link:][git-react-picture-annotation]: The original React component implementation of this project.

[git-react-picture-annotation]:https://github.com/Kunduin/react-picture-annotation

[tool-git]:https://git-scm.com/downloads
[tool-nodejs]:https://nodejs.org/en/download/package-manager
[tool-yarn]:https://yarnpkg.com/getting-started/install

[pic-demo-react]:https://raw.githubusercontent.com/cainmagi/dash-picture-annotation/main/display/demo-react.png
[pic-demo-dash]:https://raw.githubusercontent.com/cainmagi/dash-picture-annotation/main/display/demo-dash.png

[link-contributing]:https://github.com/cainmagi/dash-picture-annotation/blob/main/CONTRIBUTING.md
[link-changelog]:https://github.com/cainmagi/dash-picture-annotation/blob/main/Changelog.md

[link-demo-minimal]:https://github.com/cainmagi/dash-picture-annotation/blob/main/examples/minimal.py
[link-demo-usage]:https://github.com/cainmagi/dash-picture-annotation/blob/main/usage.py
