# E2C - reference cards for EXAM2 (keep with EXAM2.py).
# Card: "Title|line\nline|label;numerator;denominator"
# Lines starting with ! are answers; ending with : are subheads.

def get(i):
  # Ch 6 normal
  if i == 0:
    return [
      'Normal facts|Bell-shaped, symmetric.\nMean = median = mode.\nTotal area = 1.\nEach side of mu = .50.\nStandard normal: 0 and 1.\nContinuous: P(X = a) = 0\nP(X < a) = P(X <= a)\nExact 95%: 1.96, not 2.',
      'Goldfish: mu 60, sd 20|More than 80 days:\nz = (80 - 60)/20 = 1.00\n1 - .8413\n!= .1587\nMore than 60 days:\nz = 0\n!= .50',
      'Goldfish: between, tail|25 to 45 days:\nz = -1.75 and -0.75\n.2266 - .0401\n!= .1865\nWithin 7 days:\nz = -2.65\n!= .0040 = .40%',
      'Goldfish cutoffs|Top 10%: z = 1.28\n!60 + 1.28(20) = 85.6\nBottom 20%: z = -0.84\n!60 - 0.84(20) = 43.2\nMiddle 95%: z = +/-1.96\n!20.80 to 99.20 days',
      'Unknown mean / x|86.65% below x = 449,\nsigma 36: z = 1.11\n!mu = 449 - 1.11(36)\n!= 409.04\n67.72% ABOVE x: .3228\nz = -0.46, mu 3.58, 1.04\n!x = 3.1016',
      '95% of values vs CI|Middle 95% of fish:\nmu +/- 1.96(sigma)\n95% CI for a mean:\nxbar +/- 1.96(SE)\nSame 1.96, different\nquestion.',
    ]
  # Ch 7 sampling
  elif i == 1:
    return [
      'Sampling dist of xbar|Center: E(xbar) = mu\nSpread: sigma / sqrt(n)\nShape: normal if pop is\nnormal; else n >= 30\n(Central Limit Theorem).\nThe population itself\ndoes not become normal.',
      'Credit card: setup|mu 2864, sd 775, n 50\nSE = 775 / sqrt(50)\n!SE = 109.6016\nn >= 30: approx normal.\nNever divide by 775 here.',
      'Credit card: answers|xbar > 3000: z = 1.24\n!1 - .8925 = .1075\nWithin $100 of mu:\nz = +/-0.91\n!.8186 - .1814 = .6372\nn = 100: SE = 77.5\n!z +/-1.29: .8030',
      'Changing n|Bigger n: same center,\nsmaller SE.\n4 x n -> SE / 2.\nPop sigma never changes.\nMore xbar close to mu.',
      'Sampling dist of pbar|Center: E(pbar) = p\nSE: sqrt( p(1-p) / n )\nShape: np >= 5 and\nn(1-p) >= 5.\nDecimals: 66% = .66\nCount cutoff: x/n first.',
      'Internet: p .66, n 300|np 198, n(1-p) 102: OK\nSE = sqrt(.66(.34)/300)\n!SE = .0273 (4 places)\nWithin .04: .62 to .70\nz = +/-1.47\n!.9292 - .0708 = .8584',
      'Sampling error|Natural gap between a\nstatistic and parameter,\nsample to sample.\nNot a mistake.\nFinite pop correction:\nnot on the formula sheet;\nhandouts leave it out.',
    ]
  # Ch 8 intervals
  elif i == 2:
    return [
      'CI structure|Estimate +/- E\nE = (critical)(SE)\nWidth = 2E\nMean CI estimates mu.\nProportion CI estimates p.\nalpha = 1 - confidence',
      'z or t?|sigma given -> z\nonly s given -> t\n!t even if n = 60\ndf = n - 1\nSmall n: needs normal pop.\nProbabilities (Ch 7): z.\nSample size: always z.',
      'Verizon: z CI|xbar 153, sd 46, n 85\n95%: z = 1.96\nSE = 46/sqrt(85) = 4.9894\nE = 9.7792\n!(143.22, 162.78)\nMonthly minutes per\nresidential user.',
      'Reading the t-table|Row: df = n - 1\nColumn: upper area a/2\n!.025, df 12 -> 2.179\nLower .05, df 50:\n!-1.676 (do not halve)\n90%, n 26: df 25\n!+/-1.708',
      'Aerospace: t CI|n 18, xbar 13.56, s 7.8\n90%, df 17: t = 1.740\nSE = 7.8/sqrt(18)\n= 1.83848\nE = 3.19895\n!(10.36, 16.76) hours\nNormal pop: n < 30 OK.',
      'More t practice|xbar 25, s 3.5, n 60, 95%\ndf 59, t = 2.001\n!(24.096, 25.904)\nxbar 3.419, s .974, n 32\n90%, df 31, t = 1.696\n!(3.127, 3.711)',
      'Proportion CI|pbar .39, n 87, 95%\nCounts 33.93, 53.07 OK\nSE = .0523, E = .1025\n!(.2875, .4925)\nSE uses pbar here.\n1-PropZInt needs whole x:\n33.93 -> do it by hand.',
      'Min n: mean|90%, sigma 4, E 1\n(1.645 x 4 / 1)^2\n= 43.2964\n!Round UP: 44\nNo sigma: pilot study\nor range / 4.',
      'Min n: proportion|98%: z = 2.33, E = .03\nPilot p* = .40:\n!1447.71 -> 1,448\nNo pilot, p* = .50:\n!1508.03 -> 1,509\nKey prints 1,508: wrong.',
      'How pieces move|More confidence: wider.\nLarger n: narrower.\nHalve E: 4 x n.\nLarger sigma: bigger n.\nE = .03, not 3.\nn always rounds UP.',
      'Interpret a CI|We are 95% confident the\npopulation mean (name it)\nis between L and U.\n95% of intervals made\nthis way contain mu.\nNot where 95% of\nindividual values fall.',
    ]
  return []
