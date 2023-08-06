# ![logo](https://raw.githubusercontent.com/mar10/stressor/master/stressor/monitor/htdocs/stressor_48x48.png) stressor-ps
[![Latest Version](https://img.shields.io/pypi/v/stressor-ps.svg)](https://pypi.python.org/pypi/stressor-ps/)
[![License](https://img.shields.io/pypi/l/stressor-ps.svg)](https://github.com/mar10/stressor-ps/blob/master/LICENSE.txt)
[![StackOverflow: stressor](https://img.shields.io/badge/StackOverflow-stressor-blue.svg)](https://stackoverflow.com/questions/tagged/stressor)


> Stressor plugin that adds memory, cpu, and hardware testing functionality.

**Note:** <br>
This extension is currently mainly a proof of concept and example for
a [stressor](https://stressor.readthedocs.io/) plugin.
Only a simple `PsAlloc` activity is implemented.<br>
See also
[Writing Plugins](https://stressor.readthedocs.io/en/latest/ug_writing_plugins.html)
for details.


# Usage

This plugin adds new activities and macros that can be used in the
same way as the the [standard activities and macros](
https://stressor.readthedocs.io/en/latest/ug_reference.html).

## Activities

### `PsAlloc` Activity
Allocate and hold some memory in order to simulate RAM usage and shortage.
```yaml
sequences:
  main:
    # Allocate 1 GiB of RAM per running session
    - activity: PsAlloc
      allocate_mb: 1024
      per_session: true
```

<dl>
<dt>allocate_mb (float, mandatory)
<dd>
    Number of megabytes (1024^2 bytes) that should be allocated.
<dd>
<dt>per_session (bool, default: <i>false</i>)
<dd>
  If true, every session will alloacate the block of memory.
  Otherwise (by default), only one session will allocate.
</dd>
</dl>


## Macros

This extension does not yet implement new macros.
