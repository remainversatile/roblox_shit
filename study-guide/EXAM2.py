# EXAM2 - MGSC 2301 Ch 6-8 helper
# Plain Python for the TI-84 Python app.
# Every answer shows TABLE (course z-table
# method) and EXACT (calculator method).
import math

TBLZ = {80: 1.28, 90: 1.645, 95: 1.96,
        98: 2.33, 99: 2.576}


def num(prompt):
  while True:
    s = input(prompt)
    try:
      return float(s)
    except:
      print("Type a number")


def pause():
  input("[enter]")


def f4(x):
  return "%.4f" % x


def f2(x):
  return "%.2f" % x


try:
  _erf = math.erf
except:
  def _erf(x):
    # Abramowitz-Stegun 7.1.26
    sg = 1
    if x < 0:
      sg = -1
      x = -x
    t = 1 / (1 + 0.3275911 * x)
    y = 1 - (((((1.061405429 * t
        - 1.453152027) * t) + 1.421413741)
        * t - 0.284496736) * t
        + 0.254829592) * t * math.exp(-x * x)
    return sg * y


def phi(z):
  # left area under standard normal
  return 0.5 * (1 + _erf(z / math.sqrt(2)))


def invphi(a):
  lo = -9.0
  hi = 9.0
  for i in range(80):
    m = (lo + hi) / 2
    if phi(m) < a:
      lo = m
    else:
      hi = m
  return (lo + hi) / 2


def r2(z):
  # z rounded the way the table reads it
  return math.floor(z * 100 + 0.5) / 100


try:
  _lg = math.lgamma
except:
  def _lg(x):
    # Lanczos log-gamma
    c = [76.18009172947146, -86.50532032941677,
         24.01409824083091, -1.231739572450155,
         0.1208650973866179e-2,
         -0.5395239384953e-5]
    y = x
    tmp = x + 5.5
    tmp -= (x + 0.5) * math.log(tmp)
    s = 1.000000000190015
    for k in c:
      y += 1
      s += k / y
    return -tmp + math.log(2.5066282746310005 * s / x)


def _betacf(a, b, x):
  qab = a + b
  qap = a + 1
  qam = a - 1
  c = 1.0
  d = 1 - qab * x / qap
  if abs(d) < 1e-30:
    d = 1e-30
  d = 1 / d
  h = d
  for m in range(1, 200):
    m2 = 2 * m
    aa = m * (b - m) * x / ((qam + m2) * (a + m2))
    d = 1 + aa * d
    if abs(d) < 1e-30:
      d = 1e-30
    c = 1 + aa / c
    if abs(c) < 1e-30:
      c = 1e-30
    d = 1 / d
    h *= d * c
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
    d = 1 + aa * d
    if abs(d) < 1e-30:
      d = 1e-30
    c = 1 + aa / c
    if abs(c) < 1e-30:
      c = 1e-30
    d = 1 / d
    de = d * c
    h *= de
    if abs(de - 1) < 1e-10:
      break
  return h


def _ibeta(a, b, x):
  if x <= 0:
    return 0.0
  if x >= 1:
    return 1.0
  bt = math.exp(_lg(a + b) - _lg(a) - _lg(b)
                + a * math.log(x) + b * math.log(1 - x))
  if x < (a + 1) / (a + b + 2):
    return bt * _betacf(a, b, x) / a
  return 1 - bt * _betacf(b, a, 1 - x) / b


def tupper(t, df):
  # area to the RIGHT of t (t >= 0)
  x = df / (df + t * t)
  return 0.5 * _ibeta(df / 2, 0.5, x)


def invt(upper, df):
  # t with this upper-tail area
  lo = 0.0
  hi = 60.0
  for i in range(70):
    m = (lo + hi) / 2
    if tupper(m, df) > upper:
      lo = m
    else:
      hi = m
  return (lo + hi) / 2


def zcrit(conf):
  # conf as a percent, e.g. 95
  ex = invphi(1 - (1 - conf / 100) / 2)
  k = int(conf + 0.5)
  if k in TBLZ and abs(conf - k) < 1e-9:
    tb = TBLZ[k]
  else:
    tb = r2(ex)
  return tb, ex


