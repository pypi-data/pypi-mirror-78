# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Notebook generation code used to generate Jupyter notebooks from a Jinja2 template."""
from typing import Any, cast, Dict, Set
import functools

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import NotebookGenMissingDependency

from .. import __version__
from .utilities import escape_json
from azureml.automl.core.shared.exceptions import ClientException, ConfigException

try:
    import jinja2
    from jinja2 import Environment, meta
    import nbformat
    dependencies_installed = True
except ImportError:
    dependencies_installed = False


class NotebookTemplate:
    """
    Generates notebooks using a Jupyter notebook template.
    """

    def __init__(self, notebook_template: str) -> None:
        """
        Create an instance of a NotebookGenerator.

        :param notebook_template: the Jupyter notebook to use as a template, as a string
        """
        if not dependencies_installed:
            raise ConfigException._with_error(AzureMLError.create(NotebookGenMissingDependency, target="notebook_gen"))
        self.template = notebook_template

    @functools.lru_cache(maxsize=1)
    def get_arguments(self) -> Set[str]:
        """
        Retrieve the names of all the arguments needed to generate the notebook.

        :return: a list of all argument names
        """
        notebook = nbformat.reads(self.template, nbformat.current_nbformat)
        env = Environment()
        args = set()    # type: Set[str]

        # Parse the conents of each notebook cell into an AST and scan for jinja2 variables
        for cell in notebook.cells:
            source = cell.get('source')
            if source:
                parsed = env.parse(source)
                args |= meta.find_undeclared_variables(parsed)
        return args

    def generate_notebook(self, notebook_args: Dict[str, Any]) -> str:
        """
        Generate a notebook from a template using the provided arguments.

        :param notebook_args: a dictionary containing keyword arguments
        :return: a Jupyter notebook as a string
        """
        required_args = self.get_arguments()
        provided_args = set(notebook_args)
        missing_args = required_args - provided_args
        extra_args = provided_args - required_args

        if any(missing_args) or any(extra_args):
            raise ClientException.create_without_pii(
                'Mismatch between template and provided arguments. Missing arguments: {} Extra args: {}'.format(
                    missing_args, extra_args))

        # Render the notebook template using the given arguments.
        # Arguments need to be escaped since Jupyter notebooks are in JSON format.
        env = Environment(undefined=jinja2.StrictUndefined)
        template = env.from_string(self.template)
        source = template.render(**{
            k: escape_json(notebook_args[k])
            for k in notebook_args
        })

        # Tag the notebook with the SDK version used to generate it.
        node = nbformat.reads(source, nbformat.current_nbformat)
        node.metadata.automl_sdk_version = __version__

        return cast(str, nbformat.writes(node, nbformat.current_nbformat))
