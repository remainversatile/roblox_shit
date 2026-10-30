# EXAM2 - MGSC 2301 Ch 6-8 helper
# Plain Python for the TI-84 Python app.
# Every answer shows TABLE (course z-table
# method, matches the key) and EXACT
# (full calculator precision).
# Inputs accept math: 46/sqrt(85), 1-.05/2
import math

# course table critical values
TBLZ = {80: 1.28, 90: 1.645, 95: 1.96,
        98: 2.33, 99: 2.576}
ENV = {"sqrt": math.sqrt, "pi": math.pi}


# ---------- input helpers ----------

def num(prompt, pos=False):
  while True:
    s = input(prompt).strip()
    if s == "":
      continue
    try:
      v = float(eval(s, ENV))
    except:
      print("Not a number. Try again")
      continue
    if pos and v <= 0:
      print("Must be > 0")
      continue
    return v


def pick(prompt, hi):
  # menu choice 1..hi
  while True:
    v = num(prompt)
    k = int(v)
    if k == v and 1 <= k <= hi:
      return k
    print("Pick 1 to", hi)


def prop(prompt):
  # proportion; 66 or .66 -> .66
  while True:
    v = num(prompt)
    if v > 1:
      v = v / 100
    if 0 < v < 1:
      return v
    print("Need 0 < p < 1")


def pause():
  input("[enter]")


def rnd(x, d):
  # half away from zero, float-safe
  m = 10 ** d
  s = 1
  if x < 0:
    s = -1
  return s * math.floor(abs(x) * m + 0.5 + 1e-9) / m


def r2(z):
  return rnd(z, 2)


def r4(a):
  return rnd(a, 4)


def f4(x):
  return "%.4f" % x


def f2(x):
  return "%.2f" % x


def pct(p):
  return "%.2f%%" % (p * 100)


# ---------- normal distribution ----------

try:
  _erf = math.erf
except:
  def _erf(x):
    # all-positive series, full precision
    sg = 1
    if x < 0:
      sg = -1
      x = -x
    if x > 6:
      return sg * 1.0
    term = x
    s = x
    k = 0
    while term > 1e-17 * s:
      k += 1
      term = term * 2 * x * x / (2 * k + 1)
      s += term
    return sg * 2 / math.sqrt(math.pi) * math.exp(-x * x) * s


def phi(z):
  # area to the LEFT of z
  return 0.5 * (1 + _erf(z / math.sqrt(2)))


def tphi(z):
  # table reading: z to 2 places, 4-place
  # area; past +/-3.49 reads .0000/1.0000
  z = r2(z)
  if z < -3.49:
    return 0.0
  if z > 3.49:
    return 1.0
  return r4(phi(z))


def invphi(a):
  lo = -9.0
  hi = 9.0
  for i in range(55):
    m = (lo + hi) / 2
    if phi(m) < a:
      lo = m
    else:
      hi = m
  return (lo + hi) / 2


def tablez(a):
  # z whose 4-place area is closest to a;
  # a tie (like .95) takes the midpoint
  best = 9.0
  zs = []
  z0 = r2(invphi(a))
  for i in range(-3, 4):
    z = r2(z0 + i / 100)
    d = abs(r4(phi(z)) - a)
    if d < best - 1e-9:
      best = d
      zs = [z]
    elif abs(d - best) <= 1e-9:
      zs.append(z)
  return rnd(sum(zs) / len(zs), 3)


# ---------- t distribution ----------

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


def _tiny(v):
  if abs(v) < 1e-30:
    return 1e-30
  return v


def _betacf(a, b, x):
  qab = a + b
  qap = a + 1
  qam = a - 1
  c = 1.0
  d = 1 / _tiny(1 - qab * x / qap)
  h = d
  for m in range(1, 200):
    m2 = 2 * m
    aa = m * (b - m) * x / ((qam + m2) * (a + m2))
    d = 1 / _tiny(1 + aa * d)
    c = _tiny(1 + aa / c)
    h *= d * c
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
    d = 1 / _tiny(1 + aa * d)
    c = _tiny(1 + aa / c)
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
  return 0.5 * _ibeta(df / 2, 0.5, df / (df + t * t))


def invt(upper, df):
  # positive t with this upper-tail area
  lo = 0.0
  hi = 700.0
  for i in range(50):
    m = (lo + hi) / 2
    if tupper(m, df) > upper:
      lo = m
    else:
      hi = m
  return (lo + hi) / 2


# ---------- confidence helpers ----------

def getconf():
  while True:
    c = num("Confidence % (eg 95): ")
    if 0 < c < 1:
      c = c * 100
    if 0 < c < 100:
      break
    print("Need 0 to 100")
  a = 1 - c / 100
  print("alpha=" + f4(a) + " a/2=" + f4(a / 2))
  print("1-a/2=" + f4(1 - a / 2))
  return c