def getconf():
  c = num("Confidence % (eg 95): ")
  if c < 1:
    c = c * 100
  a = 1 - c / 100
  print("alpha =", f4(a))
  print("a/2 =", f4(a / 2), " 1-a/2 =", f4(1 - a / 2))
  return c


def r4(a):
  return math.floor(a * 10000 + 0.5) / 10000


def areas(lo_z, hi_z, kind, tbl):
  # kind: 1 below, 2 above, 3 between
  # tbl: read 4-place areas like the table
  pl = phi(lo_z)
  ph = phi(hi_z)
  if tbl:
    pl = r4(pl)
    ph = r4(ph)
  if kind == 1:
    return ph
  if kind == 2:
    return 1 - pl
  return ph - pl


def askkind():
  print("1:P(below a)  2:P(above a)")
  print("3:P(between a,b)")
  return int(num("Pick: "))


def prob_core(center, se, label, se_t=0):
  if se_t == 0:
    se_t = se
  k = askkind()
  if k == 3:
    a = num("a (lower) = ")
    b = num("b (upper) = ")
  else:
    a = num("a = ")
    b = a
  za = (a - center) / se
  zb = (b - center) / se
  ta = r2((a - center) / se_t)
  tb = r2((b - center) / se_t)
  print("-- z =", label)
  if k == 3:
    print("z(a) =", f4(za), " z(b) =", f4(zb))
  else:
    print("z =", f4(za))
  pt = areas(ta, tb, k, True)
  pe = areas(za, zb, k, False)
  if k == 3:
    print("table: z", f2(ta), "and", f2(tb))
    print("  L areas", f4(phi(ta)), f4(phi(tb)))
  else:
    print("table: z", f2(ta), "L area", f4(phi(ta)))
  print("TABLE P =", f4(pt))
  print("EXACT P =", f4(pe))
  if k == 2:
    print("(above = 1 - left area)")
  if k == 3:
    print("(subtract AREAS, not z)")
  pause()


def m_individual():
  print("ONE value x: z=(x-mu)/sigma")
  mu = num("mu = ")
  sg = num("sigma = ")
  prob_core(mu, sg, "(x-mu)/sigma")


def m_inverse():
  print("PERCENTILE -> value")
  print("Enter the LEFT area.")
  print("top 10% -> .90")
  print("bottom 20% -> .20")
  print("67.72% ABOVE x -> .3228")
  a = num("left area = ")
  if a > 1:
    a = a / 100
  print("1: find x   2: find mu")
  k = int(num("Pick: "))
  ze = invphi(a)
  zt = r2(ze)
  print("z table ~", f2(zt), " exact", f4(ze))
  print("(check table: the area closest")
  print(" to", f4(a), "is the z to use)")
  if k == 1:
    mu = num("mu = ")
    sg = num("sigma = ")
    print("x = mu + (z)(sigma)")
    print("TABLE x =", f4(mu + zt * sg))
    print("EXACT x =", f4(mu + ze * sg))
  else:
    x = num("x = ")
    sg = num("sigma = ")
    print("mu = x - (z)(sigma)")
    print("TABLE mu =", f4(x - zt * sg))
    print("EXACT mu =", f4(x - ze * sg))
  pause()


def m_xbar():
  print("SAMPLE MEAN xbar (Ch 7)")
  print("uses sigma/sqrt(n), NOT sigma")
  mu = num("mu = ")
  sg = num("sigma (population) = ")
  n = num("n = ")
  se = sg / math.sqrt(n)
  print("E(xbar) = mu =", mu)
  print("SE = sigma/sqrt(n) =", f4(se))
  if n >= 30:
    print("n>=30: approx normal (CLT)")
  else:
    print("n<30: normal ONLY if pop normal")
  prob_core(mu, se, "(xbar-mu)/SE")


