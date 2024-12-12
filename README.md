# Backend shared utils

Shared utilities for MCM backend microservices, specifically for Django services

## Getting started

To use the latest 
```pip install mcm-common-utils @ git+https://bitbucket.apps.monash.edu:8443/scm/mcm/py-app-engine-common-utils.git```

For a particular tag
```pip install mcm-common-utils @ git+https://bitbucket.apps.monash.edu:8443/scm/mcm/py-app-engine-common-utils.git@{tag}```

### Prerequisites

Python 3.10+

## Contributing

- Make sure to have latest version of python library build installed on your system ```python3 -m pip install --upgrade build```
- Add required feature, bug fix etc.
- Add dependencies with version to pyproject.toml under dependencies (try to be as lenient as possible with versioning, so that maximum end users can use the library. Try not to pin versions)
- Update version in pyproject.toml according to [semver](https://semver.org/)
- Run ```python3 -m build``` to generate the distribution wheels and source builds
- Raise PR for review
- Once approved and merged, create tag for the version and push it in

## Additional documentation

- [Python packaging](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Setuptools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#)
- [Semver](https://semver.org/)

## Feedback

Where and how users can leave feedback?

- [Bitbucket](https://bitbucket.apps.monash.edu:8443/projects/MCM/repos/py-app-engine-common-utils/browse)
