# E2U - shared math, input and screen code for EXAM2.
# Keep with EXAM2.py. Plain ASCII, math + ti_draw.
# TABLE = course z-table method (matches key).
# EXACT = full calculator precision.
import math
import gc
try:
  import ti_draw as dr
  GR = True
except ImportError:
  GR = False
try:
  from ti_system import disp_clr
except ImportError:
  def disp_clr():
    print("\n" * 3)

def parse(s):
  for c in s.replace("sqrt", ""):
    if c not in "0123456789.+-*/() ":
      raise ValueError("Use digits, / and sqrt()")
  try:
    return float(eval(s, {"sqrt": math.sqrt}))
  except ZeroDivisionError:
    raise ValueError("Zero denominator")
  except Exception:
    raise ValueError("Not a number")

def rnd(x, d):
  m = 10 ** d
  g = -1 if x < 0 else 1
  return g * math.floor(abs(x) * m + 0.5 + 1e-9) / m

def f4(x):
  return "%.4f" % x

def f2(x):
  return "%.2f" % x

def sh(x):
  return "%.6g" % x

# ---- normal and t ----
try:
  erf = math.erf
except AttributeError:
  def erf(x):
    g = -1 if x < 0 else 1
    x = abs(x)
    if x > 6:
      return g
    t = s = x
    k = 0
    while t > 1e-16 * s:
      k += 1
      t = t * 2 * x * x / (2 * k + 1)
      s += t
    return g * 1.1283791670955126 * math.exp(-x * x) * s

def phi(z):
  return 0.5 * (1 + erf(z / 1.4142135623730951))

def tphi(z):
  z = rnd(z, 2)
  if z < -3.49:
    return 0.0
  if z > 3.49:
    return 1.0
  return rnd(phi(z), 4)

def bis(f, a, lo, hi):
  # x in [lo,hi] where increasing f(x) = a
  for i in range(48):
    m = (lo + hi) / 2
    if f(m) < a:
      lo = m
    else:
      hi = m
  return (lo + hi) / 2

def invphi(a):
  return bis(phi, a, -9.0, 9.0)

def tablez(a):
  # closest 4-place table area; a tie takes the midpoint
  z0 = rnd(invphi(a), 2)
  best = 9
  zs = []
  for i in range(-3, 4):
    z = rnd(z0 + i / 100, 2)
    d = abs(rnd(phi(z), 4) - a)
    if d < best - 1e-9:
      best = d
      zs = [z]
    elif abs(d - best) <= 1e-9:
      zs.append(z)
  return rnd(sum(zs) / len(zs), 3)

