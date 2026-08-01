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

## What downloads return

The download methods — `client.api.document()`, `client.api.annotation()` and
`client.api.curation()` — all return the response body as raw `bytes`. Pycaprio does not
inspect or unwrap that payload, so **what those bytes actually contain depends on the
format you requested**:

* **A single file.** Most formats produce one file, and the returned bytes are that file's
  content directly. For text-based formats such as `text`, `ctsv3` or `xmi` this is a
  UTF-8 encoded string you can `.decode()`; for formats such as `bin`, `pdf2` or `docx` it
  is binary data.
* **A ZIP archive.** Some formats need to emit more than one file — for example UIMA CAS
  XMI, which ships the annotations as `.xmi` alongside the type system as `TypeSystem.xml`.
  In those cases INCEpTION returns a ZIP archive, and the returned bytes are the archive
  rather than the annotation file itself.

Nothing in the response says which case you got, and INCEpTION may change a format's
packaging between versions — so sniff the payload rather than hard-coding a list of formats.
A ZIP archive always starts with the magic bytes `PK\x03\x04`:

```python
import io
import zipfile

from pycaprio.mappings import InceptionFormat

content = client.api.annotation(1, 4, 'test-user', annotation_format=InceptionFormat.UIMA_CAS_XMI)

if content.startswith(b'PK\x03\x04'):
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        names = archive.namelist()  # e.g. ['test-user.xmi', 'TypeSystem.xml']
        xmi = archive.read(next(n for n in names if n.endswith('.xmi')))
else:
    xmi = content
```

Prefer the prefix check over `zipfile.is_zipfile()`: the latter seeks to the end of the
stream to locate the central directory and leaves the position there, so a buffer it has
already inspected cannot be handed straight to `ZipFile` without rewinding.

`client.api.export_project()` also returns `bytes`, but it is not ambiguous in this way — a
project export is always a ZIP archive regardless of the format requested, so it needs no
sniffing. See [Export project](projects.md#export-project).

Note that this matters when you feed a download straight back into an upload: the upload
methods expect the *inner* file, not the ZIP archive, so an XMI round-trip has to unzip in
between. See [Upload curation](curations.md#upload-curation) for a worked example.
