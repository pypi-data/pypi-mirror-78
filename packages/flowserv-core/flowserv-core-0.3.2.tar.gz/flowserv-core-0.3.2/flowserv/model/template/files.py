# This file is part of the Reproducible and Reusable Data Analysis Workflow
# Server (flowServ).
#
# Copyright (C) 2019-2020 NYU.
#
# flowServ is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Classes to maintain of workflow output file specifications."""

import flowserv.util as util


class WorkflowOutputFile(object):
    """Information about workflow output files that are accessible as resources
    for successful workflow runs. The majority of properties that are defined
    for output files are intended to be used by applications that display the
    result of workflow runs. For each output file the following information
    may be specified:

    - source: relative path the the file in the run folder
    - title: optional title for display purposes
    - caption: optional caption for display purposes
    - format: optional format information for file contents.
    - widget: optional instructions for widget used to display file contents.
    """
    def __init__(
        self, source, title=None, caption=None, format=None, widget=None
    ):
        """Initialize the object properties.

        Parameters
        ----------
        source: string
            Relative path the the file in the run folder.
        title: string, default=None
            Optional title for display purposes.
        caption: string, default=None
            Optional caption for display purposes.
        format: dict, default=None
            Optional format information for file contents.
        widget: dict, default=None
            Optional instructions for widget used to display file contents.
        """
        self.source = source
        self.title = title
        self.caption = caption
        self.format = format
        self.widget = widget

    @classmethod
    def from_dict(cls, doc, validate=True):
        """Create object instance from dictionary serialization.

        Parameters
        ----------
        doc: dict
            Dictionary serialization for a workflow output file.
        validate: bool, default=True
            Validate the serialization if True.

        Returns
        -------
        flowserv.model.template.files.WorkflowOutputFile

        Raises
        ------
        ValueError
        """
        if validate:
            # Validate the document if the respective flag is True.
            util.validate_doc(
                doc=doc,
                mandatory=['source'],
                optional=['title', 'caption', 'widget', 'format']
            )
        return cls(
            source=doc['source'],
            title=doc.get('title'),
            caption=doc.get('caption'),
            format=doc.get('format'),
            widget=doc.get('widget')
        )

    def to_dict(self):
        """Get dictionary serialization for the output file specification.

        Returns
        -------
        dict
        """
        doc = {'source': self.source}
        if self.title is not None:
            doc['title'] = self.title
        if self.caption is not None:
            doc['caption'] = self.caption
        if self.format is not None:
            doc['format'] = self.format
        if self.widget is not None:
            doc['widget'] = self.widget
        return doc