def zcrit(c):
  # (table z, exact z) for confidence c%
  up = 1 - (1 - c / 100) / 2
  ex = invphi(up)
  k = int(c + 0.5)
  if k in TBLZ and abs(c - k) < 1e-9:
    return TBLZ[k], ex
  return tablez(up), ex


def show_z(c):
  tb, ex = zcrit(c)
  print("z table " + str(tb) + "  exact " + f4(ex))
  return tb, ex


# ---------- probability engine ----------

def askkind():
  print("1 below a   2 above a")
  print("3 between a,b  4 outside a,b")
  print("5 within +/-d of center")
  return pick("Pick: ", 5)


def area(pa, pb, k):
  # pa, pb: left areas at a and b
  if k == 1:
    return pa
  if k == 2:
    return 1 - pa
  if k == 3:
    return pb - pa
  return 1 - (pb - pa)


def prob_core(ctr, se, se_t=0):
  # se_t: SE the table method uses
  if se_t == 0:
    se_t = se
  k = askkind()
  if k == 5:
    d = num("d (how far) = ", True)
    a = ctr - d
    b = ctr + d
    print("range " + str(rnd(a, 6)) + " to " + str(rnd(b, 6)))
    k = 3
  elif k >= 3:
    a = num("a (lower) = ")
    b = num("b (upper) = ")
    if b < a:
      a, b = b, a
  else:
    a = num("a = ")
    b = a
  za = (a - ctr) / se
  zb = (b - ctr) / se
  ta = r2((a - ctr) / se_t)
  tb = r2((b - ctr) / se_t)
  if k <= 2:
    print("z = " + f4(za) + " -> table " + f2(ta))
    print("left area " + f4(tphi(ta)))
  else:
    print("z(a)=" + f4(za) + " -> " + f2(ta))
    print("z(b)=" + f4(zb) + " -> " + f2(tb))
    print("areas " + f4(tphi(ta)) + ", " + f4(tphi(tb)))
  pt = area(tphi(ta), tphi(tb), k)
  pe = area(phi(za), phi(zb), k)
  print("TABLE P = " + f4(pt) + " (" + pct(pt) + ")")
  print("EXACT P = " + f4(pe))
  if k == 2:
    print("above = 1 - left area")
  if k >= 3:
    print("subtract AREAS, not z")
  if abs(ta) > 3.49 or abs(tb) > 3.49:
    print("z past 3.49: table edge")
  pause()


def clt(n):
  if n >= 30:
    print("n>=30: approx normal (CLT)")
  else:
    print("n<30: normal ONLY if pop is")


def phat_check(p, n):
  a = n * p
  b = n * (1 - p)
  print("np=" + f2(a) + " n(1-p)=" + f2(b))
  if a >= 5 and b >= 5:
    print("both >= 5: approx normal")
  else:
    print("NOT both >= 5: not normal!")
  se = math.sqrt(p * (1 - p) / n)
  print("SE = " + f4(se) + " (" + "%.6f" % se + ")")
  return se


def spread():
  # returns (center, se_exact, se_table)
  print("Value is about:")
  print("1 one x      2 sample mean")
  print("3 sample proportion")
  w = pick("Pick: ", 3)
  if w == 1:
    mu = num("mu = ")
    sg = num("sigma = ", True)
    return mu, sg, sg
  if w == 2:
    mu = num("mu = ")
    sg = num("sigma (population) = ", True)
    n = num("n = ", True)
    se = sg / math.sqrt(n)
    print("SE = sigma/sqrt(n) = " + f4(se))
    clt(n)
    return mu, se, se
  p = prop("population p = ")
  n = num("n = ", True)
  se = phat_check(p, n)
  return p, se, r4(se)


# ---------- menu items ----------

def m_individual():
  print("ONE value: z=(x-mu)/sigma")
  mu = num("mu = ")
  sg = num("sigma = ", True)
  prob_core(mu, sg)


def m_xbar():
  print("SAMPLE MEAN (Ch 7)")
  print("SE = sigma/sqrt(n), not sigma")
  mu = num("mu = ")
  sg = num("sigma (population) = ", True)
  n = num("n = ", True)
  se = sg / math.sqrt(n)
  print("E(xbar) = mu = " + str(mu))
  print("SE = " + f4(se))
  clt(n)
  prob_core(mu, se)


def m_pbar():
  print("SAMPLE PROPORTION (Ch 7)")
  print("SE uses KNOWN p, not pbar")
  p = prop("population p = ")
  n = num("n = ", True)
  print("E(pbar) = p = " + str(p))
  se = phat_check(p, n)
  print("TABLE uses SE " + f4(se))
  print("Count given? cutoff = x/n")
  prob_core(p, se, r4(se))


