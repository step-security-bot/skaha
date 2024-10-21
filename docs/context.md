# Context API

Context API allows the user to get information about the resources available to be requested for a session on the CANFAR Science Platform. This information can be used to configure the session to request the appropriate resources for your 

## Getting Reosources Information

```python title="Get context information"
from skaha.context import Context

context = Context()
context.resources()
```

```python
{
    "defaultCores": 2,
    "defaultCoresHeadless": 1,
    "availableCores": [1, 2, 4, 8, 16],
    "defaultRAM": 16,
    "defaultRAMHeadless": 4,
    "availableRAM": [1, 2, 4, 8, 16, 32, 64, 128, 192],
    "availableGPUs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...],
}
```

::: skaha.context.Context
    handler: python
    selection:
      members:
        - resources
    rendering:
      members_order: source
      show_root_heading: true
      show_source: true
      heading_level: 3