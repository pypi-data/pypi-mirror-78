# minnie-config
Synced universal configuration for working with the `microns_minnie65_%` schemas with external and their attribute adapters.

## Installation

```bash
pip3 install git+https://github.com/cajal/minnie-config.git
```

## Command Line Interface (CLI)

This is only used for mounting the required `dj-stor01` (currently windows only) which for example will mount the network drive to the Z drive letter on windows while the `-s` option makes it persistent.

```bash
minfig -s --drive Z 
```

While this command

```bash
minfig -m --drive Z
```

will unmount it.

Another way of mounting without mapping to a drive letter on windows is

```bash
minfig -s
```

however this will also require the drive to be absent, like this

```bash
minfig -m
```

to unmount it and won't be visible in file explorer. You can still view the mapped drives with

```bash
net use
```

if necessary.

There are more options like including the username or password on command line, and these option descriptions are available of course with

```bash
minfig -h
```

## Usage

Before initializing the schema or a virtual module of the schema

```python
import minfig
from minfig.adapters import * # Required for the adapters to be used with locally defined tables

minfig.configure_minnie()
```

or

```python
from minfig import * # This will also import the attribute adapters into the namespace

minfig.configure_minnie()
```

To create a virtual schema with the proper attribute adapters

```python
import minfig

minnie = minfig.configure_minnie(return_virtual_module=True)
```

or a more manual version

```python
import datajoint as dj
from minfig import adapter_objects # included with wildcard imports

minnie = dj.create_virtual_module('minnie', 'microns_minnie65_01', add_objects=adapter_objects)
```
