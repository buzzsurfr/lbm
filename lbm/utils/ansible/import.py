import copy

import bigsuds

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory

from system.models import DeviceGroup, Device
