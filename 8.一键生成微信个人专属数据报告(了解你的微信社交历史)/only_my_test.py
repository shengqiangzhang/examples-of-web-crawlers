# -*- coding:utf-8 -*-

from pyecharts import Pie
from pyecharts import Map
import subprocess
from wxpy import *
from platform import system
import os
import subprocess
import shutil
from tqdm import tqdm
from pyecharts import Pie
from pyecharts import Map
from requests import get
from requests import post
from json import loads
from platform import system
import re
from tqdm import tqdm
import time

if(__name__ == '__main__'):

    ss = '大家好<span class dasdsafdsfdsfSDASD SAS ss试试</span>'
    print(re.sub(re.compile(r"<span class.*?</span>", re.S), "", ss))

    for i in tqdm(range(100)):
        time.sleep(1)