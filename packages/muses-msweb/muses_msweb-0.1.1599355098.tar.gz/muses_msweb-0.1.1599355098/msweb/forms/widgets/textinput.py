from django.forms import (
    TextInput as Ti
)


class TextInput(Ti):
    template_name = "web/forms/widgets/text.html"
