# EXAM2 - TI-84 Evo Python, MGSC 2301 Exam 2 (Ch 6-8)
# ECON2 menu/card layout. Plain ASCII, math + ti_draw.
# Send ALL of these to the calculator:
#   EXAM2 E2U E2P E2I E2Z E2C E2X  (.py)
# Helpers load only while in use, to save memory.
import sys
from E2U import *

# ---- reference cards (from E2Z, E2C, E2X) ----
# Each module has get(i) -> list of
# "Title|line\nline|label;numerator;denominator" strings.
MODS = [("E2Z", 0), ("E2Z", 1), ("E2C", 0), ("E2C", 1), ("E2C", 2), ("E2X", 0), ("E2X", 1), ("E2X", 2)]
NAMES = ["Z-score sheet", "Formula sheet", "Ch 6 normal", "Ch 7 sampling", "Ch 8 intervals",
         "Mix-ups", "Calculator / table", "Concepts / exam"]

def imp(name):
  try:
    return __import__(name)
  except ImportError:
    raise ValueError("Send " + name + ".py to the calculator too")

def free(name):
  # drop a helper module so its memory comes back
  try:
    del sys.modules[name]
  except Exception:
    pass
  gc.collect()

def run(name, fn):
  m = imp(name)
  try:
    getattr(m, fn)()
  finally:
    del m
    free(name)

def load(i):
  name, j = MODS[i]
  m = imp(name)
  raw = m.get(j)
  del m
  free(name)
  cs = []
  for r in raw:
    p = r.split("|")
    cs += mk(p[0], p[1], tuple(p[2].split(";")) if len(p) > 2 else None)
  del raw
  gc.collect()
  return cs

def refs():
  while True:
    disp_clr()
    print("--- REFERENCE CARDS ---")
    for i in range(8):
      print(str(i + 1) + " " + NAMES[i])
    print("0 Main menu")
    s = input("> ").strip()
    if s == "0":
      return
    if len(s) == 1 and s in "12345678":
      i = int(s) - 1
      cs = load(i)
      ACC[0] = COLS[i]
      try:
        browse(cs)
      finally:
        ACC[0] = NAVY
        del cs
        gc.collect()

def main():
  while True:
    disp_clr()
    print("=== EXAM2: CH 6-8 ===")
    print("1 Reference cards")
    print("2 Probability x/xbar/pbar")
    print("3 Percent -> cutoff")
    print("4 Critical z / t")
    print("5 Confidence interval")
    print("6 Minimum sample size")
    print("7 CI parts / std dev")
    print("0 Exit")
    s = input("> ").strip()
    if s == "0":
      break
    try:
      if s == "1":
        refs()
      elif s in ["2", "3", "4"]:
        run("E2P", ["prob", "cutoff", "crit"][int(s) - 2])
      elif s in ["5", "6", "7"]:
        run("E2I", ["ci", "size", "more"][int(s) - 5])
    except ValueError as e:
      disp_clr()
      print(str(e))
      input("ENTER: menu")
    except ZeroDivisionError:
      disp_clr()
      print("Undefined: zero denominator")
      input("ENTER: menu")
    except MemoryError:
      disp_clr()
      print("Out of memory. Close other")
      print("apps, then rerun EXAM2.")
      input("ENTER: menu")
    gc.collect()

main()
