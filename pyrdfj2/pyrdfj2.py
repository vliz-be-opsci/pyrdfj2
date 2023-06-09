from abc import ABC, abstractmethod


class SparqlBuilder(ABC):
    @abstractmethod
    def build_sparql_query(self, name: str, **variables):
        """
        Builds the named sparql query by applying the provided params

        :param name: Name of the query.
        :param variables: Dict of all the variables given to the template to
            make the sparql query.

        :type name: str
        """
        pass  # pragma: no cover

    @abstractmethod
    def variables_in_query(self, name: str):
        """
        Return the set of all the variable names applicable to the named query

        :param name: [Name of the query.]
        :type name: str

        :return: the set of all variables applicable to the named query.
        :rtype: set

        """
        pass  # pragma: no cover
