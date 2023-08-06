from django import forms


class Form(forms.Form):

    def as_div(self):
        """Return this form rendered as HTML <tr>s -- excluding the <table></table>."""
        return self._html_output(
            normal_row="""
            <div class="muses-field">
                %(label)s
                <div class="muses-control">
                %(field)s
                </div>
                %(errors)s
                %(help_text)s
            </div>
            """,
            error_row=""""<p class="muses-help muses-is-danger">%s</p>""",
            row_ender='</div>',
            help_text_html="""<p class="muses-help muses-is-success">%s</p>""",
            errors_on_separate_row=False,
        )

    class Media:
        pass
