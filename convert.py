# %%
import sys

NUM_ARG = 1
if len(sys.argv) > NUM_ARG:
    PATH_LOG = sys.argv[1]
else:
    print("""
    PATH_LOG 인자를 전달하세요.
    Ex) python convert.py PATH_LOG
    """)
    exit()


# %%
# 파일에서 추출
from pathlib import Path

OBJ_PATH_LOG = Path(PATH_LOG)

lines = []
with open(OBJ_PATH_LOG, 'r') as file:
    line = True
    while line:
        line = file.readline()
        lines.append(line)


# %%
import re

# 로그 row 파싱.
def trim_line(line):
    return re.sub(r'/s+|\n', "", line)
def split_line(line):
    return line.split("|")
def parse_line(line):
    return split_line(trim_line(line))

# %%
# 필요한 로그 추출.
OPEN_TAG, CLOSE_TAG = "<properties>", "</properties>"

def is_open(line):
    return OPEN_TAG in line

def is_close(line):
    return CLOSE_TAG in line


# %%
# 필요한 로그 추출.
properties = []

stack = None
for line in lines:
    if is_open(line):
        stack = dict()
    elif is_close(line):
        properties.append(stack)
        stack = None
    elif stack is not None:
        key, value = parse_line(line)
        stack[key] = value


# %%
# 숫자형 변환.
attributes = ['num-calls-of-query', 'execution-time-milli-seconds']
func_trans = int

for item in properties:
    for attr in attributes:
        if attr not in item:
            continue
        ex_attr = item[attr]
        item[attr] = func_trans(ex_attr)

# %%
import pickle

PATH_PICKLES = "./pickles"
OBJ_PATH_PICKLES = Path(PATH_PICKLES)

PATH_SAVE = OBJ_PATH_PICKLES / f"{OBJ_PATH_LOG.stem}.pickle"

# 객체를 파일에 저장 (직렬화)
with open(PATH_SAVE, "wb") as file:
    pickle.dump(properties, file)
print(f"다음 경로에 저장됨.\n{PATH_SAVE}")

