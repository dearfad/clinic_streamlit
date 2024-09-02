# import streamlit as st
import json
from libs.bvcutils import read_prompt, write_prompt

init_prompt = read_prompt()
print(init_prompt)

init_prompt['info'] = 'pl'
write_prompt(init_prompt)
x = read_prompt()
print(x)
