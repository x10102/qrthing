from typing import cast
from flask_babel import lazy_gettext as _lazy

# LazyString doesn't actually subclass str, which means Pylance will spam me with errors
# about type incompatibility all the time, unless I do this ugly thing
def _l(text: str) -> str:
    return cast(str, _lazy(text))