def m_inverse():
  print("PERCENT -> CUTOFF (inverse)")
  print("1 % below cutoff")
  print("2 % above cutoff (top __%)")
  print("3 middle % (two cutoffs)")
  k = pick("Pick: ", 3)
  pc = prop("percent (eg 10 or .10): ")
  if k == 1:
    lefts = [pc]
  elif k == 2:
    lefts = [1 - pc]
  else:
    lefts = [(1 - pc) / 2, 1 - (1 - pc) / 2]
  for a in lefts:
    print("LEFT " + f4(a) + " z " + str(tablez(a)) + " ex " + f4(invphi(a)))
  print("Solve for: 1 cutoff  2 mu")
  g = pick("Pick: ", 2)
  if g == 2:
    x = num("x = ")
    sg = num("sigma = ", True)
    print("mu = x - (z)(sigma)")
    for a in lefts:
      print("TABLE mu = " + f4(x - tablez(a) * sg))
      print("EXACT mu = " + f4(x - invphi(a) * sg))
    pause()
    return
  ctr, se, se_t = spread()
  print("cutoff = center + (z)(SE)")
  for a in lefts:
    print("TABLE = " + f4(ctr + tablez(a) * se_t))
    print("EXACT = " + f4(ctr + invphi(a) * se))
  pause()


def m_crit():
  print("CRITICAL PROBS & VALUES")
  c = getconf()
  show_z(c)
  n = num("n for t (0 = skip): ")
  if n >= 2:
    df = int(n - 1 + 0.5)
    up = (1 - c / 100) / 2
    print("df=" + str(df) + " upper area " + f4(up))
    print("t = +/-" + "%.3f" % invt(up, df))
  pause()


def ci_out(pt, e_t, e_e):
  dp = int(num("decimals wanted: "))
  if dp < 0 or dp > 6:
    dp = 2
  fm = "%." + str(dp) + "f"
  print("TABLE (" + fm % (pt - e_t) + ", " + fm % (pt + e_t) + ")")
  print("EXACT (" + fm % (pt - e_e) + ", " + fm % (pt + e_e) + ")")
  print("width = 2E = " + fm % (2 * e_t))
  pause()


def m_ci_z():
  print("CI for mu, SIGMA KNOWN: z")
  xb = num("xbar = ")
  sg = num("sigma = ", True)
  n = num("n = ", True)
  c = getconf()
  tb, ex = show_z(c)
  se = sg / math.sqrt(n)
  print("SE = sigma/sqrt(n) = " + f4(se))
  print("E table " + f4(tb * se) + " exact " + f4(ex * se))
  ci_out(xb, tb * se, ex * se)


def m_ci_t():
  print("CI for mu, only s: t")
  print("(t even when n >= 30)")
  xb = num("xbar = ")
  s = num("s = ", True)
  n = num("n = ", True)
  if n < 2:
    print("need n >= 2")
    pause()
    return
  c = getconf()
  df = int(n - 1 + 0.5)
  up = (1 - c / 100) / 2
  print("computing t...")
  te = invt(up, df)
  print("df = n-1 = " + str(df))
  print("t-table: row " + str(df) + ", col " + f4(up))
  print("t exact = " + "%.3f" % te)
  if n < 30:
    print("n<30: needs normal pop")
  tt = num("t from YOUR table (0=exact): ")
  if tt <= 0:
    tt = rnd(te, 3)
  se = s / math.sqrt(n)
  print("SE = s/sqrt(n) = " + f4(se))
  print("E table " + f4(tt * se) + " exact " + f4(te * se))
  ci_out(xb, tt * se, te * se)


def m_ci_p():
  print("CI for p: SE uses pbar")
  print("1 have pbar  2 have count x")
  k = pick("Pick: ", 2)
  if k == 2:
    x = num("x (count) = ")
    n = num("n = ", True)
    pb = x / n
  else:
    pb = prop("pbar = ")
    n = num("n = ", True)
  print("pbar = " + f4(pb))
  print("n*pbar=" + f2(n * pb) + " n(1-pbar)=" + f2(n * (1 - pb)))
  if n * pb < 5 or n * (1 - pb) < 5:
    print("counts < 5: not normal!")
  c = getconf()
  tb, ex = show_z(c)
  se = math.sqrt(pb * (1 - pb) / n)
  print("SE = " + f4(se))
  print("E table " + f4(tb * se) + " exact " + f4(ex * se))
  ci_out(pb, tb * se, ex * se)


def ceil_n(v):
  return int(math.ceil(v - 1e-9))


