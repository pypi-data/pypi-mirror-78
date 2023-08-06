# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Draft Services."""

from .draft import RecordDraftService, RecordDraftServiceConfig
from .draft_file import DraftFileService, DraftFileServiceConfig
from .draft_file_metadata import DraftFileMetadataService, \
    DraftFileMetadataServiceConfig

__all__ = (
    "DraftFileMetadataService",
    "DraftFileMetadataServiceConfig",
    "DraftFileService",
    "DraftFileServiceConfig",
    "RecordDraftService",
    "RecordDraftServiceConfig",
)
