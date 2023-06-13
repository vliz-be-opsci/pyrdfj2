import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, meta

from pyrdfj2.j2_functions import Filters, Functions
from pyrdfj2.pyrdfj2 import RDFSyntaxBuilder

log = logging.getLogger(__name__)


DEFAULT_TEMPLATES_FOLDER = Path(__file__).parent.absolute() / "templates"


class J2RDFSyntaxBuilder(RDFSyntaxBuilder):
    """
    Generic class to perform templated SPARQL searches versus a given SPARQL
        endpoint.

    :param endpoint: sparql endpoint URL of the service to call upon
    :param templates_folder: location of the folder containing the sparql
        templates
    :param j2_filters: jinja2 custom filters to apply on templates.
    :param j2_functions: jinja2 custom functions to apply on templates.
    """

    def __init__(
        self,
        templates_folder: str = DEFAULT_TEMPLATES_FOLDER,
        j2_filters=Filters,
        j2_functions=Functions,
    ):
        self._templates_env = Environment(
            loader=FileSystemLoader(templates_folder)
        )
        if j2_filters:
            self._templates_env.filters.update(j2_filters.all())
        if j2_functions:
            self._templates_env.globals = j2_functions.all()

    def _get_rdfsyntax_template(self, name: str):
        """Gets the template"""
        return self._templates_env.get_template(name)

    def variables_in_template(self, name: str) -> set:
        """
        The set of variables to make this template work

        :param name: name of the template to inspect
        :returns: set of variable-names
        :rtype: set of str
        """
        template_name = name
        templates_env = self._templates_env
        log.debug(f"name template: {template_name}")
        template_source = templates_env.loader.get_source(
            templates_env, template_name
        )
        log.debug(f"template source = {template_source}")
        ast = self._templates_env.parse(*template_source)
        return meta.find_undeclared_variables(ast)

    def build_syntax(self, name: str, **variables) -> str:
        """
        Fills a named template sparql

        :param name: of the template
        :param **variables: named context parameters to apply to the template
        """
        log.debug(f"building sparql query '{name}' with variables={variables}")
        qry = self._get_rdfsyntax_template(name).render(variables)
        return qry
