# loguru-caplog

Сaptures loguru logging output.

Source: [Making things work with Pytest and caplog](https://loguru.readthedocs.io/en/0.4.1/resources/migration.html#making-things-work-with-pytest-and-caplog)

## Usage

```python
from loguru_caplog import loguru_caplog as caplog

# `some_func` adds two numbers, and logs a warning if the first is < 1
def test_some_func_logs_warning(caplog):
    assert some_func(-1, 3) == 2
    assert "Oh no!" in caplog.text
```
