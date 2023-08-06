import os

import bibtexparser
import jinja2

from folder_compiler.processors import Processor
from folder_compiler.processors.utils.processor_utils import ProcessorUtils


class BibtexProcessor(Processor):
    """
    The bibtex processor parses a bibtex file and provides the entry via
    the list 'entries' to the jinja template.
    The values in the entries are already converted to utf-8 html.
    The authors are provided as a list.
    The extension will automatically be changed to ".html".

    A template could look like this:
    ```html
    <h1>Publications</h1>
    Here is a list of my publications:
    {% for entry in entries %}
    <p>
        {{ entry["author"]|join(", ") }}

        <br>
        <b>{{ entry["title"] }}
            {% if "url" in entry %}
            [<a href="{{entry['url']}}">URL</a>]
            {% endif %}
            {% if "doi" in entry %}
            [<a href="https://doi.org/{{entry['doi']}}">DOI</a>]
            {% endif %}
        </b><br>
        <i>
            {{ entry["year"] }}
            {% if "type" in entry %}, {{ entry["type"] }}{% endif %}
            {% if "journal" in entry %}, {{ entry["journal"] }}{% endif %}
            {% if "booktitle" in entry %}, {{ entry["booktitle"] }}{% endif %}
            {% if "volume" in entry %}, Volume: {{ entry["volume"] }}{% endif %}
            {% if "issue" in entry %}, Issue: {{ entry["issue"]}}{% endif %}
            {% if "pages" in entry %}, pp. {{ entry["pages"] }}{% endif %}
        </i>
    </p>
    {% endfor %}
    ```
    """

    def __init__(self, template: jinja2.Template, reversed=True):
        """
        :param template: The jinja template to be used.
        :param reversed: Order of the years. False to start with older publications.
        """
        super().__init__()
        self.template = template
        self.reversed = reversed

    def _clean_authors(self, authors: str):
        clean_authors = []
        for author in authors.split(" and "):
            try:
                author_name = author.split(",")[1] + " " + author.split(",")[0]
            except IndexError as e:
                author_name = author
            author_name = author_name.strip()
            clean_authors.append(author_name)
        return clean_authors

    def _clean_entry(self, entry: dict):
        clean_entry = {}
        for key, value in entry.items():
            value = value.replace('\n', ' ')
            value = value.encode('ascii', 'xmlcharrefreplace')
            value = value.decode('utf-8')
            clean_entry[key] = value.strip()
        clean_entry["author"] = self._clean_authors(clean_entry["author"])
        return clean_entry

    def _parse_bibtex(self, source, utils):
        bibtex_source = utils.read_source_content(source)
        parser = bibtexparser.bparser.BibTexParser()
        parser.customization = bibtexparser.customization.convert_to_unicode
        bibtex_db = bibtexparser.loads(bibtex_source, parser=parser)
        return bibtex_db

    def _prepare_database_for_jinja(self, bibtex_db: bibtexparser.bibdatabase) -> dict:
        entries = [self._clean_entry(entry) for entry in bibtex_db.entries]
        entries.sort(key=lambda x: x["year"], reverse=self.reversed)
        entry_years = {entry["year"] for entry in entries}
        entry_years = [year for year in entry_years]
        entry_years.sort(reverse=self.reversed)
        return {"entries": entries, "years": entry_years}

    def process_file(self, source: str, utils: ProcessorUtils):
        """
        To be called by the compiler.
        """
        target = os.path.splitext(source)[0] + ".html"
        bibtex_db = self._parse_bibtex(source, utils)
        bibtex_data = self._prepare_database_for_jinja(bibtex_db)
        utils.write_target_content(target, self.template.render(bibtex=bibtex_data))
        return True
