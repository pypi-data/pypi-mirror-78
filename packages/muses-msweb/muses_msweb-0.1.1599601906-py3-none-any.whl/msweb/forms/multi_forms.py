from django.utils.safestring import mark_safe

from .form import Form


class MultiForm(Form):
    id_form = ""

    def __init__(self, id_form: str):
        super().__init__()
        self.id_form = id_form

    def _html_output(self,
                     normal_row,
                     error_row,
                     row_ender,
                     help_text_html,
                     errors_on_separate_row):
        output = super()._html_output(
            normal_row,
            error_row,
            row_ender,
            help_text_html,
            errors_on_separate_row)
        output2 = f"<input type='hidden' id='id_form' value='{self.id_form}'>"
        return mark_safe(output + output2)
