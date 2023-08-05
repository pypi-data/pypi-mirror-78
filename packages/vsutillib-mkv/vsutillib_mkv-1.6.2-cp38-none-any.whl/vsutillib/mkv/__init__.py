"""VS module names"""

# MKV0001

#     MKVCommandNew,

from .classes import (
    MKVAttachment,
    MKVAttachments,
    MKVCommand,
    MKVCommandParser,
    MKVParseKey,
    SourceFile,
    SourceFiles,
    VerifyMKVCommand,
    VerifyStructure,
)
from .mkvutils import (
    convertToBashStyle,
    getMKVMerge,
    getMKVMergeVersion,
    numberOfTracksInCommand,
    resolveOverwrite,
    stripEncaseQuotes,
    unQuote,
)
