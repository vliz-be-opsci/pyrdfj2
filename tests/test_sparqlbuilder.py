import pytest
from jinja2 import Template
from util4tests import log, run_single_test

from pyrdfj2.sparqlbuilder import J2RDFSyntaxBuilder
from tests.const import (
    ALL_QUERY,
    N,
    simple_template,
    sparql_templates_list,
    template_variables,
)

j2sqb = J2RDFSyntaxBuilder()


def test_get_rdfsyntax_template():
    qry = j2sqb._get_rdfsyntax_template(simple_template)
    assert isinstance(qry, Template)


def test_build_syntax():
    qry = j2sqb.build_syntax(simple_template, N=N)
    assert qry is not None, "result qry should exist"
    log.debug(f"qry={qry}")
    log.debug(f"expected={ALL_QUERY}")
    assert qry == ALL_QUERY, "unexpected qry result"


@pytest.mark.parametrize(
    "name",
    sparql_templates_list,
)
def test_get_variables_sparql_template(name):
    j2sqb = J2RDFSyntaxBuilder()
    variables = j2sqb.variables_in_template(name=name)
    log.info(f"all variables {variables}")
    assert (
        variables == template_variables[name]
    ), f"unexpected variables in {name}"


if __name__ == "__main__":
    run_single_test(__file__)
