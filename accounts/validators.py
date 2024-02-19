import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r"^[a-zA-Z]+\/(...)\/(....)"
    message = _(
        "Introduzca un nombre de usuario válido. Este valor sólo puede contener letras inglesas, "
        "números y caracteres @/./+/-/_."
    )
    flags = re.ASCII
