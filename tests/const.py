from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEST_TEMPLATES_FOLDER = Path(__file__).parent.absolute() / "templates"

file_system_loader = FileSystemLoader(TEST_TEMPLATES_FOLDER)
templates_env = Environment(loader=file_system_loader)

sparql_templates_list = templates_env.list_templates()

template_variables = {
    "all.sparql": set({"N"}),
    "bodc-find.sparql": set({"regex", "collections", "language"}),
    "bodc-listing.sparql": set({"cc", "lang", "N"}),
    "broader-terms.sparql": set({"term", "language"}),
    "rdf-predicates-count.sparql": set(),
    "rdf-predicates.sparql": set({"regex"}),
    "rdf-types.sparql": set({"regex"}),
    "skos-broader-depth.sparql": set(),
    "skos-collection-member-count.sparql": set(),
    "skos-collection.sparql": set({"language"}),
    "term-match-in-collection.sparql": set({"term", "col_uri", "N"}),
}

simple_template = "all.sparql"

N = 723
ALL_QUERY = f"SELECT * WHERE {{ ?s ?p ?o.}} LIMIT {N}"
