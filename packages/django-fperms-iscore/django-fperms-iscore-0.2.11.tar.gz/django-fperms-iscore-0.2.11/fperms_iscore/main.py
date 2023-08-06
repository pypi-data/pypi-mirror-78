from is_core.main import UIRESTModelISCore

from fperms_iscore.mixins import PermISCoreMixin


class PermUIRESTModelISCore(PermISCoreMixin, UIRESTModelISCore):

    abstract = True
