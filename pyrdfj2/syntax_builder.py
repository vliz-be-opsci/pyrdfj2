import logging

from jinja2 import Environment, FileSystemLoader, meta

from pyrdfj2.exceptions import NoTemplateFolder
from pyrdfj2.j2_functions import Filters, Functions
from pyrdfj2.pyrdfj2 import RDFSyntaxBuilder

log = logging.getLogger(__name__)


class J2RDFSyntaxBuilder(RDFSyntaxBuilder):
    """
    Generic class to perform templated SPARQL searches versus a given SPARQL
        endpoint.

    :param templates_folder: location of the folder containing the jinja2
        templates
    :param extra_filters: jinja2 custom filters to apply on templates.
    :param extra_functions: jinja2 custom functions to apply on templates.
    """

    def __init__(
        self,
        templates_folder: str = "",
        extra_filters={},
        extra_functions={},
        jinja_env_variables={},
    ):
        if not templates_folder:
            raise NoTemplateFolder
        self._templates_env = Environment(
            loader=FileSystemLoader(templates_folder), **jinja_env_variables
        )

        filters: dict = Filters.all()
        functions: dict = Functions.all()
        if extra_filters:
            filters.update(extra_filters)
        if extra_functions:
            functions.update(extra_functions)
        self._templates_env.filters.update(filters)
        self._templates_env.globals.update(functions)

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
