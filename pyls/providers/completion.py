# Copyright 2017 Palantir Technologies, Inc.
import logging
from .base import JediProvider
from pyls.vscode import CompletionItemKind

log = logging.getLogger(__name__)


class JediCompletionProvider(JediProvider):
    """ Provide auto-complete suggestions """

    def run(self, doc_uri, position):
        definitions = self.jedi_script(doc_uri, position).completions()

        return {
            'isIncomplete': False,
            'items': [{
                'label': d.name,
                'kind': _kind(d),
                'detail': d.description or "",
                'documentation': d.docstring(),
                'sortText': sort_text(d)
            } for d in definitions]
        }


def sort_text(definition):
    """ Ensure builtins appear at the bottom.
    Description is of format <type>: <module>.<item>
    """
    if definition.in_builtin_module():
        # It's a builtin, put it last
        return 'z' + definition.name

    if definition.name.startswith("_"):
        # It's a 'hidden' func, put it next last
        return 'y' + definition.name

    # Else put it at the front
    return 'a' + definition.name


def _kind(d):
    """ Return the VSCode type """
    MAP = {
        'none': CompletionItemKind.Value,
        'type': CompletionItemKind.Class,
        'tuple': CompletionItemKind.Class,
        'dict': CompletionItemKind.Class,
        'dictionary': CompletionItemKind.Class,
        'function': CompletionItemKind.Function,
        'lambda': CompletionItemKind.Function,
        'generator': CompletionItemKind.Function,
        'class': CompletionItemKind.Class,
        'instance': CompletionItemKind.Reference,
        'method': CompletionItemKind.Method,
        'builtin': CompletionItemKind.Class,
        'builtinfunction': CompletionItemKind.Function,
        'module': CompletionItemKind.Module,
        'file': CompletionItemKind.File,
        'xrange': CompletionItemKind.Class,
        'slice': CompletionItemKind.Class,
        'traceback': CompletionItemKind.Class,
        'frame': CompletionItemKind.Class,
        'buffer': CompletionItemKind.Class,
        'dictproxy': CompletionItemKind.Class,
        'funcdef': CompletionItemKind.Function,
        'property': CompletionItemKind.Property,
        'import': CompletionItemKind.Module,
        'keyword': CompletionItemKind.Keyword,
        'constant': CompletionItemKind.Variable,
        'variable': CompletionItemKind.Variable,
        'value': CompletionItemKind.Value,
        'param': CompletionItemKind.Variable,
        'statement': CompletionItemKind.Keyword,
    }

    return MAP.get(d.type)
