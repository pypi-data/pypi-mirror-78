import os

import jinja2

from folder_compiler.processors import Processor
from folder_compiler.processors.utils.processor_utils import ProcessorUtils


class JinjaProcessor(Processor):
    """
    Renders a jinja template with full access to the provided jinja environment.
    """

    def __init__(self, env: jinja2.Environment):
        """
        A jinja environment for creating and rendering the template in (e.g. by using
        inheritance).
        The file will be converted to a template via 'from_string'.
        :param env: Jinja environment.
        """
        super().__init__()
        self._jinja = env

    def process_file(self, source: str, utils: ProcessorUtils):
        """
        Called by the compiler.
        """
        target = os.path.splitext(source)[0] + ".html"
        source_content = utils.read_source_content(source)
        template = self._jinja.from_string(source_content)
        html = template.render(**self._get_variables(source=source, target=target,
                                                     source_content=source_content,
                                                     utils=utils))
        utils.write_target_content(target, html)
        return True

    def _get_variables(self, source: str, target: str, source_content: str,
                       utils: ProcessorUtils):
        """
        This method can be override to extend some variable features.
        :param source: Path of source
        :param target: Path of target
        :param source_content: Content of source
        :param utils: ProcessorUtils
        :return: A dict
        """
        return dict()
