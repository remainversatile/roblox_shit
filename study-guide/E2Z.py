# E2Z - reference cards for EXAM2 (keep with EXAM2.py).
# Card: "Title|line\nline|label;numerator;denominator"
# Lines starting with ! are answers; ending with : are subheads.

def get(i):
  # Z-score sheet
  if i == 0:
    return [
      'One value (Ch 6)|Center mu, spread sigma.\nOne person, fish, bill.|z;x - mu;sigma',
      'Sample mean (Ch 7)|SE = sigma / sqrt(n)\nAverage of n items.\nNever plain sigma.|z xbar;xbar - mu;sigma / sqrt(n)',
      'Sample prop (Ch 7)|SE uses KNOWN p.\nCount given: pbar = x/n.|z pbar;pbar - p;sqrt( p(1-p) / n )',
      'Backwards: value from z|x = mu + (z)(sigma)\nmu = x - (z)(sigma)\nxbar cutoff:\nmu + (z)(sigma/sqrt(n))\nBelow-mean cutoff: z < 0\nso x comes out below mu.',
      'What z means|z = SDs from the center.\nz = 1.5: 1.5 SD above.\nz < 0: below, left < .5\nz > 0: above, left > .5\nz = 0: mean, area .5000\n68/95/99.7: 1, 2, 3 SD\nP(X = a) = 0 exactly.',
      'Reading the z-table|Table = area to the LEFT.\nRound z to 2 places first.\nRow: ones + tenths (1.2)\nColumn: hundredths (.04)\n!z = 1.24 -> .8925\nNegative: row -1.7,\ncol .05 -> -1.75 = .0401',
      'Area rules|Below a: left(a)\nAbove a: 1 - left(a)\nBetween: left(b) - left(a)\nOutside: 1 - between\nWithin +/-d of center:\nleft(+z) - left(-z)\n!Subtract AREAS, not z.',
      'Inverse: % to cutoff|1 Wording -> LEFT area\n2 Find area INSIDE table\n3 Closest cell gives z\n4 x = mu + (z)(sigma)\nExactly halfway: average\n!.95 -> 1.645 (midpoint)',
      'Wording -> LEFT area|Bottom 20% -> .20\nTop 10% -> .90\n67.72% above x -> .3228\nx above 86.65% -> .8665\nMiddle 95% -> .025, .975\n!Top __% means 1 - __.',
      'Percentile z values|.01 -2.33, .99 2.33\n.025 -1.96, .975 1.96\n.05 -1.645, .95 1.645\n.10 -1.28, .90 1.28\n.20 -0.84, .80 0.84\n.25 -0.67, .75 0.67\n.30 -0.52, .70 0.52\n.40 -0.25, .60 0.25',
      'z -> areas|z: left, right, within\n1.00: .8413 .1587 .6826\n1.28: .8997 .1003 .7994\n1.645: .9500 .0500 .9000\n1.96: .9750 .0250 .9500\n2.33: .9901 .0099 .9802\n2.576: .9950 .0050 .9900\n3.00: .9987 .0013 .9974',
      'Critical z values|Conf: 1-a/2 -> z\n80%: .9000 -> 1.28\n85%: .9250 -> 1.44\n90%: .9500 -> 1.645\n95%: .9750 -> 1.96\n98%: .9900 -> 2.33\n99%: .9950 -> 2.576',
      'z mistakes|Forgot 1 - for above.\nSubtracted z, not areas.\nsigma used for xbar.\npbar used in Ch 7 SE.\nLooked up % not LEFT.\nDid not round z to 2.\n.0040 = .40%, not 4%.\nPast +/-3.49: ~0 or ~1.',
      'z on the TI-84|Left area of z:\nnormalcdf(-1E99,z,0,1)\nFrom raw values:\nnormalcdf(lo,hi,mu,sd)\nz from a left area:\ninvNorm(area,0,1)\nE in 1E99: 2nd , (EE)\nRound z to 2 for table.',
    ]
  # Formula sheet
  elif i == 1:
    return [
      'Std dev: population|Then take the square root.\nSheet prints xbar and n;\nfor a population that is\nmu and N.|sigma^2;sum (xi - xbar)^2;N',
      'Std dev: sample|Then take the square root.\nShortcut on sheet:\n[sum x^2 - (sum x)^2/n]\ndivided by n - 1.|s^2;sum (xi - xbar)^2;n - 1',
      'Critical probability|Areas for CI cutoffs:\n!alpha/2 & 1 - alpha/2\nalpha = 1 - confidence\n95%: .0250 and .9750',
      'z-score (raw data)|One individual value.|z;x - mu;sigma',
      'z to raw score / mean|z-score to a raw score:\n!x = mu + (z)(sigma)\nz-score to a pop mean:\n!mu = x - (z)(sigma)',
      'Expected value of xbar|!E(xbar) = mu xbar = mu\nCenter of the sampling\ndistribution of xbar.\nxbar is unbiased for mu.',
      'z-score (sample mean)|sigma xbar = sigma/sqrt(n)|z xbar;xbar - mu;sigma xbar',
      'SE of mean (sigma known)|Standard error of the mean.|sigma xbar;sigma;sqrt(n)',
      'CI for mu (sigma known)|CI estimate for mu:\n!mu = xbar +/-\n!(Z a/2)(sigma / sqrt(n))\nPopulation sigma given.',
      'SE of mean (sigma unkn.)|Uses the sample s.|S xbar;s;sqrt(n)',
      'CI for mu (sigma unkn.)|CI estimate for mu:\n!mu = xbar +/-\n!(t a/2)(s / sqrt(n))\ndf = n - 1. a/2 = alpha/2',
      'Sample size for mu|= ((z a/2)(sigma) / E)^2\nAlways round UP.|n;[ (z a/2)(sigma) ]^2;E^2',
      'Sample proportion|x = count of successes.|pbar;x;n',
      'pbar center, normality|Expected value of pbar:\n!E(pbar) = p\nNormality requirements:\n!np >= 5, n(1 - p) >= 5',
      'z-score (sample prop)|sigma pbar uses known p.|z pbar;pbar - p;sigma pbar',
      'SE of the proportion|= sqrt( p(1 - p) / n )\nUses population p.|sigma pbar;sqrt[ p(1 - p) ];sqrt(n)',
      'CI estimate for p|!p = pbar +/- (Z a/2) x\n!sqrt( pbar(1-pbar) / n )\np unknown: SE uses pbar.',
      'Sample size for p|p* = pilot, else .50\nAlways round UP.|n;(z a/2)^2 p*(1 - p*);E^2',
    ]
  return []
