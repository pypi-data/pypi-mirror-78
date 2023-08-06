"""Support for multilingual strings in oarepo invenio repository."""

import re
import traceback

from flask import Flask, current_app

from marshmallow import INCLUDE, Schema, ValidationError, validates_schema
from marshmallow.fields import Nested


class MultilingualStringPartSchemaV2(Schema):

    @validates_schema
    def validate_schema(self, data, **kwargs):
        list_data = list(data)
        for s in list_data:
            try:
                if "SUPPORTED_LANGUAGES" in current_app.config and s not in current_app.config["SUPPORTED_LANGUAGES"]:
                    raise ValidationError(s, "Wrong language name. Supported languages: %s" % current_app.config[
                        "SUPPORTED_LANGUAGES"])
                continue
            except ValidationError:
                raise
            except RuntimeError: #thrown if not in app_context
                pass
            if not re.match('^[a-z][a-z]$', s) and not re.match('^[a-z][a-z]-[a-z][a-z]$', s):
                raise ValidationError(s, "Wrong language name")
            if not isinstance((data[s]), str):
                raise ValidationError(s, "Wrong data type")


    class Meta:
        unknown = INCLUDE


def MultilingualStringV2(**kwargs):
    """Return a schema for multilingual string."""
    return Nested(MultilingualStringPartSchemaV2(), **kwargs)


__all__ = ('MultilingualStringV2',)
