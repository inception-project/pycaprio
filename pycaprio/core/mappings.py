DATE_FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%S%z"
NO_PROJECT = -1
NO_DOCUMENT = -1


class InceptionFormat:
    DEFAULT = "text"

    CONLL2000 = "conll2000"
    CONLL2006 = "conll2006"
    CONLL2009 = "conll2009"
    CONLLCORENLP = "conllcorenlp"
    CONLLU = "conllu"

    WEBANNO_TSV_1 = "tsv"
    WEBANNO_TSV_2 = "ctsv"
    WEBANNO_TSV_3 = "ctsv3"
    WEBANNO = WEBANNO_TSV_3
    TSV = WEBANNO_TSV_3

    HTML_LEGACY = "html"
    HTML = "htmldoc"

    LIF = "lif"
    NIF = "nif"
    PDF = "pdf"
    PUBANNOTATION_SECTIONS = "pubannotation-sections"
    TCF = "tcf"

    PERSEUS_2_1 = "perseus_2.1"
    PERSEUS = PERSEUS_2_1

    TEXT = "text"
    TEXT_SENTENCE_PER_LINE = "textlines"
    TEXT_PRETOKENIZED_SENTENCE_PER_LINE = "pretokenized-textlines"

    DKPRO_CORE_TEI = "dkpro-core-tei"
    TEI = DKPRO_CORE_TEI

    UIMA_CAS_BINARY = "bin"
    UIMA_CAS_JSON = "json"
    UIMA_CAS_XMI_XML_1_0 = "xmi"
    UIMA_CAS_XMI_XML_1_1 = "xmi-xml1.1"
    UIMA_CAS_XMI = UIMA_CAS_XMI_XML_1_0


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
    # https://github.com/inception-project/inception/blob/main/inception/inception-model/src/main/java/de/tudarmstadt/ukp/clarin/webanno/model/PermissionLevel.java
    ANNOTATOR = "ANNOTATOR"
    CURATOR = "CURATOR"
    MANAGER = "MANAGER"
