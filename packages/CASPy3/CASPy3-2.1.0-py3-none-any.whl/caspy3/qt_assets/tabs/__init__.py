import json
import sys
import pkg_resources

from .derivative import DerivativeTab
from .equations import EquationsTab
from .evaluate import EvaluateTab
from .expand import ExpandTab
from .formulas import FormulaTab
from .integral import IntegralTab
from .limit import LimitTab
from .pf import PfTab
from .shell.shell import ShellTab
from .simplify import SimplifyTab
from .summation import SummationTab
from .web import WebTab

TABS = []


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


settings_json = pkg_resources.resource_filename('caspy3', 'data/settings.json')
with open(settings_json, "r", encoding="utf8") as json_f:
    tab_file = json_f.read()
    tab_data = json.loads(tab_file)["tabs"]

for tab in list(tab_data.keys()):
    if tab_data[tab]:
        TABS.append(str_to_class(tab))
