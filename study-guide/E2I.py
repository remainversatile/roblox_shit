# E2I - intervals, sample size and CI tools for EXAM2.
# Loaded only while in use. Keep with EXAM2.py.
from E2U import *

# ---- confidence intervals ----
def ival(est, et, ee, what):
  d = min(int(ask("Decimals the question wants", nonneg=True)), 6)
  fm = "%." + str(d) + "f"
  return mk("Interval", ["!TABLE (" + fm % (est - et) + ", " + fm % (est + et) + ")",
            "EXACT (" + fm % (est - ee) + ", " + fm % (est + ee) + ")", "Width = 2E = " + fm % (2 * et),
            "We are __% confident the", what, "is in this interval."])

def ci():
  k = pick(["1 mu, sigma known (z)", "2 mu, only s given (t)", "3 p from pbar", "4 p from count x", "0 Cancel"], 4)
  if not k:
    return
  if k < 3:
    xb = ask("Sample mean xbar")
    sg = ask("Population sigma" if k == 1 else "Sample s", True)
    n = ask("Sample size n", True)
    c = askc()
    se = sg / math.sqrt(n)
    cs = mk("Standard error", ["!SE = " + f4(se)], ("SE", sh(sg), "sqrt(" + sh(n) + ")"))
    if k == 1:
      tb, ex = zcrit(c)
      cs += mk("Critical z", ["sigma known -> z", "!Table z = " + str(tb), "Calculator z = " + f4(ex)])
    else:
      if n < 2:
        raise ValueError("Need n >= 2")
      v = int(n - 1 + 0.5)
      up = (1 - c / 100) / 2
      ex = invt(up, v)
      note("t-table lookup", ["Row: df = %d" % v, "Column: upper " + f4(up), "!Exact t = %.3f" % ex,
           "n < 30: needs normal pop" if n < 30 else "t even with n >= 30", "Next: YOUR table t"])
      tb = ask("Your table t (0 = exact)", nonneg=True) or rnd(ex, 3)
    cs += mk("Margin of error", ["E = (crit)(SE)", "= (" + sh(tb) + ")(" + f4(se) + ")", "!E = " + f4(tb * se),
             "Exact E = " + f4(ex * se)])
    browse(cs + ival(xb, tb * se, ex * se, "population mean"))
    return
  if k == 4:
    x = ask("Count x", nonneg=True)
    n = ask("Sample size n", True)
    pb = x / n
  else:
    pb = askp("Sample proportion pbar")
    n = ask("Sample size n", True)
  c = askc()
  tb, ex = zcrit(c)
  se = math.sqrt(pb * (1 - pb) / n)
  ok = n * pb >= 5 and n * (1 - pb) >= 5
  cs = mk("Check + SE", ["pbar = " + f4(pb), "Counts " + f2(n * pb) + ", " + f2(n * (1 - pb)),
          "Both >= 5: OK" if ok else "Counts < 5: not normal", "!SE = " + f4(se)],
          ("SE", "sqrt[ " + f4(pb) + "(" + f4(1 - pb) + ") ]", "sqrt(" + sh(n) + ")"))
  cs += mk("Margin of error", ["z table " + str(tb) + ", exact " + f4(ex), "SE uses pbar (p unknown).",
           "!E = " + f4(tb * se), "Exact E = " + f4(ex * se)])
  browse(cs + ival(pb, tb * se, ex * se, "population proportion"))

# ---- minimum sample size ----
def size():
  k = pick(["1 Mean, sigma given", "2 Mean, use range/4", "3 Proportion", "0 Cancel"], 3)
  if not k:
    return
  if k == 3:
    e = ask("Margin E (3 pts = .03)", True)
    if e >= 1:
      e /= 100
    disp_clr()
    s = input("Pilot p* (ENTER = .50): ").strip()
    p = parse(s) if s else 0.5
    if p >= 1:
      p /= 100
    if not 0 < p < 1:
      raise ValueError("Need 0 < p* < 1")
    c = askc()
    tb, ex = zcrit(c)
    vt, ve = tb * tb * p * (1 - p) / e / e, ex * ex * p * (1 - p) / e / e
    fr = ("n", "(" + str(tb) + ")^2 (" + sh(p) + ")(" + sh(1 - p) + ")", "(" + sh(e) + ")^2")
  else:
    sg = ask("Range (max - min)", True) / 4 if k == 2 else ask("Population sigma", True)
    e = ask("Margin E", True)
    c = askc()
    tb, ex = zcrit(c)
    vt, ve = (tb * sg / e) ** 2, (ex * sg / e) ** 2
    fr = ("n", "[ (" + str(tb) + ")(" + sh(sg) + ") ]^2", "(" + sh(e) + ")^2")
  browse(mk("Minimum n", ["n = " + f4(vt), "!Round UP: %d" % math.ceil(vt - 1e-9),
            "Exact z: %d" % math.ceil(ve - 1e-9), "Always round up."], fr))

# ---- more ----
def more():
  k = pick(["1 From a CI: center, E", "2 Std dev from raw data", "0 Cancel"], 2)
  if k == 1:
    lo = ask("Lower endpoint L")
    hi = ask("Upper endpoint U")
    browse(mk("From a CI", ["center = (L + U) / 2", "!center = " + sh((lo + hi) / 2), "E = (U - L) / 2",
              "!E = " + sh((hi - lo) / 2), "Width = " + sh(hi - lo)]))
  elif k == 2:
    xs = []
    while True:
      disp_clr()
      print("Value x%d (blank = done)" % (len(xs) + 1))
      s = input("> ").strip()
      if not s:
        break
      try:
        xs.append(parse(s))
      except ValueError as e:
        print(str(e))
        input("ENTER to retry")
    n = len(xs)
    if n < 2:
      raise ValueError("Need 2 or more values")
    m = sum(xs) / n
    ss = sum([(x - m) ** 2 for x in xs])
    browse(mk("Std dev", ["n = %d, mean = " % n + f4(m), "Sum (x-mean)^2 = " + f4(ss),
              "!Population sigma = " + f4(math.sqrt(ss / n)), "(divide by N)",
              "!Sample s = " + f4(math.sqrt(ss / (n - 1))), "(divide by n - 1)"]))

