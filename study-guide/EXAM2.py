# EXAM2 - TI-84 Evo Python study reference, MGSC 2301 Exam 2 (Ch 6-8).
# Built on the ECON2 menu and card layout.
# Plain ASCII, core Python, ti_draw; no external Python packages.
# Every calculation shows TABLE (course z-table method, matches the
# answer key) and EXACT (full calculator precision).
import math
try:
    import ti_draw as dr
    GRAPHICS = True
except ImportError:
    GRAPHICS = False
try:
    from ti_system import disp_clr
except ImportError:
    def disp_clr():
        print("\n" * 3)

# ---------- numbers ----------

TBLZ = {80: 1.28, 90: 1.645, 95: 1.96, 98: 2.33, 99: 2.576}
OK_CHARS = "0123456789.+-*/() "

def parse(s):
    # Numbers, a/b, and sqrt(), e.g. 46/sqrt(85)
    s = s.strip()
    for c in s.replace("sqrt", ""):
        if c not in OK_CHARS:
            raise ValueError("Use digits, / and sqrt()")
    try:
        return float(eval(s, {"sqrt": math.sqrt}))
    except ZeroDivisionError:
        raise ValueError("Zero denominator")
    except Exception:
        raise ValueError("Not a number")

def rnd(x, d):
    # half away from zero, float-safe
    m = 10 ** d
    sg = -1 if x < 0 else 1
    return sg * math.floor(abs(x) * m + 0.5 + 1e-9) / m

def f4(x):
    return "%.4f" % x

def f2(x):
    return "%.2f" % x

def short(x):
    return "%.6g" % x

def ceil_n(v):
    return int(math.ceil(v - 1e-9))

# ---------- normal and t distributions ----------

try:
    _erf = math.erf
except AttributeError:
    def _erf(x):
        # all-positive series, full precision
        sg = -1 if x < 0 else 1
        x = abs(x)
        if x > 6:
            return sg * 1.0
        term, s, k = x, x, 0
        while term > 1e-17 * s:
            k += 1
            term = term * 2 * x * x / (2 * k + 1)
            s += term
        return sg * 2 / math.sqrt(math.pi) * math.exp(-x * x) * s

def phi(z):
    # area to the LEFT of z
    return 0.5 * (1 + _erf(z / math.sqrt(2)))

def tphi(z):
    # table reading: z to 2 places, 4-place area
    z = rnd(z, 2)
    if z < -3.49:
        return 0.0
    if z > 3.49:
        return 1.0
    return rnd(phi(z), 4)

def invphi(a):
    lo, hi = -9.0, 9.0
    for i in range(55):
        m = (lo + hi) / 2
        if phi(m) < a:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2

def tablez(a):
    # z whose 4-place area is closest to a; a tie takes the midpoint
    best, zs = 9.0, []
    z0 = rnd(invphi(a), 2)
    for i in range(-3, 4):
        z = rnd(z0 + i / 100, 2)
        d = abs(rnd(phi(z), 4) - a)
        if d < best - 1e-9:
            best, zs = d, [z]
        elif abs(d - best) <= 1e-9:
            zs.append(z)
    return rnd(sum(zs) / len(zs), 3)

try:
    _lg = math.lgamma
except AttributeError:
    def _lg(x):
        # Lanczos log-gamma
        c = [76.18009172947146, -86.50532032941677, 24.01409824083091,
             -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]
        y = x
        tmp = x + 5.5
        tmp -= (x + 0.5) * math.log(tmp)
        s = 1.000000000190015
        for k in c:
            y += 1
            s += k / y
        return -tmp + math.log(2.5066282746310005 * s / x)

def _tiny(v):
    return 1e-30 if abs(v) < 1e-30 else v

