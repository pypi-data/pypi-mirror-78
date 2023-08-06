import os

import jinja2

from folder_compiler.processors import Processor
from folder_compiler.processors.utils.processor_utils import ProcessorUtils


class HtmlProcessor(Processor):
    """
    Inserts content of the file into the template via the variable 'content'.
    The template could look like
    ```
    <!DOCTYPE html>
    <html lang="en">
    {{ content }}
    </html>
    ```
    but it is of course most useful if you add some navigation into the template.
    """

    def __init__(self, template: jinja2.Template):
        """
        :param template: The jinja template that gets the 'content' variable with the
            content of the file.
        """
        super().__init__()
        self.template = template

    def process_file(self, source: str, utils: ProcessorUtils):
        """
        Called by the compiler
        """
        target = os.path.splitext(source)[0] + ".html"
        content = utils.read_source_content(source)
        rendered = self.template.render(content=content)
        utils.write_target_content(target, rendered)
        return True
