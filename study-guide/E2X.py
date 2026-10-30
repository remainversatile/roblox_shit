# E2X - reference cards for EXAM2 (keep with EXAM2.py).
# Card: "Title|line\nline|label;numerator;denominator"
# Lines starting with ! are answers; ending with : are subheads.

def get(i):
  # Mix-ups
  if i == 0:
    return [
      "One x or an average?|One x: z = (x-mu)/sigma\nAverage: SE=sigma/sqrt(n)\n'randomly selected fish'\n-> one value.\n'mean of a sample of 50'\n-> xbar.",
      'Middle 95%: which?|Individuals:\nmu +/- 1.96 sigma\nSample means (Ch 7):\nmu +/- 1.96 sigma/sqrt(n)\nCI (Ch 8):\nxbar +/- 1.96 sigma/sqrt(n)',
      "p, pbar, or p*?|'66% of ALL adults' = p\n-> Ch 7, SE uses p.\n'39% of a sample of 87'\n= pbar -> Ch 8 CI.\nSample size: p* pilot,\nor .50 with no pilot.",
      'Normality checks|Means: n >= 30, or the\npopulation is normal.\nProportions: np >= 5\nand n(1-p) >= 5.\nCI: check with pbar.',
      'E means two things|E(xbar), E(pbar):\nexpected value = center.\nE alone: margin of error\n= half the CI width.\n3 percentage points:\n!E = .03, not 3',
      'x means three things|Ch 6: x = one raw value.\nProportion: x = a count,\npbar = x / n.\nxbar = a sample mean.\nCount cutoff: 210 of 300\n!-> pbar = .70',
      'Crit prob vs value|Critical probabilities:\nareas a/2 and 1 - a/2\n!95%: .0250 and .9750\nCritical value: z or t\n!95%: +/-1.96\nalpha itself = .05',
      "One tail or two?|CI: split alpha,\nupper area = alpha/2.\n'Lower-tail area .05':\nuse .05, do not halve.\nLower tail: t negative.",
      'sigma (/N) vs s (/n-1)|Population: divide by N.\nTI 1-Var Stats: sigma x\nSample: divide by n - 1.\nTI 1-Var Stats: Sx',
      'Working back from a CI|center = (L + U) / 2\nE = (U - L) / 2\nwidth = U - L = 2E',
      "Trigger words 1|'randomly selected' ->\nCh 6, one value.\n'percentile, top __%' ->\ninverse normal.\n'sample mean, average' ->\nCh 7, SE = sigma/sqrt(n).\n'sample proportion' ->\nCh 7, SE from p.",
      "Trigger words 2|'estimate, confident' ->\nCh 8 CI.\n'population SD' -> z\n's =' -> t, df = n - 1\n'how many to sample' ->\nmin n, round UP.\n'no pilot' -> p* = .50",
    ]
  # Calculator / table
  elif i == 1:
    return [
      'Table vs calculator|The key uses the z-table:\nz to 2 places, 4-place\nareas, 2.33 for 98%.\nCalculator keeps every\ndigit, so it can differ.\n!Enter the TABLE answer.',
      'Biggest differences|Table vs calculator:\nAcme pilot: 1448 / 1444\nAcme none: 1509 / 1504\nInternet: .8584 / .8564\nWithin $100: .6372/.6384\n98% CI low: 112.57/112.58\n25-45 days: .1865/.1866',
      'Match the table on TI|1 Round z to 2 places.\n2 normalcdf(-1E99,z,0,1)\n3 Round area to 4.\n4 Between: round each\narea, then subtract.\n5 98%: type 2.33 by hand.',
      'TI keys: normal|2nd VARS (DISTR):\n2 normalcdf(lo,hi,mu,sd)\n3 invNorm(LEFT,mu,sd)\n4 invT(1 - a/2, df)\nxbar: sd = sigma/sqrt(n)\n-1E99 / 1E99 = infinity\nUse (-) for negatives.',
      'TI keys: intervals|STAT > TESTS:\n7 ZInterval (sigma)\n8 TInterval (Sx = s)\nA 1-PropZInt (whole x)\nInpt: Stats\nC-Level: 95 or .95\nMin n: type the formula.',
      'Calculator traps|invNorm wants LEFT area.\nTail setting: LEFT.\n1-PropZInt: x whole.\nZInterval: 2.3263 at 98%.\nClose sqrt( parentheses.\nPhone in bag in exam.',
      "Rounding rules|'Round final answer only':\nkeep digits to the end.\n'Round all calculations':\nround at every step.\nMin n: always UP.\nMatch decimals asked.\nPractice SE: 4 places.",
      'Answer key errors|Acme no pilot: 1,509\n(key 1,508: early round)\n67.72% above: use .3228\n(key typo .3328)\nGoldfish > 60: z = 0\n(key shows .5)\nVerizon: monthly minutes',
    ]
  # Concepts / exam
  elif i == 2:
    return [
      'Vocabulary|Parameter: population\n(mu, sigma, p).\nStatistic: sample\n(xbar, s, pbar).\nSE: SD of a sampling\ndistribution.\nUnbiased: E(statistic)\n= parameter.',
      'Sampling methods 1|Simple random: equal\nchance for every item.\nStratified: random from\nEACH subgroup.\nSystematic: random start,\nevery kth, k = N / n.\nCluster: randomly pick\nSOME groups.',
      "Sampling methods 2|Nonrandom:\nConvenience: easiest.\nJudgment: researcher\npicks 'representative'.\nQuota: fill targets\nwithout randomness.\nStratified vs quota:\nrandom vs not.",
      'Survey errors|Coverage: frame misses\ngroups.\nNonresponse: answerers\ndiffer from others.\nMeasurement: wording,\ninterviewer effects.\nSampling: natural\nsample-to-sample change.',
      'Exam 2 format|95 min, in class.\n50 Q, 59 pts + 3 bonus.\nQ1-12 multiple choice.\nQ13-50 fill in blank.\nShow work except 13.\nName on every page.\nLockDown Browser.',
      'Allowed / not|Allowed: calculator,\nz-table, t-table,\nformula sheet, no notes.\n!Ask before keeping this\n!program for the exam.\nLeaving exam page = 0.',
    ]
  return []
