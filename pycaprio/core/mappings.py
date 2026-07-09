DATE_FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%S%z"
NO_PROJECT = -1
NO_DOCUMENT = -1


class InceptionFormat:
    DEFAULT = "text"

    CONLL2000 = "conll2000"
    CONLL2002 = "conll2002"
    CONLL2003 = "conll2003"
    CONLL2006 = "conll2006"
    CONLL2009 = "conll2009"
    CONLL2012 = "conll2012"
    CONLLCORENLP = "conllcorenlp"
    CONLLU = "conllu"

    WEBANNO_TSV_1 = "tsv"
    WEBANNO_TSV_2 = "ctsv"
    WEBANNO_TSV_3 = "ctsv3"
    WEBANNO = WEBANNO_TSV_3
    TSV = WEBANNO_TSV_3

    HTML_LEGACY = "html"
    HTML = "htmldoc"
    HTML_ZIP = "htmldoc-zip"
    MHTML = "mhtml"

    DOCX = "docx"

    LIF = "lif"
    NIF = "nif"

    # INCEpTION renamed the PDF format id from "pdf" to "pdf2"; the bare "pdf" id no longer exists.
    PDF = "pdf2"
    PDF_WITH_JSON_CAS = "pdf2JsonCas"
    PDF_WITH_XMI_CAS = "pdf2XmiCas"

    PUBANNOTATION_SECTIONS = "pubannotation-sections"
    PUBANNOTATION_ANNOTATIONS = "pubannotation-annotations"
    TCF = "tcf"

    IMSCWB = "imscwb"

    PERSEUS_2_1 = "perseus_2.1"
    PERSEUS = PERSEUS_2_1

    TEXT = "text"
    TEXT_SENTENCE_PER_LINE = "textlines"
    TEXT_PRETOKENIZED_SENTENCE_PER_LINE = "pretokenized-textlines"

    DKPRO_CORE_TEI = "dkpro-core-tei"
    TEI = DKPRO_CORE_TEI

    XML_DOCUMENT = "dkpro-core-xml-document"
    INLINE_XML = "dkpro-core-uima-inline-xml"

    UIMA_CAS_BINARY = "bin"

    # Legacy UIMA CAS JSON format; deprecated in INCEpTION in favour of UIMA_CAS_JSON_0_4_0.
    UIMA_CAS_JSON_LEGACY = "json"
    UIMA_CAS_JSON = UIMA_CAS_JSON_LEGACY
    # UIMA CAS JSON 0.4.0 (see https://github.com/inception-project/pycaprio/issues/17)
    UIMA_CAS_JSON_0_4_0 = "jsoncas"
    UIMA_CAS_JSON_0_4_0_STRUCTURE = "jsoncas-struct"

    UIMA_CAS_XMI_XML_1_0 = "xmi"
    UIMA_CAS_XMI_XML_1_0_STRUCTURE = "xmi-struct"
    UIMA_CAS_XMI_XML_1_1 = "xmi-xml1.1"
    UIMA_CAS_XMI = UIMA_CAS_XMI_XML_1_0

    UIMA_CAS_RDF = "rdfcas"

    BIOC = "bioc"


class AnnotationState:
    DEFAULT = "NEW"
    NEW = "NEW"
    LOCKED = "LOCKED"
    IN_PROGRESS = "IN-PROGRESS"
    COMPLETE = "COMPLETE"


class DocumentState:
    DEFAULT = "NEW"
    NEW = "NEW"
    ANNOTATION_IN_PROGRESS = "ANNOTATION-IN-PROGRESS"
    ANNOTATION_COMPLETE = "ANNOTATION-COMPLETE"
    CURATION_IN_PROGRESS = "CURATION-IN-PROGRESS"
    CURATION_COMPLETE = "CURATION-COMPLETE"


class RoleType:
    # Project role names as used by the INCEpTION permission API. These are the *names* of the
    # PermissionLevel enum constants (the API reads them via PermissionLevel.valueOf(...) and returns
    # them via PermissionLevel.name()), NOT the enum ids ("user"/"curator"/"admin").
    # https://github.com/inception-project/inception/blob/main/inception/inception-model/src/main/java/de/tudarmstadt/ukp/clarin/webanno/model/PermissionLevel.java
    ANNOTATOR = "ANNOTATOR"
    CURATOR = "CURATOR"
    MANAGER = "MANAGER"
