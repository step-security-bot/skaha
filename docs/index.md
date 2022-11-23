A lightweight python library the Skaha Container Science Platform at CANFAR.

!!! Installation

    ```bash
    pip install skaha
    ```

!!! example

    ```python
    from skaha.session import Session

    session = Session()
    session.create(
        name="test",
        image="images.canfar.net/skaha/terminal:0.1",
        cores=2,
        ram=8,
        kind="headless",
        cmd="env",
        env={"TEST": "test"},
    )
    ```

[Get Started](client.md){: .md-button .md-button--primary } 
[Go to GitHub :fontawesome-brands-github:](https://github.com/chimefrb/skaha){: .md-button .md-button--primary }