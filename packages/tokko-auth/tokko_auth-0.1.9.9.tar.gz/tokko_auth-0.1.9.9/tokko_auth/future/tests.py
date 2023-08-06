from unittest import TestCase

from tokko_auth.future.encodings import ErrorDataType


class EncodingsTestCase(TestCase):

    def test_01_error_data_type_print(self):

        edt_a = ErrorDataType(**{"message": "testing", "exception": TypeError(), "status": 500})
        edt_b = ErrorDataType(message="testing")

        self.assertEquals(f"{edt_a}", "testing - TypeError [500]")
        self.assertEquals(f"{edt_b}", "testing - Exception [-]")


class ToolsPermissionTestCase(TestCase):
    ...


class ToolsTestingTestCase(TestCase):
    ...