def m_n_mean():
  print("MIN n for a MEAN, round UP")
  print("1 sigma given  2 use range/4")
  k = pick("Pick: ", 2)
  if k == 2:
    rg = num("range (max-min) = ", True)
    sg = rg / 4
    print("sigma ~ " + f4(sg))
  else:
    sg = num("sigma = ", True)
  e = num("E (margin) = ", True)
  c = getconf()
  tb, ex = show_z(c)
  vt = (tb * sg / e) ** 2
  ve = (ex * sg / e) ** 2
  print("TABLE " + f4(vt) + " -> " + str(ceil_n(vt)))
  print("EXACT " + f4(ve) + " -> " + str(ceil_n(ve)))
  pause()


def m_n_prop():
  print("MIN n for a PROPORTION")
  print("no pilot: p* = .50, round UP")
  e = num("E (3 points = .03): ", True)
  if e >= 1:
    e = e / 100
    print("using E = " + str(e))
  ps = num("p* (0 = no pilot) = ")
  if ps <= 0:
    ps = 0.5
  elif ps >= 1:
    ps = ps / 100
  c = getconf()
  tb, ex = show_z(c)
  vt = tb * tb * ps * (1 - ps) / (e * e)
  ve = ex * ex * ps * (1 - ps) / (e * e)
  print("TABLE " + f4(vt) + " -> " + str(ceil_n(vt)))
  print("EXACT " + f4(ve) + " -> " + str(ceil_n(ve)))
  pause()


def m_back():
  print("FROM A CI (L, U)")
  lo = num("L = ")
  hi = num("U = ")
  print("center = (L+U)/2 = " + str(rnd((lo + hi) / 2, 6)))
  print("E = (U-L)/2 = " + str(rnd((hi - lo) / 2, 6)))
  print("width = U-L = " + str(rnd(hi - lo, 6)))
  pause()


def m_sd():
  print("STD DEV from raw data")
  print("enter values, blank = done")
  xs = []
  while True:
    s = input("x" + str(len(xs) + 1) + " = ").strip()
    if s == "":
      break
    try:
      xs.append(float(eval(s, ENV)))
    except:
      print("Not a number")
  n = len(xs)
  if n < 2:
    print("need 2+ values")
    pause()
    return
  m = sum(xs) / n
  ss = 0.0
  for x in xs:
    ss += (x - m) ** 2
  print("n=" + str(n) + " mean=" + f4(m))
  print("sum(x-mean)^2 = " + f4(ss))
  print("POP sigma /N = " + f4(math.sqrt(ss / n)))
  print("SAMPLE s /(n-1) = " + f4(math.sqrt(ss / (n - 1))))
  pause()


def m_which():
  print("About: 1 one value x")
  print("2 an average  3 a proportion")
  a = pick("Pick: ", 3)
  if a == 1:
    print("Ch 6: z = (x-mu)/sigma")
    print("P -> menu 1. Cutoff -> 4")
    pause()
    return
  print("Want: 1 probability")
  print("2 interval  3 sample size")
  b = pick("Pick: ", 3)
  if a == 2:
    if b == 1:
      print("Ch 7: SE = sigma/sqrt(n)")
      print("z, never t -> menu 2")
    elif b == 2:
      print("sigma given -> z, menu 6")
      print("only s -> t, menu 7")
    else:
      print("n=((z)(sigma)/E)^2 menu 9")
  else:
    if b == 1:
      print("Ch 7: p KNOWN -> menu 3")
      print("SE = sqrt(p(1-p)/n)")
    elif b == 2:
      print("Ch 8: SE uses pbar, menu 8")
    else:
      print("p*=.50 if no pilot, menu 10")
  pause()


MENU = [
  ("Which formula?", m_which),
  ("P one x (Ch6)", m_individual),
  ("P xbar (Ch7)", m_xbar),
  ("P pbar (Ch7)", m_pbar),
  ("Percent->cutoff", m_inverse),
  ("Critical z / t", m_crit),
  ("CI mu, sigma: z", m_ci_z),
  ("CI mu, s: t", m_ci_t),
  ("CI p", m_ci_p),
  ("Min n, mean", m_n_mean),
  ("Min n, prop", m_n_prop),
  ("From CI: E, ctr", m_back),
  ("Std dev of data", m_sd),
]


def main():
  while True:
    print("== EXAM 2 (q quits) ==")
    for i in range(0, len(MENU), 2):
      a = (str(i) + " " + MENU[i][0] + " " * 16)[:16]
      if i + 1 < len(MENU):
        a = a + str(i + 1) + " " + MENU[i + 1][0]
      print(a[:32])
    s = input("Pick #: ").strip()
    if s == "q" or s == "Q":
      break
    try:
      k = int(s)
    except:
      continue
    if 0 <= k < len(MENU):
      try:
        MENU[k][1]()
      except KeyboardInterrupt:
        print("back to menu")
      except Exception as e:
        print("Error:", e)
        pause()


main()
