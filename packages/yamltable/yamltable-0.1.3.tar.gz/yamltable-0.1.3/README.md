# YamlTable

![](https://img.shields.io/pypi/v/yamltable)
![](https://img.shields.io/pypi/pyversions/yamltable.svg)
![](https://github.com/wolfgangwazzlestrauss/yamltable/workflows/build/badge.svg)
![](https://codecov.io/gh/wolfgangwazzlestrauss/yamltable/branch/master/graph/badge.svg)
![](https://img.shields.io/badge/code%20style-black-000000.svg)
![](https://img.shields.io/github/repo-size/wolfgangwazzlestrauss/yamltable)
![](https://img.shields.io/github/license/wolfgangwazzlestrauss/yamltable)

---

**Documentation**: https://wolfgangwazzlestrauss.github.io/yamltable

**Source Code**: https://github.com/wolfgangwazzlestrauss/yamltable

---

YamlTable is a Python command line utility for working with YAML files organized
similar to a relational database table. It supports YAML files organized as a
list of dictionaries, which share key names and value types. YamlTable provides
commands for listing, searching, sorting, etc. data from the supported files.

## Supported YAML File Organizations

YamlTable works with YAML files organized as a list of dictionaries with similar
key names and value types.

```yaml
- name: awscli
  description: Amazon Web Services command line client
  website: https://aws.amazon.com/
- name: glances
  description: operating system monitoring interface
  website: https://github.com/nicolargo/glances
```

The JSON schema support is included for YAML files organized as:

```yaml
schema:
  $schema: http://json-schema.org/draft-07/schema#
  description: pipx package metadata schema
  type: object
  properties:
    name:
      type: string
      pattern: "^[\\w-]+$"
    description:
      type: string
    website:
      type: string
  required:
    - name
    - description
    - website
  additionalProperties: false
rows:
  - name: awscli
    description: Amazon Web Services command line client
    website: https://aws.amazon.com/
  - name: glances
    description: operating system monitoring interface
    website: https://github.com/nicolargo/glances
```

## Getting Started

### Installation

YamlTable can be installed for Python 3.6+ with `pipx`.

```console
pipx install yamltable
```

To reuse its library functions install with `pip`.

```console
pip install --user yamltable
```

The latest release can also be downloaded and installed from GitHub.

```console
pip install --user https://github.com/wolfgangwazzlestrauss/yamltable/releases/latest/download/yamltable-py3-none-any.whl
```

### Commands

YamlTable provides the following commands for working with YAML files:

- `list`: list dictionary key values
- `search`: search dictionaries by key and value
- `sort`: sort dictionaries by key and value
- `validate`: validate that dictionaries conform to the given JSON schema

## Contributing

Since YamlTable is in an early development phase, it is not currently open to
contributors.

## License

Licensed under the [MIT license](license.md).
