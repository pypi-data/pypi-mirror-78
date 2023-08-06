import os

import jinja2
from markdown2 import markdown

from folder_compiler.processors import Processor


class MarkdownProcessor(Processor):
    """
    Converts the markdown to html and pass it together with possible metadata to the
    template for rendering.

    The markdown file could look like this
    ```
    title: This is a fancy title to show metadata
    ---

    # Header
    This is _some_ content.
    ```

    The template could look like this:
    ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>{% if "title" in metadata %}{{metadata['title']}}{% endif %}</title>
    </head>
    <body>
    {{ content }}
    </body>
    </html>
    ```
    """

    def __init__(self, template: jinja2.Template):
        """
        :param template: Jinja template that renders the to html compiled markdown
                        file and its metadata.
        """
        super().__init__()
        self.template = template

    def process_file(self, source, utils):
        """
        Called by the compiler
        """
        target = os.path.splitext(source)[0] + ".html"
        md_source = utils.read_source_content(source)
        md_compiled = markdown(md_source, extras=["metadata", ])
        html_output = self.template.render(content=md_compiled,
                                           metadata=md_compiled.metadata)
        utils.write_target_content(target, html_output)
        return True
