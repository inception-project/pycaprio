# List of formats

Documents, annotations and exports can be downloaded/created in different formats.

INCEpTION doesn't specify in their documentation which formats are supported, but the following have been found and included in `pycaprio`:

* `bin`: UIMA binary CAS
* `bioc`: BioC XML
* `conll2000`: CoNLL 2000
* `conll2002`: CoNLL 2002
* `conll2003`: CoNLL 2003
* `conll2006`: CoNLL 2006
* `conll2009`: CoNLL 2009
* `conll2012`: CoNLL 2012
* `conllcorenlp`: CoNLL CoreNLP
* `conllu`: CoNLL-U
* `ctsv`: WebAnno TSV v2
* `ctsv3`: WebAnno TSV v3.3
* `dkpro-core-tei`: TEI P5 XML (legacy)
* `dkpro-core-uima-inline-xml`: Inline XML
* `dkpro-core-xml-document`: XML (generic)
* `docx`: DOCX
* `html`: HTML (legacy)
* `htmldoc`: HTML
* `htmldoc-zip`: HTML (ZIP)
* `imscwb`: Corpus Workbench Format (aka VRT)
* `json`: UIMA CAS JSON (legacy)
* `jsoncas`: UIMA CAS JSON 0.4.0
* `jsoncas-struct`: UIMA CAS JSON 0.4.0 (XML/PDF structure)
* `lif`: LAPPS Interchange Format (LIF)
* `mhtml`: MHTML (Web archive)
* `nif`: NLP Interchange Format (NIF)
* `pdf2`: PDF
* `pdf2JsonCas`: PDF (with embedded JSON CAS)
* `pdf2XmiCas`: PDF (with embedded XMI CAS)
* `perseus_2.1`: Perseus treebank XML 2.1
* `pubannotation-annotations`: PubAnnotation Document with Annotations (JSON)
* `pubannotation-sections`: PubAnnotation Document with Sections (JSON)
* `rdfcas`: UIMA CAS RDF
* `tcf`: WebLicht TCF
* `text`: Plain text (**DEFAULT**)
* `textlines`: Plain text (one sentence per line)
* `pretokenized-textlines`: Plain text (space-separated tokens, one sentence per line)
* `tsv`: WebAnno TSV v1
* `xmi`: UIMA CAS XMI (XML 1.0)
* `xmi-struct`: UIMA CAS XMI (XML 1.0 + XML/PDF structure)
* `xmi-xml1.1`: UIMA CAS XMI (XML 1.1)


You can find a class with all the formats in `pycaprio.core.mappings.InceptionFormat`:

```python
from pycaprio.core.mappings import InceptionFormat

InceptionFormat.DEFAULT # Defaults to `text`
InceptionFormat.TEI
...
```
