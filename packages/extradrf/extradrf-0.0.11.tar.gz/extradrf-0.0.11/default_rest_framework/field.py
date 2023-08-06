from rest_framework import fields


class AllowBlankCharField(fields.CharField):

    def run_validation(self, data=fields.empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.
        # if data == '' or (self.trim_whitespace and str(data).strip() == ''):
            # no validate blank
            # if not self.allow_blank:
            #     self.fail('blank')
            # return ''
        return super().run_validation(data)
