import markdown

from ..markdown_extensions.class_wrapper import AddDivClassExtension
from .base import BaseReader


class MarkdownReader(BaseReader):
    def __init__(self, md_path):
        self.md_path = md_path

    def read_md(self):
        with open(self.md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        return md_text

    def get_context(self):
        md_file = self.read_md()
        md = markdown.Markdown(extensions=['meta', 'codehilite', AddDivClassExtension()])
        ctx = {}
        md_content = md.convert(md_file)
        if md_content:
            ctx['content'] = md_content
        md_meta = md.Meta or {}
        for k, v in md_meta.items():
            if len(v) == 1:
                md_meta[k] = v[0]
        ctx.update(md_meta)
        return ctx


    def __str__(self):
        return "Markdown Reader for Dipor"