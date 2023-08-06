# stressor-ps

> Stressor plugin that adds memory, cpu, and hardware testing functionality


# Usage

The whole *stressor* confiuration is stored in a single YAML file with a few
attributes and five mandatory sections.

**See also**:
See the annotated :doc:`ug_sample_stressor_yaml` for an example.


## Activities
### Common Args
All activites share these common arguments
(see also :class:`~stressor.plugins.base.ActivityBase`).


### 'PsAlloc' Activity

```yaml
sequences:
  main:
    # 'init' is the reserved name for the set-up sequence.
    - activity: PsAlloc
      allocate_mb: 1000
      per_session: true
```

allocate_mb (float, default: **)
    Check if the response has HTML format and matches an XPath expression::

        - activity: GetRequest
        url: /
        assert_html:
            "//*[@class='logo']": true

    (See also the common ``assert_match`` argument.)

per_session (bool, default: *false*)


## Macros

This extension does not implement new macros.