def tcdf(t, v):
  # P(T < t) for t >= 0, whole df (exact series)
  th = math.atan(t / math.sqrt(v))
  c2 = math.cos(th) ** 2
  w = 1.0
  tot = 1.0
  if v % 2:
    for k in range(1, (v - 1) // 2):
      w *= c2 * 2 * k / (2 * k + 1)
      tot += w
    a = th + (math.sin(th) * math.cos(th) * tot if v > 1 else 0)
    a = 2 * a / math.pi
  else:
    for k in range(1, v // 2):
      w *= c2 * (2 * k - 1) / (2 * k)
      tot += w
    a = math.sin(th) * tot
  return (1 + a) / 2

def invt(up, v):
  # positive t with upper-tail area up
  if v > 200:
    z = invphi(1 - up)
    return z + (z ** 3 + z) / (4 * v) + (5 * z ** 5 + 16 * z ** 3 + 3 * z) / (96 * v * v)
  return bis(lambda t: tcdf(t, v), 1 - up, 0.0, 1000.0)

TZ = {80: 1.28, 90: 1.645, 95: 1.96, 98: 2.33, 99: 2.576}

def zcrit(c):
  up = 1 - (1 - c / 100) / 2
  k = int(c + 0.5)
  if k in TZ and abs(c - k) < 1e-9:
    return TZ[k], invphi(up)
  return tablez(up), invphi(up)

# ---- input ----
def ask(label, pos=False, nonneg=False):
  while True:
    disp_clr()
    print(label)
    print("Number, a/b, or sqrt()")
    print("Blank = cancel")
    s = input("> ").strip()
    if s == "":
      raise ValueError("Cancelled")
    try:
      x = parse(s)
      if pos and x <= 0:
        raise ValueError("Must be positive")
      if nonneg and x < 0:
        raise ValueError("Cannot be negative")
      return x
    except ValueError as e:
      print(str(e))
      input("ENTER to retry")

def askp(label):
  p = ask(label + " (.66 or 66)", True)
  if p > 1:
    p /= 100
  if p >= 1:
    raise ValueError("Need 0 < p < 1")
  return p

def askc():
  c = ask("Confidence % (95 or .95)", True)
  if c < 1:
    c *= 100
  if c >= 100:
    raise ValueError("Need under 100%")
  return c

def pick(lines, n):
  disp_clr()
  for s in lines:
    print(s)
  k = input("> ").strip()
  return int(k) if k in [str(i) for i in range(1, n + 1)] else 0

# ---- screen and cards (ECON2 layout) ----
def wrap(t, w=28):
  out = []
  line = ""
  for word in t.split():
    if len(word) > w:
      word = word[:w]
    if line and len(line) + len(word) + 1 > w:
      out.append(line)
      line = word
    else:
      line = word if not line else line + " " + word
  if line:
    out.append(line)
  return out

def ink(c):
  dr.set_color(c[0], c[1], c[2])

NAVY = (10, 65, 100)
COLS = [(10, 65, 100), (0, 105, 75), (150, 75, 0), (130, 35, 110),
        (165, 35, 45), (55, 60, 135), (0, 110, 130), (110, 85, 20)]
ACC = [NAVY]

def tint(c):
  return (c[0] + (255 - c[0]) * 7 // 8, c[1] + (255 - c[1]) * 7 // 8, c[2] + (255 - c[2]) * 7 // 8)

def box(x, y, w, h):
  try:
    dr.fill_rect(x, y, w, h)
  except Exception:
    pass

def frame(title, tag, i=0, n=0):
  a = ACC[0]
  dr.clear()
  dr.set_pen("thin", "solid")
  ink(tint(a))
  box(0, 0, 320, 24)
  ink(a)
  dr.draw_text(8, 5, title)
  box(0, 24, 320, 2)
  if n > 1:
    ink((205, 210, 215))
    box(0, 26, 320, 3)
    ink(a)
    box(0, 26, 320 * i // n, 3)
  ink((232, 235, 238))
  box(0, 188, 320, 22)
  ink((70, 70, 70))
  dr.draw_text(8, 192, tag)

def mk(title, body, fr=None):
  # card = (title, lines, fraction); overflow goes to extra pages
  flat = []
  for s in (body.split("\n") if isinstance(body, str) else body):
    if s[:1] == "!":
      flat += ["!" + w for w in wrap(s[1:], 27)]
    else:
      flat += wrap(s) if s else [""]
  room = 4 if fr else 8
  out = [(title, flat[:room], fr)]
  flat = flat[room:]
  while flat:
    out.append((title, flat[:8], None))
    flat = flat[8:]
  return out

def show(cd, i=1, n=1):
  title, lines, fr = cd
  foot = "Page %d of %d   CLEAR = nav" % (i, n) if n > 1 else "Press CLEAR"
  if GR:
    a = ACC[0]
    frame(title, foot, i, n)
    y = 35
    if fr:
      ink(tint(a))
      box(4, 31, 312, 74)
      ink(a)
      dr.draw_text(10, 33, fr[0] + " =")
      ink((25, 25, 25))
      dr.draw_text(24, 52, fr[1])
      ink(a)
      dr.draw_line(20, 73, 300, 73)
      dr.draw_line(20, 74, 300, 74)
      ink((25, 25, 25))
      dr.draw_text(24, 79, fr[2])
      y = 112
    for s in lines:
      if s[:1] == "!":
        ink(tint(a))
        box(4, y - 2, 312, 19)
        ink(a)
        box(4, y - 2, 3, 19)
        ink((0, 0, 0))
        dr.draw_text(12, y, s[1:])
      else:
        ink(a if s[-1:] == ":" else (25, 25, 25))
        dr.draw_text(8, y, s)
      y += 18
    dr.show_draw()
  else:
    disp_clr()
    print("== " + title + " ==")
    if fr:
      print(fr[0] + " =")
      print("  " + fr[1])
      print(" " + "-" * 26)
      print("  " + fr[2])
    for s in lines:
      print(">> " + s[1:] if s[:1] == "!" else s)

def browse(cards):
  i = 0
  n = len(cards)
  while True:
    show(cards[i], i + 1, n)
    disp_clr()
    print("ENTER next | 1 previous")
    print("2 jump to page | 0 menu")
    c = input("> ").strip()
    if c == "0":
      return
    if c == "1":
      i = (i - 1) % n
    elif c == "2":
      try:
        j = int(input("Page 1-%d: " % n))
        if 1 <= j <= n:
          i = j - 1
      except ValueError:
        pass
    else:
      i = (i + 1) % n

def note(title, body):
  for cd in mk(title, body):
    show(cd)
    if not GR:
      input("ENTER: continue")

# ---- normal-curve graph ----
def cy(z):
  return int(160 - 118 * math.exp(-z * z / 2))

def graph(k, za, zb, label):
  # k: 1 below, 2 above, 3 between, 4 outside
  if not GR:
    return
  disp_clr()
  if input("1 View graph; ENTER menu: ").strip() != "1":
    return
  frame("Shaded area", "CLEAR: return to menu")
  ink((150, 200, 190))
  for px in range(23, 298):
    z = (px - 160) / 38
    if (k == 1 and z <= za) or (k == 2 and z >= za) or (k == 3 and za <= z <= zb) or (k == 4 and (z <= za or z >= zb)):
      dr.draw_line(px, 160, px, cy(z))
  ink((0, 0, 0))
  dr.draw_line(20, 160, 300, 160)
  ink(ACC[0])
  for px in range(23, 296, 2):
    dr.draw_line(px, cy((px - 160) / 38), px + 2, cy((px - 158) / 38))
  ink((70, 70, 70))
  for z in ([za] if k <= 2 else [za, zb]):
    z = max(-3.6, min(3.6, z))
    x = int(160 + z * 38)
    dr.draw_line(x, 160, x, cy(z))
    s = f2(z)
    dr.draw_text(max(4, min(x - 14, 316 - 10 * len(s))), 164, s)
  ink((0, 0, 0))
  dr.draw_text(8, 171, label)
  dr.show_draw()

