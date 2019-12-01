DATE_FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%S%z"
NO_PROJECT = -1
NO_DOCUMENT = -1


class InceptionFormat:
    DEFAULT = 'text'

    BIN = 'bin'
    CONLL2000 = 'conll2000'
    CONLL2006 = 'conll2006'
    CONLL2009 = 'conll2009'
    CONLLCORENLP = 'conllcorenlp'
    CONLLU = 'conllu'
    CTSV = 'ctsv'
    CTSV3 = 'ctsv3'
    DKPRO_CORE_TEI = 'dkpro-core-tei'
    TEI = 'dkpro-core-tei'
    HTML = 'html'
    LIF = 'lif'
    NIF = 'nif'
    PDF = 'pdf'
    PERSEUS_2_1 = 'perseus_2.1'
    PUBANNOTATION_SECTIONS = 'pubannotation-sections'
    TCF = 'tcf'
    TEXT = 'text'
    TEXTLINES = 'textlines'
    TSV = 'tsv'

    XMI = 'xmi'

    PERSEUS = 'perseus_2.1'
    WEBANNO = 'tsv'
    JSON = 'json'


class AnnotationState:
    DEFAULT = 'NEW'
    NEW = 'NEW'
    LOCKED = 'LOCKED'
    IN_PROGRESS = 'IN-PROGRESS'
    COMPLETE = 'COMPLETE'


class DocumentState:
    DEFAULT = 'NEW'
    NEW = 'NEW'
    ANNOTATION_IN_PROGRESS = 'ANNOTATION-IN-PROGRESS'
    ANNOTATION_COMPLETE = 'ANNOTATION-COMPLETE'
    CURATION_IN_PROGRESS = 'CURATION-IN-PROGRESS'
    CURATION_COMPLETE = 'CURATION-COMPLETE'
