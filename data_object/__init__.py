from .entity import *
from .fact import *
from .mention import *
from .page import *
from .paragraph import *
from .sentence import *
from .concept import *
from .relation import *
from .dataset import *

from client import MongoDB

MongoDB.connect()