def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
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
    bt = math.exp(_lg(a + b) - _lg(a) - _lg(b) + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1 - bt * _betacf(b, a, 1 - x) / b

def tupper(t, df):
    # area to the RIGHT of t (t >= 0)
    return 0.5 * _ibeta(df / 2, 0.5, df / (df + t * t))

def invt(upper, df):
    lo, hi = 0.0, 700.0
    for i in range(50):
        m = (lo + hi) / 2
        if tupper(m, df) > upper:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2

def zcrit(c):
    # (table z, exact z) for confidence c percent
    up = 1 - (1 - c / 100) / 2
    ex = invphi(up)
    k = int(c + 0.5)
    if k in TBLZ and abs(c - k) < 1e-9:
        return TBLZ[k], ex
    return tablez(up), ex

# ---------- input ----------

def ask(label, positive=False, nonnegative=False):
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
            if positive and x <= 0:
                raise ValueError("Must be positive")
            if nonnegative and x < 0:
                raise ValueError("Cannot be negative")
            return x
        except ValueError as e:
            print(str(e))
            input("ENTER to retry")

def ask_p(label):
    # proportion: 66, 66% or .66 -> .66
    while True:
        p = ask(label + " (.66 or 66)", positive=True)
        if p > 1:
            p = p / 100
        if p < 1:
            return p
        disp_clr()
        print("Need 0 < p < 1")
        input("ENTER to retry")

def ask_conf():
    while True:
        c = ask("Confidence % (95 or .95)", positive=True)
        if c < 1:
            c = c * 100
        if c < 100:
            return c
        disp_clr()
        print("Need under 100%")
        input("ENTER to retry")

def choose(lines, n):
    # numbered submenu; returns 1..n or 0
    disp_clr()
    for line in lines:
        print(line)
    k = input("> ").strip()
    if k in [str(i) for i in range(1, n + 1)]:
        return int(k)
    return 0

# ---------- screen and cards (ECON2 layout) ----------

def wrap(text, width=28):
    lines, line = [], ""
    for word in text.split():
        if len(word) > width:
            raise ValueError("Display word too long")
        if line and len(line) + len(word) + 1 > width:
            lines.append(line)
            line = word
        else:
            line = word if not line else line + " " + word
    if line:
        lines.append(line)
    return lines

def ink(r, g, b):
    dr.set_color(r, g, b)

def text(x, y, s):
    dr.draw_text(x, y, s)

NAVY = (10, 65, 100)
TOPIC_COLORS = [(10, 65, 100), (0, 105, 75), (150, 75, 0), (130, 35, 110),
                (165, 35, 45), (55, 60, 135), (0, 110, 130), (110, 85, 20)]
ACCENT = [NAVY]

def tint(c):
    return (c[0] + (255 - c[0]) * 7 // 8, c[1] + (255 - c[1]) * 7 // 8, c[2] + (255 - c[2]) * 7 // 8)

def box(x, y, w, h):
    try:
        dr.fill_rect(x, y, w, h)
    except Exception:
        pass

def frame(title, tag, index=0, total=0):
    a = ACCENT[0]
    dr.clear()
    dr.set_pen("thin", "solid")
    ink(*tint(a))
    box(0, 0, 320, 24)
    ink(*a)
    text(8, 5, title)
    box(0, 24, 320, 2)
    dr.draw_line(0, 25, 319, 25)
    if total > 1:
        ink(205, 210, 215)
        box(0, 26, 320, 3)
        ink(*a)
        box(0, 26, 320 * index // total, 3)
    ink(232, 235, 238)
    box(0, 188, 320, 22)
    ink(70, 70, 70)
    text(8, 192, tag)

# Card: (title, body lines, fraction or None).
# Fraction: (left label, numerator text, denominator text).
# Body lines starting with "!" are answers: drawn on a highlight bar.
# Body lines ending with ":" are subheadings: drawn in the accent color.
def show(card, index=1, total=1):
    title, lines, fraction = card
    if total > 1:
        footer = "Page " + str(index) + " of " + str(total) + "   CLEAR = nav"
    else:
        footer = "Press CLEAR"
    if GRAPHICS:
        a = ACCENT[0]
        frame(title, footer, index, total)
        if fraction:
            label, num, den = fraction
            ink(*tint(a))
            box(4, 31, 312, 74)
            ink(*a)
            text(10, 33, label + " =")
            ink(25, 25, 25)
            text(24, 52, num)
            ink(*a)
            dr.draw_line(20, 73, 300, 73)
            dr.draw_line(20, 74, 300, 74)
            ink(25, 25, 25)
            text(24, 79, den)
            y = 112
        else:
            y = 35
        for line in lines:
            if line[:1] == "!":
                ink(*tint(a))
                box(4, y - 2, 312, 19)
                ink(*a)
                box(4, y - 2, 3, 19)
                ink(0, 0, 0)
                text(12, y, line[1:])
            elif line[-1:] == ":":
                ink(*a)
                text(8, y, line)
            else:
                ink(25, 25, 25)
                text(8, y, line)
            y += 18
        dr.show_draw()
    else:
        disp_clr()
        print("== " + title + " ==")
        if fraction:
            label, num, den = fraction
            print(label + " =")
            print("  " + num)
            print(" " + "-" * 28)
            print("  " + den)
        for line in lines:
            if line[:1] == "!":
                print(">> " + line[1:])
            else:
                print(line)

def card(title, body, frac=None):
    lines = body.split("\n") if isinstance(body, str) else body
    flat = []
    for line in lines:
        if not line:
            flat.append("")
        elif line[:1] == "!" and len(line) > 29:
            # keep every wrapped piece of an answer highlighted
            flat += ["!" + w for w in wrap(line[1:], 27)]
        else:
            flat += wrap(line)
    if len(flat) > (4 if frac else 8):
        raise ValueError("Card too tall: " + title)
    return (title, flat, frac)

def res(title, body, frac=None):
    # Result cards: anything too tall continues on extra pages.
    lines = body.split("\n") if isinstance(body, str) else body
    flat = []
    for line in lines:
        if line[:1] == "!" and len(line) > 29:
            flat += ["!" + w for w in wrap(line[1:], 27)]
        else:
            flat += wrap(line) if line else [""]
    room = 4 if frac else 8
    if len(flat) <= room:
        return [(title, flat, frac)]
    out = [(title, flat[:room], frac)]
    flat = flat[room:]
    while flat:
        out.append((title + " (cont)", flat[:8], None))
        flat = flat[8:]
    return out

def browse(cards):
    flat = []
    for c in cards:
        if isinstance(c, list):
            flat += c
        else:
            flat.append(c)
    cards = flat
    i = 0
    while True:
        show(cards[i], i + 1, len(cards))
        disp_clr()
        print("ENTER next | 1 previous")
        print("2 jump to page | 0 menu")
        c = input("> ").strip()
        if c == "0":
            return
        if c == "1":
            i = (i - 1) % len(cards)
        elif c == "2":
            try:
                j = int(input("Page 1-" + str(len(cards)) + ": "))
                if 1 <= j <= len(cards):
                    i = j - 1
            except ValueError:
                pass
        else:
            i = (i + 1) % len(cards)

def note(title, body):
    # card(s) shown before the next prompt
    for c in res(title, body):
        show(c)
        if not GRAPHICS:
            input("ENTER: continue")

# ---------- normal-curve graph ----------

def curve_y(z):
    return 160 - 118 * math.exp(-z * z / 2)

def zx(z):
    z = max(-3.6, min(3.6, z))
    return int(160 + z * 38)

def graph(kind, za, zb, label):
    # kind: 1 below, 2 above, 3 between, 4 outside
    if not GRAPHICS:
        return
    a = ACCENT[0]
    frame("Shaded area", "CLEAR: return to menu")
    ink(150, 200, 190)
    for px in range(23, 298):
        z = (px - 160) / 38
        if kind == 1:
            inside = z <= za
        elif kind == 2:
            inside = z >= za
        elif kind == 3:
            inside = za <= z <= zb
        else:
            inside = z <= za or z >= zb
        if inside:
            dr.draw_line(px, 160, px, int(curve_y(z)))
    ink(0, 0, 0)
    dr.draw_line(20, 160, 300, 160)
    ink(*a)
    prev = None
    for px in range(23, 298, 2):
        pt = (px, int(curve_y((px - 160) / 38)))
        if prev:
            dr.draw_line(prev[0], prev[1], pt[0], pt[1])
        prev = pt
    ink(70, 70, 70)
    marks = [za] if kind <= 2 else [za, zb]
    for z in marks:
        dr.draw_line(zx(z), 160, zx(z), int(curve_y(max(-3.6, min(3.6, z)))))
        lab = f2(z)
        text(max(4, min(zx(z) - 14, 316 - 10 * len(lab))), 164, lab)
    ink(0, 0, 0)
    text(8, 171, label)
    dr.show_draw()

def offer_graph(kind, za, zb, label):
    if GRAPHICS:
        disp_clr()
        if input("1 View graph; ENTER menu: ").strip() == "1":
            graph(kind, za, zb, label)

# ---------- probability (Ch 6 and Ch 7) ----------

RULES = ["", "left area", "1 - left area", "left(b) - left(a)", "1 - between"]
WORDS = ["", "Below a", "Above a", "Between a and b", "Outside a to b"]

def area(pa, pb, k):
    if k == 1:
        return pa
    if k == 2:
        return 1 - pa
    if k == 3:
        return pb - pa
    return 1 - (pb - pa)

def probability():
    w = choose(["1 One value x (Ch 6)", "2 Sample mean xbar (Ch 7)",
                "3 Sample prop pbar (Ch 7)", "0 Cancel"], 3)
    if not w:
        return
    if w == 1:
        ctr = ask("Population mean mu")
        se = ask("Population sigma", positive=True)
        se_t = se
        setup = res("Setup: one value", ["Center = mu = " + short(ctr),
                     "Spread = sigma = " + short(se), "No sqrt(n): one value."], ("z", "x - mu", "sigma"))
        sym = "x"
    elif w == 2:
        ctr = ask("Population mean mu")
        sg = ask("Population sigma", positive=True)
        n = ask("Sample size n", positive=True)
        se = sg / math.sqrt(n)
        se_t = se
        shape = "n >= 30: approx normal" if n >= 30 else "n < 30: pop must be normal"
        setup = res("Setup: sample mean", ["E(xbar) = mu = " + short(ctr), "!SE = " + f4(se), shape],
                     ("SE", short(sg), "sqrt(" + short(n) + ")"))
        sym = "xbar"
    else:
        ctr = ask_p("Population proportion p")
        n = ask("Sample size n", positive=True)
        se = math.sqrt(ctr * (1 - ctr) / n)
        se_t = rnd(se, 4)
        ok = n * ctr >= 5 and n * (1 - ctr) >= 5
        setup = res("Setup: sample prop", ["np = " + f2(n * ctr) + ", n(1-p) = " + f2(n * (1 - ctr)),
                     "Both >= 5: approx normal" if ok else "NOT both >= 5: not normal",
                     "!SE = " + f4(se) + " (table uses)", "Count given? use x/n"],
                     ("SE", "sqrt[ " + short(ctr) + "(" + short(1 - ctr) + ") ]", "sqrt(" + short(n) + ")"))
        sym = "pbar"
    k = choose(["1 Below a | 2 Above a", "3 Between | 4 Outside",
                "5 Within +/-d of center", "0 Cancel"], 5)
    if not k:
        return
    if k == 5:
        d = ask("Distance d from center", positive=True)
        a, b, k = ctr - d, ctr + d, 3
    elif k >= 3:
        a = ask("Lower value a")
        b = ask("Upper value b")
        if b < a:
            a, b = b, a
    else:
        a = ask("Value a")
        b = a
    za, zb = (a - ctr) / se, (b - ctr) / se
    ta, tb = rnd((a - ctr) / se_t, 2), rnd((b - ctr) / se_t, 2)
    cards = [setup, res("z for a", ["z = " + f4(za), "!Table z = " + f2(ta), "Left area = " + f4(tphi(ta))],
                         ("z", short(a) + " - " + short(ctr), f4(se_t)))]
    if k >= 3:
        cards.append(res("z for b", ["z = " + f4(zb), "!Table z = " + f2(tb), "Left area = " + f4(tphi(tb))],
                          ("z", short(b) + " - " + short(ctr), f4(se_t))))
    pt = area(tphi(ta), tphi(tb), k)
    pe = area(phi(za), phi(zb), k)
    ans = [WORDS[k] + " (" + sym + ")", "Rule: " + RULES[k], "!TABLE P = " + f4(pt),
           "EXACT P = " + f4(pe), "As percent: " + f2(pt * 100) + "%"]
    if k >= 3:
        ans.append("Subtract AREAS, not z.")
    if abs(ta) > 3.49 or abs(tb) > 3.49:
        ans.append("Past 3.49: table edge.")
    cards.append(res("Answer", ans))
    browse(cards)
    offer_graph(k, ta, tb, "P = " + f4(pt))

# ---------- percent -> cutoff ----------

def cutoff():
    k = choose(["1 Bottom __% (below)", "2 Top __% (above)", "3 Middle __%", "0 Cancel"], 3)
    if not k:
        return
    pc = ask_p("Percent")
    lefts = [pc] if k == 1 else ([1 - pc] if k == 2 else [(1 - pc) / 2, 1 - (1 - pc) / 2])
    g = choose(["Solve for:", "1 Cutoff for one x", "2 Cutoff for xbar", "3 Cutoff for pbar",
                "4 Unknown mean mu", "0 Cancel"], 4)
    if not g:
        return
    if g == 4:
        x = ask("Known value x")
        sg = ask("Population sigma", positive=True)
    elif g == 3:
        ctr = ask_p("Population proportion p")
        n = ask("Sample size n", positive=True)
        se = math.sqrt(ctr * (1 - ctr) / n)
        se_t = rnd(se, 4)
    else:
        ctr = ask("Population mean mu")
        sg = ask("Population sigma", positive=True)
        se = sg
        if g == 2:
            n = ask("Sample size n", positive=True)
            se = sg / math.sqrt(n)
        se_t = se
    cards = []
    for a in lefts:
        cards.append(res("LEFT area " + f4(a), ["Find " + f4(a) + " INSIDE table.", "!Table z = " + str(tablez(a)),
                          "Calculator z = " + f4(invphi(a)), "Top __%: left = 1 - __."]))
    for a in lefts:
        zt, ze = tablez(a), invphi(a)
        if g == 4:
            cards.append(res("Unknown mean", ["mu = x - (z)(sigma)", "= " + short(x) + " - (" + str(zt) + ")(" + short(sg) + ")",
                              "!TABLE mu = " + f4(x - zt * sg), "EXACT mu = " + f4(x - ze * sg)]))
        else:
            cards.append(res("Cutoff", ["cutoff = center + (z)(SE)", "= " + short(ctr) + " + (" + str(zt) + ")(" + short(se_t) + ")",
                              "!TABLE = " + f4(ctr + zt * se_t), "EXACT = " + f4(ctr + ze * se),
                              "z < 0: cutoff below mean."]))
    browse(cards)
    zs = [tablez(a) for a in lefts]
    if k == 3:
        offer_graph(3, zs[0], zs[1], "Middle " + f2(pc * 100) + "%")
    else:
        offer_graph(k, zs[0], zs[0], WORDS[k].split()[0] + " " + f2(pc * 100) + "%")

# ---------- critical values ----------

def critical():
    c = ask_conf()
    al = 1 - c / 100
    tb, ex = zcrit(c)
    cards = [res("Critical probabilities", ["Confidence " + short(c) + "%", "alpha = " + f4(al),
                  "!alpha/2 = " + f4(al / 2), "!1 - alpha/2 = " + f4(1 - al / 2), "Look up 1 - alpha/2."]),
             res("Critical z", ["!Table z = +/-" + str(tb), "Calculator z = " + f4(ex), "Used for: sigma known,",
                  "proportions, sample size."])]
    disp_clr()
    s = input("n for a t value (ENTER skip): ").strip()
    if s:
        n = parse(s)
        if n >= 2:
            df = int(n - 1 + 0.5)
            cards.append(res("Critical t", ["df = n - 1 = " + str(df), "Column: upper area " + f4(al / 2),
                              "!t = +/-" + "%.3f" % invt(al / 2, df), "Used for: only s given."]))
    browse(cards)

# ---------- confidence intervals ----------

def ci_cards(est, e_t, e_e, dp, what):
    fm = "%." + str(dp) + "f"
    return res("Interval", ["!TABLE (" + fm % (est - e_t) + ", " + fm % (est + e_t) + ")",
                "EXACT (" + fm % (est - e_e) + ", " + fm % (est + e_e) + ")",
                "Width = 2E = " + fm % (2 * e_t), "We are confident the", what, "is in this interval."])

def ask_dp():
    d = int(ask("Decimals the question wants", nonnegative=True))
    return min(d, 6)

def interval():
    k = choose(["1 mu, sigma known (z)", "2 mu, only s given (t)", "3 p from pbar",
                "4 p from count x", "0 Cancel"], 4)
    if not k:
        return
    if k == 1:
        xb = ask("Sample mean xbar")
        sg = ask("Population sigma", positive=True)
        n = ask("Sample size n", positive=True)
        c = ask_conf()
        tb, ex = zcrit(c)
        se = sg / math.sqrt(n)
        cards = [res("Standard error", ["!SE = " + f4(se), "sigma known -> z"], ("SE", short(sg), "sqrt(" + short(n) + ")")),
                 res("Critical z", ["Confidence " + short(c) + "%", "!Table z = " + str(tb), "Calculator z = " + f4(ex)]),
                 res("Margin of error", ["E = (z)(SE)", "= (" + str(tb) + ")(" + f4(se) + ")", "!E = " + f4(tb * se), "Exact E = " + f4(ex * se)])]
        dp = ask_dp()
        cards.append(ci_cards(xb, tb * se, ex * se, dp, "population mean"))
    elif k == 2:
        xb = ask("Sample mean xbar")
        s = ask("Sample s", positive=True)
        n = ask("Sample size n (2+)", positive=True)
        if n < 2:
            raise ValueError("Need n >= 2")
        c = ask_conf()
        df = int(n - 1 + 0.5)
        up = (1 - c / 100) / 2
        te = invt(up, df)
        note("t-table lookup", ["Row: df = " + str(df), "Column: upper area " + f4(up), "!Exact t = " + "%.3f" % te,
             "n < 30: needs normal pop" if n < 30 else "t even though n >= 30", "Next: type YOUR table t."])
        tt = ask("Your table t (0 = exact)", nonnegative=True)
        if tt == 0:
            tt = rnd(te, 3)
        se = s / math.sqrt(n)
        cards = [res("Standard error", ["!SE = " + f4(se), "only s -> t, df = " + str(df)], ("SE", short(s), "sqrt(" + short(n) + ")")),
                 res("Margin of error", ["E = (t)(SE)", "= (" + short(tt) + ")(" + f4(se) + ")", "!E = " + f4(tt * se), "Exact E = " + f4(te * se)])]
        dp = ask_dp()
        cards.append(ci_cards(xb, tt * se, te * se, dp, "population mean"))
    else:
        if k == 4:
            x = ask("Count x", nonnegative=True)
            n = ask("Sample size n", positive=True)
            pb = x / n
        else:
            pb = ask_p("Sample proportion pbar")
            n = ask("Sample size n", positive=True)
        c = ask_conf()
        tb, ex = zcrit(c)
        se = math.sqrt(pb * (1 - pb) / n)
        ok = n * pb >= 5 and n * (1 - pb) >= 5
        cards = [res("Check + SE", ["pbar = " + f4(pb), "Counts " + f2(n * pb) + ", " + f2(n * (1 - pb)),
                      "Both >= 5: OK" if ok else "Counts < 5: not normal", "!SE = " + f4(se)],
                      ("SE", "sqrt[ " + f4(pb) + "(" + f4(1 - pb) + ") ]", "sqrt(" + short(n) + ")")),
                 res("Margin of error", ["Table z = " + str(tb) + " (exact " + f4(ex) + ")", "E = (z)(SE)",
                      "!E = " + f4(tb * se), "Exact E = " + f4(ex * se), "SE uses pbar (p unknown)."])]
        dp = ask_dp()
        cards.append(ci_cards(pb, tb * se, ex * se, dp, "population proportion"))
    browse(cards)

# ---------- minimum sample size ----------

def sample_size():
    k = choose(["1 Mean, sigma given", "2 Mean, use range/4", "3 Proportion", "0 Cancel"], 3)
    if not k:
        return
    if k == 3:
        e = ask("Margin E (3 pts = .03)", positive=True)
        if e >= 1:
            e = e / 100
        disp_clr()
        s = input("Pilot p* (ENTER = .50): ").strip()
        ps = parse(s) if s else 0.5
        if ps >= 1:
            ps = ps / 100
        if not 0 < ps < 1:
            raise ValueError("Need 0 < p* < 1")
        c = ask_conf()
        tb, ex = zcrit(c)
        vt = tb * tb * ps * (1 - ps) / (e * e)
        ve = ex * ex * ps * (1 - ps) / (e * e)
        frac = ("n", "(" + str(tb) + ")^2 (" + short(ps) + ")(" + short(1 - ps) + ")", "(" + short(e) + ")^2")
        title = "Min n: proportion"
    else:
        if k == 2:
            sg = ask("Range (max - min)", positive=True) / 4
        else:
            sg = ask("Population sigma", positive=True)
        e = ask("Margin E", positive=True)
        c = ask_conf()
        tb, ex = zcrit(c)
        vt = (tb * sg / e) ** 2
        ve = (ex * sg / e) ** 2
        frac = ("n", "[ (" + str(tb) + ")(" + short(sg) + ") ]^2", "(" + short(e) + ")^2")
        title = "Min n: mean"
    browse([res(title, ["n = " + f4(vt), "!Round UP: " + str(ceil_n(vt)), "Exact z: " + str(ceil_n(ve)),
                         "Always round up."], frac)])

# ---------- more tools ----------

def more():
    k = choose(["1 From a CI: center, E", "2 Std dev from raw data", "0 Cancel"], 2)
    if k == 1:
        lo = ask("Lower endpoint L")
        hi = ask("Upper endpoint U")
        browse([res("From a CI", ["center = (L + U) / 2", "!center = " + short((lo + hi) / 2),
                     "E = (U - L) / 2", "!E = " + short((hi - lo) / 2), "Width = " + short(hi - lo)])])
    elif k == 2:
        xs = []
        while True:
            disp_clr()
            print("Value x" + str(len(xs) + 1))
            print("Blank = done")
            s = input("> ").strip()
            if s == "":
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
        ss = 0.0
        for x in xs:
            ss += (x - m) ** 2
        browse([res("Std dev", ["n = " + str(n) + ", mean = " + f4(m), "Sum (x-mean)^2 = " + f4(ss),
                     "!Population sigma = " + f4(math.sqrt(ss / n)), "(divide by N)",
                     "!Sample s = " + f4(math.sqrt(ss / (n - 1))), "(divide by n - 1)"])])

def which():
    a = choose(["Question is about:", "1 One value x", "2 An average (mean)", "3 A proportion", "0 Cancel"], 3)
    if not a:
        return
    if a == 1:
        browse([res("One value: Ch 6", ["Probability: menu 3 > 1", "Cutoff: menu 4",
                      "x = mu + (z)(sigma)"], ("z", "x - mu", "sigma"))])
        return
    b = choose(["It wants:", "1 A probability", "2 An interval", "3 A sample size", "0 Cancel"], 3)
    if not b:
        return
    if a == 2:
        c = [res("Mean probability: Ch 7", ["SE = sigma / sqrt(n)", "Always z, never t.", "Menu 3 > 2"], ("z", "xbar - mu", "sigma / sqrt(n)")),
             res("Mean CI: Ch 8", ["sigma given -> z: menu 6 > 1", "only s -> t: menu 6 > 2", "df = n - 1",
                  "t even when n >= 30.", "!xbar +/- (z or t)(SE)"]),
             res("Mean sample size", ["Round UP. Menu 7 > 1", "No sigma: range / 4"], ("n", "[ (z a/2)(sigma) ]^2", "E^2"))][b - 1]
    else:
        c = [res("Prop probability: Ch 7", ["p is KNOWN.", "SE = sqrt( p(1-p)/n )", "Menu 3 > 3"], ("z", "pbar - p", "sigma pbar")),
             res("Prop CI: Ch 8", ["p unknown: SE uses pbar.", "!pbar +/- (z)(SE)", "SE = sqrt(pbar(1-pbar)/n)",
                  "Menu 6 > 3 or 6 > 4"]),
             res("Prop sample size", ["p* = pilot, else .50", "Round UP. Menu 7 > 3"], ("n", "(z a/2)^2 p*(1 - p*)", "E^2"))][b - 1]
    browse([c])

# ---------- reference cards ----------
# Notes come from the course formula sheet, the Exam 2 study guide,
# the z-score sheet, and the calculator sheet.

def references():
    return [
    ("1 Z-score sheet", [
      card("One value (Ch 6)", "Center mu, spread sigma.\nOne person, fish, bill.", ("z", "x - mu", "sigma")),
      card("Sample mean (Ch 7)", "SE = sigma / sqrt(n)\nAverage of n items.\nNever plain sigma.", ("z xbar", "xbar - mu", "sigma / sqrt(n)")),
      card("Sample prop (Ch 7)", "SE uses KNOWN p.\nCount given: pbar = x/n.", ("z pbar", "pbar - p", "sqrt( p(1-p) / n )")),
      card("Backwards: value from z", "x = mu + (z)(sigma)\nmu = x - (z)(sigma)\nxbar cutoff:\nmu + (z)(sigma/sqrt(n))\nBelow-mean cutoff: z < 0\nso x comes out below mu."),
      card("What z means", "z = SDs from the center.\nz = 1.5: 1.5 SD above.\nz < 0: below, left < .5\nz > 0: above, left > .5\nz = 0: mean, area .5000\n68/95/99.7: 1, 2, 3 SD\nP(X = a) = 0 exactly."),
      card("Reading the z-table", "Table = area to the LEFT.\nRound z to 2 places first.\nRow: ones + tenths (1.2)\nColumn: hundredths (.04)\n!z = 1.24 -> .8925\nNegative: row -1.7,\ncol .05 -> -1.75 = .0401"),
      card("Area rules", "Below a: left(a)\nAbove a: 1 - left(a)\nBetween: left(b) - left(a)\nOutside: 1 - between\nWithin +/-d of center:\nleft(+z) - left(-z)\n!Subtract AREAS, not z."),
      card("Inverse: % to cutoff", "1 Wording -> LEFT area\n2 Find area INSIDE table\n3 Closest cell gives z\n4 x = mu + (z)(sigma)\nExactly halfway: average\n!.95 -> 1.645 (midpoint)"),
      card("Wording -> LEFT area", "Bottom 20% -> .20\nTop 10% -> .90\n67.72% above x -> .3228\nx above 86.65% -> .8665\nMiddle 95% -> .025, .975\n!Top __% means 1 - __."),
      card("Percentile z values", ".01 -2.33 | .99 2.33\n.025 -1.96 | .975 1.96\n.05 -1.645 | .95 1.645\n.10 -1.28 | .90 1.28\n.20 -0.84 | .80 0.84\n.25 -0.67 | .75 0.67\n.30 -0.52 | .70 0.52\n.40 -0.25 | .60 0.25"),
      card("z -> areas", "z: left, right, within\n1.00: .8413 .1587 .6826\n1.28: .8997 .1003 .7994\n1.645: .9500 .0500 .9000\n1.96: .9750 .0250 .9500\n2.33: .9901 .0099 .9802\n2.576: .9950 .0050 .9900\n3.00: .9987 .0013 .9974"),
      card("Critical z values", "Conf: 1-a/2 -> z\n80%: .9000 -> 1.28\n85%: .9250 -> 1.44\n90%: .9500 -> 1.645\n95%: .9750 -> 1.96\n98%: .9900 -> 2.33\n99%: .9950 -> 2.576"),
      card("z mistakes", "Forgot 1 - for above.\nSubtracted z, not areas.\nsigma used for xbar.\npbar used in Ch 7 SE.\nLooked up % not LEFT.\nDid not round z to 2.\n.0040 = .40%, not 4%.\nPast +/-3.49: ~0 or ~1."),
      card("z on the TI-84", "Left area of z:\nnormalcdf(-1E99,z,0,1)\nFrom raw values:\nnormalcdf(lo,hi,mu,sd)\nz from a left area:\ninvNorm(area,0,1)\nE in 1E99: 2nd , (EE)\nRound z to 2 for table.")]),
    ("2 Formula sheet", [
      card("Std dev: population", "Then take the square root.\nSheet prints xbar and n;\nfor a population that is\nmu and N.", ("sigma^2", "sum (xi - xbar)^2", "N")),
      card("Std dev: sample", "Then take the square root.\nShortcut on sheet:\n[sum x^2 - (sum x)^2/n]\ndivided by n - 1.", ("s^2", "sum (xi - xbar)^2", "n - 1")),
      card("Critical probability", "Areas for CI cutoffs:\n!alpha/2 & 1 - alpha/2\nalpha = 1 - confidence\n95%: .0250 and .9750"),
      card("z-score (raw data)", "One individual value.", ("z", "x - mu", "sigma")),
      card("z to raw score / mean", "z-score to a raw score:\n!x = mu + (z)(sigma)\nz-score to a pop mean:\n!mu = x - (z)(sigma)"),
      card("Expected value of xbar", "!E(xbar) = mu xbar = mu\nCenter of the sampling\ndistribution of xbar.\nxbar is unbiased for mu."),
      card("z-score (sample mean)", "sigma xbar = sigma/sqrt(n)", ("z xbar", "xbar - mu", "sigma xbar")),
      card("SE of mean (sigma known)", "Standard error of the mean.", ("sigma xbar", "sigma", "sqrt(n)")),
      card("CI for mu (sigma known)", "CI estimate for mu:\n!mu = xbar +/-\n!(Z a/2)(sigma / sqrt(n))\nPopulation sigma given."),
      card("SE of mean (sigma unkn.)", "Uses the sample s.", ("S xbar", "s", "sqrt(n)")),
      card("CI for mu (sigma unkn.)", "CI estimate for mu:\n!mu = xbar +/-\n!(t a/2)(s / sqrt(n))\ndf = n - 1. a/2 = alpha/2"),
      card("Sample size for mu", "= ((z a/2)(sigma) / E)^2\nAlways round UP.", ("n", "[ (z a/2)(sigma) ]^2", "E^2")),
      card("Sample proportion", "x = count of successes.", ("pbar", "x", "n")),
      card("pbar center, normality", "Expected value of pbar:\n!E(pbar) = p\nNormality requirements:\n!np >= 5, n(1 - p) >= 5"),
      card("z-score (sample prop)", "sigma pbar uses known p.", ("z pbar", "pbar - p", "sigma pbar")),
      card("SE of the proportion", "= sqrt( p(1 - p) / n )\nUses population p.", ("sigma pbar", "sqrt[ p(1 - p) ]", "sqrt(n)")),
      card("CI estimate for p", "!p = pbar +/- (Z a/2) x\n!sqrt( pbar(1-pbar) / n )\np unknown: SE uses pbar."),
      card("Sample size for p", "p* = pilot, else .50\nAlways round UP.", ("n", "(z a/2)^2 p*(1 - p*)", "E^2"))]),
    ("3 Ch 6 normal", [
      card("Normal facts", "Bell-shaped, symmetric.\nMean = median = mode.\nTotal area = 1.\nEach side of mu = .50.\nStandard normal: 0 and 1.\nContinuous: P(X = a) = 0\nP(X < a) = P(X <= a)\nExact 95%: 1.96, not 2."),
      card("Goldfish: mu 60, sd 20", "More than 80 days:\nz = (80 - 60)/20 = 1.00\n1 - .8413\n!= .1587\nMore than 60 days:\nz = 0\n!= .50"),
      card("Goldfish: between, tail", "25 to 45 days:\nz = -1.75 and -0.75\n.2266 - .0401\n!= .1865\nWithin 7 days:\nz = -2.65\n!= .0040 = .40%"),
      card("Goldfish cutoffs", "Top 10%: z = 1.28\n!60 + 1.28(20) = 85.6\nBottom 20%: z = -0.84\n!60 - 0.84(20) = 43.2\nMiddle 95%: z = +/-1.96\n!20.80 to 99.20 days"),
      card("Unknown mean / x", "86.65% below x = 449,\nsigma 36: z = 1.11\n!mu = 449 - 1.11(36)\n!= 409.04\n67.72% ABOVE x: .3228\nz = -0.46, mu 3.58, 1.04\n!x = 3.1016"),
      card("95% of values vs CI", "Middle 95% of fish:\nmu +/- 1.96(sigma)\n95% CI for a mean:\nxbar +/- 1.96(SE)\nSame 1.96, different\nquestion.")]),
    ("4 Ch 7 sampling", [
      card("Sampling dist of xbar", "Center: E(xbar) = mu\nSpread: sigma / sqrt(n)\nShape: normal if pop is\nnormal; else n >= 30\n(Central Limit Theorem).\nThe population itself\ndoes not become normal."),
      card("Credit card: setup", "mu 2864, sd 775, n 50\nSE = 775 / sqrt(50)\n!SE = 109.6016\nn >= 30: approx normal.\nNever divide by 775 here."),
      card("Credit card: answers", "xbar > 3000: z = 1.24\n!1 - .8925 = .1075\nWithin $100 of mu:\nz = +/-0.91\n!.8186 - .1814 = .6372\nn = 100: SE = 77.5\n!z +/-1.29: .8030"),
      card("Changing n", "Bigger n: same center,\nsmaller SE.\n4 x n -> SE / 2.\nPop sigma never changes.\nMore xbar close to mu."),
      card("Sampling dist of pbar", "Center: E(pbar) = p\nSE: sqrt( p(1-p) / n )\nShape: np >= 5 and\nn(1-p) >= 5.\nDecimals: 66% = .66\nCount cutoff: x/n first."),
      card("Internet: p .66, n 300", "np 198, n(1-p) 102: OK\nSE = sqrt(.66(.34)/300)\n!SE = .0273 (4 places)\nWithin .04: .62 to .70\nz = +/-1.47\n!.9292 - .0708 = .8584"),
      card("Sampling error", "Natural gap between a\nstatistic and parameter,\nsample to sample.\nNot a mistake.\nFinite pop correction:\nnot on the formula sheet;\nhandouts leave it out.")]),
    ("5 Ch 8 intervals", [
      card("CI structure", "Estimate +/- E\nE = (critical)(SE)\nWidth = 2E\nMean CI estimates mu.\nProportion CI estimates p.\nalpha = 1 - confidence"),
      card("z or t?", "sigma given -> z\nonly s given -> t\n!t even if n = 60\ndf = n - 1\nSmall n: needs normal pop.\nProbabilities (Ch 7): z.\nSample size: always z."),
      card("Verizon: z CI", "xbar 153, sd 46, n 85\n95%: z = 1.96\nSE = 46/sqrt(85) = 4.9894\nE = 9.7792\n!(143.22, 162.78)\nMonthly minutes per\nresidential user."),
      card("Reading the t-table", "Row: df = n - 1\nColumn: upper area a/2\n!.025, df 12 -> 2.179\nLower .05, df 50:\n!-1.676 (do not halve)\n90%, n 26: df 25\n!+/-1.708"),
      card("Aerospace: t CI", "n 18, xbar 13.56, s 7.8\n90%, df 17: t = 1.740\nSE = 7.8/sqrt(18)\n= 1.83848\nE = 3.19895\n!(10.36, 16.76) hours\nNormal pop: n < 30 OK."),
      card("More t practice", "xbar 25, s 3.5, n 60, 95%\ndf 59, t = 2.001\n!(24.096, 25.904)\nxbar 3.419, s .974, n 32\n90%, df 31, t = 1.696\n!(3.127, 3.711)"),
      card("Proportion CI", "pbar .39, n 87, 95%\nCounts 33.93, 53.07 OK\nSE = .0523, E = .1025\n!(.2875, .4925)\nSE uses pbar here.\n1-PropZInt needs whole x:\n33.93 -> do it by hand."),
      card("Min n: mean", "90%, sigma 4, E 1\n(1.645 x 4 / 1)^2\n= 43.2964\n!Round UP: 44\nNo sigma: pilot study\nor range / 4."),
      card("Min n: proportion", "98%: z = 2.33, E = .03\nPilot p* = .40:\n!1447.71 -> 1,448\nNo pilot, p* = .50:\n!1508.03 -> 1,509\nKey prints 1,508: wrong."),
      card("How pieces move", "More confidence: wider.\nLarger n: narrower.\nHalve E: 4 x n.\nLarger sigma: bigger n.\nE = .03, not 3.\nn always rounds UP."),
      card("Interpret a CI", "We are 95% confident the\npopulation mean (name it)\nis between L and U.\n95% of intervals made\nthis way contain mu.\nNot where 95% of\nindividual values fall.")]),
    ("6 Mix-ups", [
      card("One x or an average?", "One x: z = (x-mu)/sigma\nAverage: SE=sigma/sqrt(n)\n'randomly selected fish'\n-> one value.\n'mean of a sample of 50'\n-> xbar."),
      card("Middle 95%: which?", "Individuals:\nmu +/- 1.96 sigma\nSample means (Ch 7):\nmu +/- 1.96 sigma/sqrt(n)\nCI (Ch 8):\nxbar +/- 1.96 sigma/sqrt(n)"),
      card("p, pbar, or p*?", "'66% of ALL adults' = p\n-> Ch 7, SE uses p.\n'39% of a sample of 87'\n= pbar -> Ch 8 CI.\nSample size: p* pilot,\nor .50 with no pilot."),
      card("Normality checks", "Means: n >= 30, or the\npopulation is normal.\nProportions: np >= 5\nand n(1-p) >= 5.\nCI: check with pbar."),
      card("E means two things", "E(xbar), E(pbar):\nexpected value = center.\nE alone: margin of error\n= half the CI width.\n3 percentage points:\n!E = .03, not 3"),
      card("x means three things", "Ch 6: x = one raw value.\nProportion: x = a count,\npbar = x / n.\nxbar = a sample mean.\nCount cutoff: 210 of 300\n!-> pbar = .70"),
      card("Crit prob vs value", "Critical probabilities:\nareas a/2 and 1 - a/2\n!95%: .0250 and .9750\nCritical value: z or t\n!95%: +/-1.96\nalpha itself = .05"),
      card("One tail or two?", "CI: split alpha,\nupper area = alpha/2.\n'Lower-tail area .05':\nuse .05, do not halve.\nLower tail: t negative."),
      card("sigma (/N) vs s (/n-1)", "Population: divide by N.\nTI 1-Var Stats: sigma x\nSample: divide by n - 1.\nTI 1-Var Stats: Sx"),
      card("Working back from a CI", "center = (L + U) / 2\nE = (U - L) / 2\nwidth = U - L = 2E"),
      card("Trigger words 1", "'randomly selected' ->\nCh 6, one value.\n'percentile, top __%' ->\ninverse normal.\n'sample mean, average' ->\nCh 7, SE = sigma/sqrt(n).\n'sample proportion' ->\nCh 7, SE from p."),
      card("Trigger words 2", "'estimate, confident' ->\nCh 8 CI.\n'population SD' -> z\n's =' -> t, df = n - 1\n'how many to sample' ->\nmin n, round UP.\n'no pilot' -> p* = .50")]),
    ("7 Calculator / table", [
      card("Table vs calculator", "The key uses the z-table:\nz to 2 places, 4-place\nareas, 2.33 for 98%.\nCalculator keeps every\ndigit, so it can differ.\n!Enter the TABLE answer."),
      card("Biggest differences", "Table vs calculator:\nAcme pilot: 1448 / 1444\nAcme none: 1509 / 1504\nInternet: .8584 / .8564\nWithin $100: .6372/.6384\n98% CI low: 112.57/112.58\n25-45 days: .1865/.1866"),
      card("Match the table on TI", "1 Round z to 2 places.\n2 normalcdf(-1E99,z,0,1)\n3 Round area to 4.\n4 Between: round each\narea, then subtract.\n5 98%: type 2.33 by hand."),
      card("TI keys: normal", "2nd VARS (DISTR):\n2 normalcdf(lo,hi,mu,sd)\n3 invNorm(LEFT,mu,sd)\n4 invT(1 - a/2, df)\nxbar: sd = sigma/sqrt(n)\n-1E99 / 1E99 = infinity\nUse (-) for negatives."),
      card("TI keys: intervals", "STAT > TESTS:\n7 ZInterval (sigma)\n8 TInterval (Sx = s)\nA 1-PropZInt (whole x)\nInpt: Stats\nC-Level: 95 or .95\nMin n: type the formula."),
      card("Calculator traps", "invNorm wants LEFT area.\nTail setting: LEFT.\n1-PropZInt: x whole.\nZInterval: 2.3263 at 98%.\nClose sqrt( parentheses.\nPhone in bag in exam."),
      card("Rounding rules", "'Round final answer only':\nkeep digits to the end.\n'Round all calculations':\nround at every step.\nMin n: always UP.\nMatch decimals asked.\nPractice SE: 4 places."),
      card("Answer key errors", "Acme no pilot: 1,509\n(key 1,508: early round)\n67.72% above: use .3228\n(key typo .3328)\nGoldfish > 60: z = 0\n(key shows .5)\nVerizon: monthly minutes")]),
    ("8 Concepts / exam", [
      card("Vocabulary", "Parameter: population\n(mu, sigma, p).\nStatistic: sample\n(xbar, s, pbar).\nSE: SD of a sampling\ndistribution.\nUnbiased: E(statistic)\n= parameter."),
      card("Sampling methods 1", "Simple random: equal\nchance for every item.\nStratified: random from\nEACH subgroup.\nSystematic: random start,\nevery kth, k = N / n.\nCluster: randomly pick\nSOME groups."),
      card("Sampling methods 2", "Nonrandom:\nConvenience: easiest.\nJudgment: researcher\npicks 'representative'.\nQuota: fill targets\nwithout randomness.\nStratified vs quota:\nrandom vs not."),
      card("Survey errors", "Coverage: frame misses\ngroups.\nNonresponse: answerers\ndiffer from others.\nMeasurement: wording,\ninterviewer effects.\nSampling: natural\nsample-to-sample change."),
      card("Exam 2 format", "95 min, in class.\n50 Q, 59 pts + 3 bonus.\nQ1-12 multiple choice.\nQ13-50 fill in blank.\nShow work except 13.\nName on every page.\nLockDown Browser."),
      card("Allowed / not", "Allowed: calculator,\nz-table, t-table,\nformula sheet, no notes.\n!Ask before keeping this\n!program for the exam.\nLeaving exam page = 0.")])]

def refmenu():
    groups = references()
    while True:
        disp_clr()
        print("--- REFERENCE CARDS ---")
        for name, cards in groups:
            print(name)
        print("0 Main menu")
        s = input("> ").strip()
        if s == "0":
            return
        if s in [str(i) for i in range(1, len(groups) + 1)]:
            ACCENT[0] = TOPIC_COLORS[int(s) - 1]
            try:
                browse(groups[int(s) - 1][1])
            finally:
                ACCENT[0] = NAVY

def main():
    while True:
        disp_clr()
        print("=== EXAM2: CH 6-8 ===")
        print("1 Reference cards")
        print("2 Which formula?")
        print("3 Probability x/xbar/pbar")
        print("4 Percent -> cutoff")
        print("5 Critical z / t")
        print("6 Confidence interval")
        print("7 Minimum sample size")
        print("8 CI parts / std dev")
        print("0 Exit")
        s = input("> ").strip()
        if s == "0":
            break
        try:
            if s == "1": refmenu()
            elif s == "2": which()
            elif s == "3": probability()
            elif s == "4": cutoff()
            elif s == "5": critical()
            elif s == "6": interval()
            elif s == "7": sample_size()
            elif s == "8": more()
        except ValueError as e:
            disp_clr(); print(str(e)); input("ENTER: menu")
        except ZeroDivisionError:
            disp_clr(); print("Undefined: zero denominator")
            input("ENTER: menu")

main()