def m_pbar():
  print("SAMPLE PROPORTION pbar (Ch 7)")
  print("SE uses KNOWN p, not pbar")
  p = num("population p = ")
  if p > 1:
    p = p / 100
  n = num("n = ")
  print("np =", f2(n * p), " n(1-p) =", f2(n * (1 - p)))
  if n * p >= 5 and n * (1 - p) >= 5:
    print("both >= 5: approx normal")
  else:
    print("NOT both >= 5: not normal!")
  se = math.sqrt(p * (1 - p) / n)
  print("E(pbar) = p =", p)
  print("SE =", f4(se), "(" + "%.6f" % se + ")")
  print("TABLE uses SE", f4(se) + ";")
  print("EXACT keeps all digits.")
  print("Count x given? cutoff = x/n")
  prob_core(p, se, "(pbar-p)/SE", r4(se))


def ci_print(pt, e_t, e_e, dp):
  fm = "%." + str(int(dp)) + "f"
  print("TABLE: (" + fm % (pt - e_t) + ", " + fm % (pt + e_t) + ")")
  print("EXACT: (" + fm % (pt - e_e) + ", " + fm % (pt + e_e) + ")")
  print("width = 2E. E = half width.")


def m_ci_z():
  print("CI for mu, SIGMA KNOWN -> z")
  xb = num("xbar = ")
  sg = num("sigma = ")
  n = num("n = ")
  c = getconf()
  tb, ex = zcrit(c)
  se = sg / math.sqrt(n)
  print("SE = sigma/sqrt(n) =", f4(se))
  print("z table", tb, " exact", f4(ex))
  print("E table =", f4(tb * se), " exact", f4(ex * se))
  dp = num("decimals wanted: ")
  ci_print(xb, tb * se, ex * se, dp)
  pause()


def m_ci_t():
  print("CI for mu, only s -> t")
  print("(t even if n >= 30)")
  xb = num("xbar = ")
  s = num("s = ")
  n = num("n = ")
  c = getconf()
  df = int(n - 1 + 0.5)
  up = (1 - c / 100) / 2
  te = invt(up, df)
  print("df = n-1 =", df)
  print("t-table: row df", df, "col", f4(up))
  print("t exact =", "%.3f" % te)
  tt = num("t from YOUR table (0=exact): ")
  if tt == 0:
    tt = te
  se = s / math.sqrt(n)
  print("SE = s/sqrt(n) =", f4(se))
  print("E table =", f4(tt * se), " exact", f4(te * se))
  dp = num("decimals wanted: ")
  ci_print(xb, tt * se, te * se, dp)
  pause()


def m_ci_p():
  print("CI for p: uses pbar in SE")
  print("1: I have pbar  2: I have x")
  k = int(num("Pick: "))
  if k == 2:
    x = num("x (count) = ")
    n = num("n = ")
    pb = x / n
  else:
    pb = num("pbar = ")
    if pb > 1:
      pb = pb / 100
    n = num("n = ")
  print("pbar =", f4(pb))
  print("n*pbar =", f2(n * pb), " n(1-pbar) =", f2(n * (1 - pb)))
  c = getconf()
  tb, ex = zcrit(c)
  se = math.sqrt(pb * (1 - pb) / n)
  print("SE =", f4(se))
  print("z table", tb, " exact", f4(ex))
  print("E table =", f4(tb * se), " exact", f4(ex * se))
  dp = num("decimals wanted: ")
  ci_print(pb, tb * se, ex * se, dp)
  pause()


def ceil_n(v):
  c = math.ceil(v - 1e-9)
  return int(c)


def m_n_mean():
  print("MIN n for a MEAN")
  print("n = ((z)(sigma)/E)^2, round UP")
  sg = num("sigma (or range/4) = ")
  e = num("E (margin) = ")
  c = getconf()
  tb, ex = zcrit(c)
  vt = (tb * sg / e) ** 2
  ve = (ex * sg / e) ** 2
  print("z table", tb, " exact", f4(ex))
  print("TABLE n =", f4(vt), "-> UP", ceil_n(vt))
  print("EXACT n =", f4(ve), "-> UP", ceil_n(ve))
  pause()


