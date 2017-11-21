from difflib import SequenceMatcher

class HTMLDiff(SequenceMatcher):
    def __init__(self, original, mutant):
        SequenceMatcher.__init__(self, None, original, mutant, False)

    def _build_table_inner(self, content):
        return ''.join(content).replace('<', '&lt;').replace('>', '&gt;')

    def diff_table(self):
        start = '<table><thead><tr><th>Original</th><th>Mutant</th></tr></thead><tbody>'
        end = '</tbody></table>'
        rows = []
        for tag, a1, a2, b1, b2 in self.get_opcodes():
            rows.append('<tr data-action="' + tag + '"><td><code>' + self._build_table_inner(self.a[a1:a2]) + '</code></td><td><code>' + self._build_table_inner(self.b[b1:b2]) + '</code></td></tr>')
        return start + ''.join(rows) + end
