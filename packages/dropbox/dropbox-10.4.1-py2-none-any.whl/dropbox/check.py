# -*- coding: utf-8 -*-
# Auto-generated by Stone, do not modify.
# @generated
# flake8: noqa
# pylint: skip-file
try:
    from . import stone_validators as bv
    from . import stone_base as bb
except (ImportError, SystemError, ValueError):
    # Catch errors raised when importing a relative module when not in a package.
    # This makes testing this file directly (outside of a package) easier.
    import stone_validators as bv
    import stone_base as bb

class EchoArg(bb.Struct):
    """
    EchoArg contains the arguments to be sent to the Dropbox servers.

    :ivar check.EchoArg.query: The string that you'd like to be echoed back to
        you.
    """

    __slots__ = [
        '_query_value',
        '_query_present',
    ]

    _has_required_fields = False

    def __init__(self,
                 query=None):
        self._query_value = None
        self._query_present = False
        if query is not None:
            self.query = query

    @property
    def query(self):
        """
        The string that you'd like to be echoed back to you.

        :rtype: str
        """
        if self._query_present:
            return self._query_value
        else:
            return u''

    @query.setter
    def query(self, val):
        val = self._query_validator.validate(val)
        self._query_value = val
        self._query_present = True

    @query.deleter
    def query(self):
        self._query_value = None
        self._query_present = False

    def _process_custom_annotations(self, annotation_type, field_path, processor):
        super(EchoArg, self)._process_custom_annotations(annotation_type, field_path, processor)

    def __repr__(self):
        return 'EchoArg(query={!r})'.format(
            self._query_value,
        )

EchoArg_validator = bv.Struct(EchoArg)

class EchoResult(bb.Struct):
    """
    EchoResult contains the result returned from the Dropbox servers.

    :ivar check.EchoResult.result: If everything worked correctly, this would be
        the same as query.
    """

    __slots__ = [
        '_result_value',
        '_result_present',
    ]

    _has_required_fields = False

    def __init__(self,
                 result=None):
        self._result_value = None
        self._result_present = False
        if result is not None:
            self.result = result

    @property
    def result(self):
        """
        If everything worked correctly, this would be the same as query.

        :rtype: str
        """
        if self._result_present:
            return self._result_value
        else:
            return u''

    @result.setter
    def result(self, val):
        val = self._result_validator.validate(val)
        self._result_value = val
        self._result_present = True

    @result.deleter
    def result(self):
        self._result_value = None
        self._result_present = False

    def _process_custom_annotations(self, annotation_type, field_path, processor):
        super(EchoResult, self)._process_custom_annotations(annotation_type, field_path, processor)

    def __repr__(self):
        return 'EchoResult(result={!r})'.format(
            self._result_value,
        )

EchoResult_validator = bv.Struct(EchoResult)

EchoArg._query_validator = bv.String()
EchoArg._all_field_names_ = set(['query'])
EchoArg._all_fields_ = [('query', EchoArg._query_validator)]

EchoResult._result_validator = bv.String()
EchoResult._all_field_names_ = set(['result'])
EchoResult._all_fields_ = [('result', EchoResult._result_validator)]

app = bb.Route(
    'app',
    1,
    False,
    EchoArg_validator,
    EchoResult_validator,
    bv.Void(),
    {'host': u'api',
     'style': u'rpc'},
)
user = bb.Route(
    'user',
    1,
    False,
    EchoArg_validator,
    EchoResult_validator,
    bv.Void(),
    {'host': u'api',
     'style': u'rpc'},
)

ROUTES = {
    'app': app,
    'user': user,
}

