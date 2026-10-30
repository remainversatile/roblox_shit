# E2P - probability, cutoff and critical values for EXAM2.
# Loaded only while in use. Keep with EXAM2.py.
from E2U import *

# ---- probability (Ch 6, Ch 7) ----
RULE = ["", "left area", "1 - left area", "left(b) - left(a)", "1 - between"]
WHAT = ["", "Below a", "Above a", "Between a and b", "Outside a to b"]

def area(pa, pb, k):
  return [0, pa, 1 - pa, pb - pa, 1 - pb + pa][k]

def prob():
  w = pick(["1 One value x (Ch 6)", "2 Sample mean xbar (Ch 7)", "3 Sample prop pbar (Ch 7)", "0 Cancel"], 3)
  if not w:
    return
  if w == 3:
    c = askp("Population proportion p")
    n = ask("Sample size n", True)
    se = math.sqrt(c * (1 - c) / n)
    st = rnd(se, 4)
    ok = n * c >= 5 and n * (1 - c) >= 5
    cs = mk("Setup: sample prop", ["np = " + f2(n * c), "n(1-p) = " + f2(n * (1 - c)),
            "Both >= 5: normal" if ok else "NOT both >= 5!", "!SE = " + f4(se)],
            ("SE", "sqrt[ " + sh(c) + "(" + sh(1 - c) + ") ]", "sqrt(" + sh(n) + ")"))
  else:
    c = ask("Population mean mu")
    sg = ask("Population sigma", True)
    n = ask("Sample size n", True) if w == 2 else 1
    se = st = sg / math.sqrt(n)
    if w == 2:
      cs = mk("Setup: sample mean", ["E(xbar) = mu = " + sh(c), "!SE = " + f4(se),
              "n >= 30: approx normal" if n >= 30 else "n < 30: pop must be normal"],
              ("SE", sh(sg), "sqrt(" + sh(n) + ")"))
    else:
      cs = mk("Setup: one value", ["Center mu = " + sh(c), "Spread sigma = " + sh(sg)], ("z", "x - mu", "sigma"))
  k = pick(["1 Below a | 2 Above a", "3 Between | 4 Outside", "5 Within +/-d of center", "0 Cancel"], 5)
  if not k:
    return
  if k == 5:
    d = ask("Distance d from center", True)
    a, b, k = c - d, c + d, 3
  elif k > 2:
    a = ask("Lower value a")
    b = ask("Upper value b")
    if b < a:
      a, b = b, a
  else:
    a = b = ask("Value a")
  za, zb = (a - c) / se, (b - c) / se
  ta, tb = rnd((a - c) / st, 2), rnd((b - c) / st, 2)
  for v, z, t in (("a", za, ta), ("b", zb, tb))[:1 if k < 3 else 2]:
    cs += mk("z for " + v, ["z = " + f4(z), "!Table z = " + f2(t), "Left area = " + f4(tphi(t))],
             ("z", sh(a if v == "a" else b) + " - " + sh(c), f4(st)))
  pt = area(tphi(ta), tphi(tb), k)
  ans = [WHAT[k], "Rule: " + RULE[k], "!TABLE P = " + f4(pt), "EXACT P = " + f4(area(phi(za), phi(zb), k)),
         "Percent: " + f2(pt * 100) + "%"]
  if k > 2:
    ans.append("Subtract AREAS, not z.")
  browse(cs + mk("Answer", ans))
  graph(k, ta, tb, "P = " + f4(pt))

# ---- percent -> cutoff ----
def cutoff():
  k = pick(["1 Bottom __% (below)", "2 Top __% (above)", "3 Middle __%", "0 Cancel"], 3)
  if not k:
    return
  p = askp("Percent")
  L = [p] if k == 1 else ([1 - p] if k == 2 else [(1 - p) / 2, (1 + p) / 2])
  g = pick(["Solve for:", "1 Cutoff, one x", "2 Cutoff, xbar", "3 Cutoff, pbar", "4 Unknown mean mu", "0 Cancel"], 4)
  if not g:
    return
  if g == 3:
    c = askp("Population proportion p")
    n = ask("Sample size n", True)
    se = math.sqrt(c * (1 - c) / n)
    st = rnd(se, 4)
  else:
    c = ask("Known value x" if g == 4 else "Population mean mu")
    sg = ask("Population sigma", True)
    se = st = sg / math.sqrt(ask("Sample size n", True)) if g == 2 else sg
  cs = []
  for a in L:
    zt, ze = tablez(a), invphi(a)
    cs += mk("LEFT area " + f4(a), ["Find " + f4(a) + " INSIDE table.", "!Table z = " + str(zt), "Calculator z = " + f4(ze)])
    if g == 4:
      cs += mk("Unknown mean", ["mu = x - (z)(sigma)", "= " + sh(c) + " - (" + str(zt) + ")(" + sh(st) + ")",
               "!TABLE mu = " + f4(c - zt * st), "EXACT mu = " + f4(c - ze * se)])
    else:
      cs += mk("Cutoff", ["= center + (z)(SE)", "= " + sh(c) + " + (" + str(zt) + ")(" + sh(st) + ")",
               "!TABLE = " + f4(c + zt * st), "EXACT = " + f4(c + ze * se)])
  browse(cs)
  z1 = tablez(L[0])
  graph(k, z1, tablez(L[-1]), ["", "Bottom ", "Top ", "Middle "][k] + f2(p * 100) + "%")

# ---- critical values ----
def crit():
  c = askc()
  al = 1 - c / 100
  tb, ex = zcrit(c)
  cs = mk("Critical probabilities", ["Confidence " + sh(c) + "%", "alpha = " + f4(al), "!alpha/2 = " + f4(al / 2),
          "!1 - alpha/2 = " + f4(1 - al / 2)])
  cs += mk("Critical z", ["!Table z = +/-" + str(tb), "Calculator z = " + f4(ex), "sigma known, proportions,", "sample size."])
  disp_clr()
  s = input("n for a t value (ENTER skip): ").strip()
  if s:
    v = int(parse(s) - 1 + 0.5)
    if v >= 1:
      cs += mk("Critical t", ["df = n - 1 = %d" % v, "Upper area " + f4(al / 2), "!t = +/-%.3f" % invt(al / 2, v), "Only s given."])
  browse(cs)

