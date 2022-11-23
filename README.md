# skaha
Python Client for Skaha Container Platform in CANFAR

## Installation

```
pip install skaha
```

## Basic Usage

```python
from skaha.session import Session

session = Session()

# Create a session
id = session.create(name="<name>", image="<image>")

# Get logs
session.logs(id)

# Destroy session
session.destroy(id)
```
