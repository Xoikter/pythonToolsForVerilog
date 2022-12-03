import re
from sim_tools import simTools as st
import os
import sys
import time
from threading import Thread
import subprocess

st = st()
st.build_opts = [

]
st.sim_opts = [

]
for item in test_list:
    st.add_test(item) 


