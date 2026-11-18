"""Add net classes to the router input: wide tracks for power (0.5 mm) and motor phases (0.4 mm)."""
s = open('ip1_main.dsn').read()
POWER = ['+24V', '+24V_IN', '+5V', 'BUCK_SW', 'FAN_N', 'VALVE_N', 'VFUSE']
MOTOR = ['MOT_A1', 'MOT_A2', 'MOT_B1', 'MOT_B2', 'SENSE_A', 'SENSE_B']
i = s.index('(class kicad_default'); j = s.index('(circuit', i); k = s.index('\n    )', j) + 6
names = s[i:j][len('(class kicad_default ""'):].split()
keep = [n for n in names if n.strip('"') not in POWER + MOTOR]
via = '"Via[0-3]_600:300_um"'
cls = lambda name, nets, w: f'    (class {name} {" ".join(nets)}\n      (circuit\n        (use_via {via})\n      )\n      (rule\n        (width {w})\n        (clearance 200.1)\n      )\n    )\n'
s = s[:i] + '(class kicad_default "" ' + ' '.join(keep) + '\n      ' + s[j:k] + '\n' + cls('power', POWER, 500) + cls('motor', MOTOR, 400) + s[k:]
import re
# route GND and +3V3 pad-to-pad as ordinary nets; the planes, plane vias and pours are added on top afterwards
s, n = re.subn(r'\(plane "?(\+3V3|GND)"? \(polygon[^)]*\)\)\s*', '', s)
assert n == 2
open('ip1_main_r.dsn', 'w').write(s)
