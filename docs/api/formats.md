# List of formats

Documents, annotations and exports can be downloaded/created in different formats.

INCEpTION doesn't specify in their documentation which formats are supported, but the following have been found and included in `pycaprio`:

* `webanno`: Webanno. This is the default format INCEpTION uses
* `nif`: NIF
* `lif`: LIF
* `dkpro-core-tei`: TEI
* `perseus_2.1`: Perseus
* `conllu`: Conllu
* `text`: Plain text
* `json`: Json
* `xmi`: XMI

You can find a class with all the formats in `pycaprio.core.mappings.DocumentFormats`:

```python
from pycaprio.core.mappings import DocumentFormats

DocumentFormats.DEFAULT
DocumentFormats.TEI
...
```
