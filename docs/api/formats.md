# List of formats

Documents, annotations and exports can be downloaded/created in different formats.

INCEpTION doesn't specify in their documentation which formats are supported, but the following have been found and included in `pycaprio`:

* `bin`: Binary.
* `conll2000`: CONLL 2000
* `conll2006`: CONLL 2006
* `conll2009`: CONLL 2009
* `conllcorenlp`: CONLL Core NLP
* `conllu`: CONLLu
* `ctsv`: CTSV
* `ctsv3`: CTSV3
* `dkpro-core-tei`: Dkpro Core TEI
* `html`: HTML
* `lif`: LIF
* `nif`: NIF
* `pdf`: PDF
* `perseus_2.1`: Perseus 2.1
* `pubannotation-sections`: Pubannotation sections
* `tcf`: TCF
* `text`: Plain text (**DEFAULT**)
* `textlines`: Text lines
* `tsv`: TSV - Webanno format


You can find a class with all the formats in `pycaprio.core.mappings.InceptionFormat`:

```python
from pycaprio.core.mappings import InceptionFormat

InceptionFormat.DEFAULT # Defaults to `text`
InceptionFormat.TEI
...
```
