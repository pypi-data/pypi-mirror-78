# jarboto
JARVICE container environment config wrapper for boto3

# Environment configuration
The following values are mandatory:
* `JARVICE_S3_ACCESSKEY`
* `JARVICE_S3_SECRETKEY`
* `JARVICE_S3_BUCKET`

Note that the `jarboto.S3` constructor throws `jarboto.ConfigError` if one of these values is not set

The following values are optional:
* `JARVICE_S3_ENDPOINTURL` (defaults to AWS)
* `JARVICE_S3_PREFIX` (defaults to `output/`)
* `JARVICE_S3_REGION` (defaults to None)

# Usage
Typical usage pattern when looking to conditionally fetch objects either from S3 or from another source:

```python
import jarboto

try:
    buf = jarboto.S3().get(name)
except jarboto.ConfigError:

    # alternate method to fetch object follows
    # ...

except jarboto.S3Error as e:

    # actually failed to fetch object
    print(e)
```

Notes:
* Keep `S3` object if you intend to perform multiple operations in that context.
* Run `pydoc jarboto.S3` for additional help on method use.

