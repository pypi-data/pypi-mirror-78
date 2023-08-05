# This file is part of the Reproducible and Reusable Data Analysis Workflow
# Server (flowServ).
#
# Copyright (C) 2019-2020 NYU.
#
# flowServ is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Helper methods and classes for unit test for components of the benchmark
modules.
"""

from flowserv.model.parameter.numeric import PARA_FLOAT, PARA_INT
from flowserv.model.parameter.string import PARA_STRING
from flowserv.model.template.schema import ResultColumn, ResultSchema
from flowserv.controller.base import WorkflowController

import flowserv.model.workflow.state as st


"""Result schema for the default benchmark."""
RESULT_FILE_ID = 'results.json'
BENCHMARK_SCHEMA = ResultSchema(
    result_file=RESULT_FILE_ID,
    columns=[
        ResultColumn('col1', 'col1', PARA_INT),
        ResultColumn('col2', 'col2', PARA_FLOAT),
        ResultColumn('col3', 'col3', PARA_STRING, required=False)
    ]
)


class StateEngine(WorkflowController):
    """Workflow controller for test purposes. Maintains a dictionary of run
    states. Allows to modify the state of maintained runs
    """
    def __init__(self):
        """Initialize the run index."""
        self.runs = dict()

    def cancel_run(self, run_id):
        """Request to cancel execution of the given run.

        Parameters
        ----------
        run_id: string
            Unique run identifier.
        """
        state = self.runs[run_id].cancel()
        self.runs[run_id] = state

    def configuration(self):  # pragma: no cover
        """Get a list of tuples with the names of additional configuration
        variables and their current values.

        Returns
        -------
        list((string, string))
        """
        return list()

    def error(self, run_id, messages=None):
        """Set the run with the given identifier into error state.

        Parameters
        ----------
        run_id: string
            Unique run identifier
        messages: list(string), optional
            Default error messages

        Returns
        -------
        flowserv.model.workflow.state.WorkflowState
        """
        state = self.runs[run_id].error(messages=messages)
        self.runs[run_id] = state
        return state

    def exec_workflow(self, run, template, arguments, service=None):
        """Fake execute method that returns the workflow state that the was
        provided when the object was instantiated. Ignores all given arguments.

        Parameters
        ----------
        run: flowserv.model.base.RunHandle
            Handle for the run that is being executed.
        template: flowserv.model.template.base.WorkflowTemplate
            Workflow template containing the parameterized specification and
            the parameter declarations.
        arguments: dict
            Dictionary of argument values for parameters in the template.
        service: contextlib,contextmanager, default=None
            Ignored. Included for API completeness.

        Returns
        -------
        flowserv.model.workflow.state.WorkflowState
        """
        state = st.StatePending()
        self.runs[run.run_id] = state
        return state

    def start(self, run_id):
        """Set the run with the given identifier into running state. Returns
        the modified workflow state.

        Parameters
        ----------
        run_id: string
            Unique run identifier

        Returns
        -------
        flowserv.model.workflow.state.WorkflowState
        """
        state = self.runs[run_id].start()
        self.runs[run_id] = state
        return state

    def success(self, run_id, files=None):
        """Set the default state to SUCCESS.

        Parameters
        ----------
        run_id: string
            Unique run identifier
        files: list(string), default=None
            List of created resource files (relative paths).

        Returns
        -------
        flowserv.model.workflow.state.WorkflowState
        """
        state = self.runs[run_id].success(files=files)
        self.runs[run_id] = state
        return state