def m_n_prop():
  print("MIN n for a PROPORTION")
  print("no pilot -> p* = .50")
  e = num("E (decimal, 3 pts=.03) = ")
  if e >= 1:
    e = e / 100
    print("converted E to", e)
  ps = num("p* (0 = none) = ")
  if ps == 0:
    ps = 0.5
  if ps > 1:
    ps = ps / 100
  c = getconf()
  tb, ex = zcrit(c)
  vt = tb * tb * ps * (1 - ps) / (e * e)
  ve = ex * ex * ps * (1 - ps) / (e * e)
  print("z table", tb, " exact", f4(ex))
  print("TABLE n =", f4(vt), "-> UP", ceil_n(vt))
  print("EXACT n =", f4(ve), "-> UP", ceil_n(ve))
  pause()


def m_sd():
  print("STD DEV from raw data")
  print("enter values; blank to finish")
  xs = []
  while True:
    s = input("x" + str(len(xs) + 1) + " = ")
    if s == "":
      break
    try:
      xs.append(float(s))
    except:
      print("Type a number")
  n = len(xs)
  if n < 2:
    print("need 2+ values")
    pause()
    return
  m = sum(xs) / n
  ss = 0.0
  for x in xs:
    ss += (x - m) ** 2
  print("n =", n, " mean =", f4(m))
  print("sum (x-mean)^2 =", f4(ss))
  print("POP sigma (/N) =", f4(math.sqrt(ss / n)))
  print("SAMPLE s (/n-1) =", f4(math.sqrt(ss / (n - 1))))
  pause()


def m_which():
  print("WHICH FORMULA?")
  print("About: 1 one value x")
  print("2 an average  3 a proportion")
  a = int(num("Pick: "))
  if a == 1:
    print("Ch 6. z=(x-mu)/sigma")
    print("Cutoff/percentile? Use menu 2")
    print("x = mu + (z)(sigma)")
  elif a == 2:
    print("Want: 1 probability")
    print("2 interval  3 sample size")
    b = int(num("Pick: "))
    if b == 1:
      print("Ch 7. SE = sigma/sqrt(n)")
      print("z = (xbar-mu)/SE. Never t.")
    elif b == 2:
      print("sigma given? -> z (menu 5)")
      print("only s?      -> t (menu 6)")
      print("df = n - 1")
    else:
      print("n = ((z)(sigma)/E)^2, UP")
  else:
    print("Want: 1 probability")
    print("2 interval  3 sample size")
    b = int(num("Pick: "))
    if b == 1:
      print("Ch 7. p is KNOWN.")
      print("SE = sqrt(p(1-p)/n)")
    elif b == 2:
      print("Ch 8. p unknown.")
      print("SE = sqrt(pbar(1-pbar)/n)")
    else:
      print("n=z^2 p*(1-p*)/E^2, UP")
      print("no pilot: p* = .50")
  pause()


MENU = [
  ("Which formula?", m_which),
  ("Ch6 P for one x", m_individual),
  ("Ch6 percentile->x/mu", m_inverse),
  ("Ch7 P for xbar", m_xbar),
  ("Ch7 P for pbar", m_pbar),
  ("Ch8 CI mu sigma(z)", m_ci_z),
  ("Ch8 CI mu s(t)", m_ci_t),
  ("Ch8 CI p", m_ci_p),
  ("Ch8 min n mean", m_n_mean),
  ("Ch8 min n prop", m_n_prop),
  ("Std dev from data", m_sd),
]


def main():
  while True:
    print("== EXAM 2 Ch 6-8 ==")
    for i in range(len(MENU)):
      print(str(i) + ":" + MENU[i][0])
    print("q: quit")
    s = input("Pick #: ")
    if s == "q" or s == "Q":
      break
    try:
      k = int(s)
    except:
      continue
    if 0 <= k < len(MENU):
      try:
        MENU[k][1]()
      except Exception as e:
        print("Error:", e)
        pause()


main()
