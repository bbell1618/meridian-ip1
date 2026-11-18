"""Meridian IP-1: a HYPOTHETICAL surgical irrigation pump console (not a real product, no third-party design data).
Parametric CAD in CadQuery. Units: mm. X = width, Y = depth (front panel at +Y), Z = up.
Run: python3 device.py [board.step]  -> out/meridian_ip1.step, out/meridian_ip1.glb, out/parts.json
Sub-systems (the same kinds of parts a real fluid-management console uses):
  - NEMA 17 stepper motor + planetary gearbox driving a 3-roller peristaltic pump head
  - solenoid pinch valve on the outlet line
  - two in-line pressure transducers (inlet and outlet), optical air-in-line (bubble) sensor
  - main controller PCB (pcb/ip1_main.kicad_pcb, 100 x 80 mm, 4 layers)
  - 24 V DC inlet, cooling fan, display module, keypad, wiring harnesses
"""
import math, os, sys, json
import cadquery as cq

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

W, D, H = 240.0, 180.0, 160.0      # enclosure outer
T = 3.0                            # wall
SPLIT = 30.0                       # tray / cover split height
FY = D / 2                         # front face y
PCB_W, PCB_D, PCB_T = 100.0, 80.0, 1.6
PCB_X, PCB_Y, PCB_Z = 55.0, -30.0, T + 8.0   # board centre and underside height
HOLES = [(4, 4), (96, 20), (4, 76), (96, 76)]  # board mounting holes (board coords, mm from top-left)
PUMP_X, PUMP_Z = -62.0, 108.0
ROTOR_R, ROLLER_R = 24.0, 7.0
TUBE_OD, TUBE_ID = 6.4, 3.2
RR = ROTOR_R + ROLLER_R - 1.5      # tube centre-line radius in the raceway
TUBE_Y = FY + 13.0
XIN, XOUT = PUMP_X - RR, PUMP_X + RR

C = dict(shell=(0.87, 0.89, 0.91), base=(0.23, 0.25, 0.28), accent=(0.04, 0.42, 0.50), steel=(0.72, 0.74, 0.77),
         dark=(0.10, 0.11, 0.13), tube=(0.93, 0.96, 0.99), pcb=(0.04, 0.33, 0.18), glass=(0.06, 0.10, 0.14),
         blue=(0.14, 0.33, 0.72), red=(0.74, 0.18, 0.14), white=(0.96, 0.96, 0.96), gold=(0.84, 0.66, 0.22),
         wire_r=(0.80, 0.10, 0.10), wire_k=(0.08, 0.08, 0.08), wire_y=(0.90, 0.75, 0.10), wire_b=(0.15, 0.30, 0.80))
col = lambda k, a=1.0: cq.Color(*C[k], a)

# ---------- primitives placed in device coordinates (no workplane sign puzzles) ----------
def box(x, y, z, sx, sy, sz):            # centred at (x, y), sitting from z to z+sz
    return cq.Workplane("XY").box(sx, sy, sz, centered=(True, True, False)).translate((x, y, z))
def cyl_z(x, y, z0, z1, r):
    return cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((x, y, z0))
def cyl_y(x, z, y0, y1, r):              # axis along Y from y0 to y1
    return cq.Workplane("XY").circle(r).extrude(y1 - y0).rotate((0, 0, 0), (1, 0, 0), -90).translate((x, y0, z))
def box_y(x, z, y0, y1, sx, sz):         # box centred on (x, z), spanning y0..y1
    return cq.Workplane("XY").box(sx, y1 - y0, sz).translate((x, (y0 + y1) / 2, z))
def wire(points, r):                     # round cable through points: cylinders + ball joints (robust, no sweeps)
    out = None
    for a, b in zip(points, points[1:]):
        v = cq.Vector(*b) - cq.Vector(*a)
        seg = cq.Solid.makeCylinder(r, v.Length, cq.Vector(*a), v.normalized())
        ball = cq.Solid.makeSphere(r, cq.Vector(*b))
        for s in (seg, ball):
            out = cq.Workplane("XY").add(s) if out is None else out.add(s)
    return out.combine()
def bez(p0, p1, p2, p3, n=14):
    pts = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        pts.append(tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3)))
    return pts
def b2d(bx, by, dz=0.0):                 # board coordinates (mm from top-left, y down) -> device coordinates on the board top
    return (PCB_X - PCB_W / 2 + bx, PCB_Y + PCB_D / 2 - by, PCB_Z + PCB_T + dz)

# ---------- enclosure ----------
def base_tray():
    b = cq.Workplane("XY").box(W, D, SPLIT, centered=(True, True, False)).edges("|Z").fillet(12).faces(">Z").shell(-T)
    for bx, by in HOLES:
        x, y, _ = b2d(bx, by)
        b = b.union(cyl_z(x, y, T - 0.2, PCB_Z, 3.5).cut(cyl_z(x, y, T + 2, PCB_Z + 1, 1.25)))
    for sx in (-1, 1):
        for sy in (-1, 1):
            b = b.union(cyl_z(sx * (W / 2 - 24), sy * (D / 2 - 24), -4, 0.2, 9))
    return b.cut(cyl_y(XOUT, 13, FY - T - 2, FY + 2, 13.4))                           # pinch-valve solenoid passes through the tray front

def top_cover():
    c = cq.Workplane("XY").box(W, D, H - SPLIT, centered=(True, True, False)).translate((0, 0, SPLIT)).edges("|Z").fillet(12).edges(">Z").fillet(7)
    c = c.faces("<Z").shell(-T)
    c = c.cut(cyl_y(PUMP_X, PUMP_Z, FY - T - 2, FY + 2, 21.5))                       # gearbox pilot bore
    c = c.cut(box_y(52, 118, FY - T - 2, FY + 2, 96, 54))                             # display window
    for i in range(4):
        c = c.cut(box_y(16 + i * 24, 76, FY - T - 2, FY + 2, 17, 9))                  # keypad
    for i in range(-3, 4):
        c = c.cut(box_y(60, 106 + i * 7, -FY - 2, -FY + T + 2, 46, 3))                 # rear fan grill
    c = c.cut(cyl_y(-70, 60, -FY - 2, -FY + T + 2, 6.2))                              # rear DC inlet
    for x in (XIN, XOUT):                                                             # sensor cable pass-throughs
        c = c.cut(cyl_y(x, 40, FY - T - 2, FY + 2, 3.2))
    return c

# ---------- pump head (outside the front panel) ----------
def pump_housing():
    h = cyl_y(PUMP_X, PUMP_Z, FY, FY + 26, ROTOR_R + 13)
    h = h.cut(cyl_y(PUMP_X, PUMP_Z, FY + 3, FY + 27, ROTOR_R + ROLLER_R + 1.2))       # raceway pocket, 3 mm back plate left
    h = h.cut(cyl_y(PUMP_X, PUMP_Z, FY - 1, FY + 4, 9))
    for x in (XIN, XOUT):
        h = h.cut(box_y(x, PUMP_Z - 24, FY + 3, FY + 27, TUBE_OD + 1.6, 34))          # tube entry / exit slots
    return h

def pump_rotor():
    r = cyl_y(PUMP_X, PUMP_Z, FY + 4, FY + 24, 8.5)
    for y0 in (FY + 5, FY + 20.5):
        plate = cq.Workplane("XY").polygon(3, 2 * ROTOR_R + 10).extrude(2.5).edges("|Z").fillet(7).rotate((0, 0, 0), (0, 0, 1), 90)
        r = r.union(plate.rotate((0, 0, 0), (1, 0, 0), -90).translate((PUMP_X, y0, PUMP_Z)))
    return r

def pump_rollers():
    w = None
    for k in range(3):
        a = math.radians(90 + 120 * k)
        x, z = PUMP_X + ROTOR_R * math.cos(a), PUMP_Z + ROTOR_R * math.sin(a)
        s = cyl_y(x, z, FY + 7.6, FY + 20.4, ROLLER_R).cut(cyl_y(x, z, FY + 7, FY + 21, 2))
        s = s.union(cyl_y(x, z, FY + 5, FY + 23, 1.9))                                 # axle pin
        w = s if w is None else w.union(s)
    return w

def pump_tube():
    pts = [(XIN, TUBE_Y, -2.0), (XIN, TUBE_Y, PUMP_Z)]
    for i in range(1, 18):
        a = math.pi - i * math.pi / 18
        pts.append((PUMP_X + RR * math.cos(a), TUBE_Y, PUMP_Z + RR * math.sin(a)))
    pts += [(XOUT, TUBE_Y, PUMP_Z), (XOUT, TUBE_Y, -2.0)]
    return wire(pts, TUBE_OD / 2)

# ---------- motor ----------
def stepper_gearmotor():
    yi = FY - T
    m = cyl_y(PUMP_X, PUMP_Z, yi - 31, yi, 18)                                        # planetary gearbox 36 mm dia
    m = m.union(cyl_y(PUMP_X, PUMP_Z, yi - 0.1, yi + 2.5, 11))                        # pilot boss
    body = box_y(PUMP_X, PUMP_Z, yi - 31 - 48, yi - 31, 42.3, 42.3).edges("|Y").chamfer(4)   # NEMA 17 body
    m = m.union(body)
    m = m.union(box_y(PUMP_X, PUMP_Z, yi - 31 - 33, yi - 31 - 15, 43.2, 43.2).edges("|Y").chamfer(4.4).cut(box_y(PUMP_X, PUMP_Z, yi - 90, yi - 20, 41.6, 41.6)))  # lamination stack band
    m = m.union(box_y(PUMP_X, PUMP_Z - 24, yi - 31 - 48, yi - 31 - 36, 16, 7))        # connector block
    m = m.union(cyl_y(PUMP_X, PUMP_Z, yi, FY + 24, 4))                                # output shaft into the rotor
    return m

def motor_bracket():
    yb = FY - T - 31
    b = box_y(PUMP_X, PUMP_Z - 36, yb - 3, yb, 64, 130).cut(cyl_y(PUMP_X, PUMP_Z, yb - 4, yb + 1, 18.6))
    b = b.cut(box_y(PUMP_X, PUMP_Z - 78, yb - 4, yb + 1, 36, 30))
    b = b.union(box(PUMP_X, yb - 20, T, 64, 40, 3))
    for sx in (-1, 1):
        b = b.union(box(PUMP_X + sx * 30.5, yb - 12, T, 3, 24, 40))
    return b

# ---------- fluid path parts on the front, below the pump ----------
def pinch_valve():
    v = box(XOUT, TUBE_Y, 4, 26, 22, 18).edges("|Z").fillet(3)                        # pinch block
    v = v.cut(cyl_z(XOUT, TUBE_Y, 3, 23, TUBE_OD / 2 + 0.4)).cut(box(XOUT, TUBE_Y + 8, 3, TUBE_OD + 0.8, 16, 20))
    v = v.union(cyl_y(XOUT, 13, FY - T - 38, FY + 2, 13))                              # solenoid coil can through the panel
    v = v.union(cyl_y(XOUT, 13, FY - T - 44, FY - T - 38, 6))                          # plunger end cap
    return v

def pressure_sensor(x, z):
    s = box(x, TUBE_Y, z, 17, 15, 20).edges("|Z").fillet(2)
    s = s.cut(cyl_z(x, TUBE_Y, z - 1, z + 21, TUBE_OD / 2 + 0.3))
    s = s.union(cyl_y(x, z + 10, FY, TUBE_Y - 5, 5.5))                                 # port to the panel
    s = s.union(cyl_y(x, z + 10, TUBE_Y + 7, TUBE_Y + 10, 6))                          # diaphragm cap
    return s

def bubble_sensor(x, z):
    s = box(x, TUBE_Y, z, 22, 18, 13).edges("|Z").fillet(2)
    s = s.cut(box(x, TUBE_Y + 5, z - 1, TUBE_OD + 0.6, 12, 15)).cut(cyl_z(x, TUBE_Y, z - 1, z + 14, TUBE_OD / 2 + 0.3))
    s = s.union(box_y(x, z + 6.5, FY, TUBE_Y - 8, 12, 8))
    return s

# ---------- electronics and panel parts ----------
def pcb_placeholder():
    b = box(PCB_X, PCB_Y, PCB_Z, PCB_W, PCB_D, PCB_T)
    for bx, by in HOLES:
        x, y, _ = b2d(bx, by)
        b = b.cut(cyl_z(x, y, PCB_Z - 1, PCB_Z + 3, 1.6))
    return b

def display():
    d = box_y(52, 118, FY - T - 9, FY - T, 104, 62)                                    # module frame
    d = d.union(box_y(52, 118, FY - T - 0.1, FY - 0.6, 95, 53))                        # glass in the window
    d = d.union(box_y(52, 118, FY - T - 11, FY - T - 9, 108, 66))                      # display driver board
    return d

def keypad():
    k = None
    for i in range(4):
        s = box_y(16 + i * 24, 76, FY - T - 4, FY + 1.6, 16, 8).edges("|Y").fillet(2)
        k = s if k is None else k.union(s)
    return k.union(box_y(52, 76, FY - T - 6, FY - T - 4, 100, 16))

def fan():
    y0 = -FY + T
    f = box_y(60, 106, y0, y0 + 15, 50, 50).edges("|Y").fillet(4).cut(cyl_y(60, 106, y0 - 1, y0 + 16, 23.5))
    f = f.union(cyl_y(60, 106, y0 + 1, y0 + 14, 10))
    for k in range(7):
        blade = box_y(60 + 16, 106, y0 + 3, y0 + 12, 13, 2.2).rotate((60, 0, 106), (60, 1, 106), 360 / 7 * k)
        f = f.union(blade)
    return f

def dc_inlet():
    j = cyl_y(-70, 60, -FY - 3, -FY + T + 20, 6).cut(cyl_y(-70, 60, -FY - 4, -FY + 6, 3.2))
    j = j.union(cyl_y(-70, 60, -FY - 3, -FY - 1, 8)).union(cyl_y(-70, 60, -FY - 3.5, -FY + 5, 1.2))
    return j

def harness_power():      # DC inlet -> J1 (24 V IN), the connector the video is about
    j = b2d(6.5, 60, 14)
    return wire(bez((-70, -FY + T + 20, 60), (-70, -40, 60), (j[0] - 30, j[1], 50), j), 2.4)
def harness_motor():      # stepper -> J3
    j = b2d(6.5, 19, 14)
    return wire(bez((PUMP_X, FY - T - 79, PUMP_Z - 27), (PUMP_X, 0, 30), (j[0] - 25, j[1], 45), j), 2.6)
def harness_valve():      # pinch valve -> J4
    j = b2d(22, 6.5, 14)
    return wire(bez((XOUT, FY - T - 44, 13), (XOUT, 20, 14), (j[0], j[1] + 20, 34), j), 1.6)
def harness_sensors():    # pressure x2 + bubble -> J5 / J6 / J7
    out = None
    for (x0, z0, bx) in ((XIN, 40, 67), (XOUT, 40, 81), (XOUT, 40, 55)):
        j = b2d(bx, 5, 12)
        w = wire(bez((x0, FY - T, z0), (x0, 50, z0 + 10), (j[0], j[1] + 35, 50), j), 1.3)
        out = w if out is None else out.union(w)
    return out

# ---------- JST VH-style wire-to-board headers (the KiCad library has no 3D model for these) ----------
VH = [("J1", 6.5, 62.0, 90, 2), ("J3", 6.5, 25.0, 90, 4), ("J4", 20.0, 6.5, 0, 2)]     # ref, pin-1 board x, y, rotation, pins
def lbox(px, py, rot, xl0, xl1, yl0, yl1, z0, z1):
    """Box given in footprint-local coordinates (x along the pin row, y down, z up from the board top) -> device coordinates."""
    if rot == 0: bx0, bx1, by0, by1 = px + xl0, px + xl1, py + yl0, py + yl1
    else:        bx0, bx1, by0, by1 = px + yl0, px + yl1, py - xl1, py - xl0
    x0, y0, zt = b2d(bx0, by1); x1, y1, _ = b2d(bx1, by0)
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, zt + z0))
def vh_headers():
    body = pins = None
    for ref, px, py, rot, n in VH:
        l0, l1 = -1.95, (n - 1) * 3.96 + 1.95
        for b in (lbox(px, py, rot, l0, l1, -3.8, 4.9, 0, 2.0), lbox(px, py, rot, l0, l1, -3.8, -2.6, 0, 9.4), lbox(px, py, rot, l0, l1, 3.9, 4.9, 0, 6.0),
                  lbox(px, py, rot, l0, l0 + 1.0, -3.8, 4.9, 0, 7.0), lbox(px, py, rot, l1 - 1.0, l1, -3.8, 4.9, 0, 7.0)):
            body = b if body is None else body.union(b)
        for i in range(n):
            p = lbox(px, py, rot, i * 3.96 - 0.57, i * 3.96 + 0.57, -0.57, 0.57, -3.3, 7.6)
            pins = p if pins is None else pins.union(p)
    return body, pins

def build(pcb_step=None):
    a = cq.Assembly(name="Meridian_IP1")
    add = lambda shape, name, c, alpha=1.0: a.add(shape, name=name, color=col(c, alpha))
    add(base_tray(), "base_tray", "base")
    add(top_cover(), "top_cover", "shell")
    add(pump_housing(), "pump_housing", "accent")
    add(pump_rotor(), "pump_rotor", "steel")
    add(pump_rollers(), "pump_rollers", "white")
    add(pump_tube(), "pump_tube", "tube", 0.8)
    add(stepper_gearmotor(), "stepper_gearmotor", "dark")
    add(motor_bracket(), "motor_bracket", "steel")
    add(pinch_valve(), "solenoid_pinch_valve", "blue")
    add(pressure_sensor(XIN, 42), "pressure_sensor_inlet", "gold")
    add(pressure_sensor(XOUT, 50), "pressure_sensor_outlet", "gold")
    add(bubble_sensor(XOUT, 31), "bubble_sensor", "red")
    add(display(), "display", "glass")
    add(keypad(), "keypad", "accent")
    add(fan(), "fan", "dark")
    add(dc_inlet(), "dc_inlet_24v", "steel")
    add(harness_power(), "harness_24v_power", "wire_r")
    add(harness_motor(), "harness_motor", "wire_k")
    add(harness_valve(), "harness_valve", "wire_b")
    add(harness_sensors(), "harness_sensors", "wire_y")
    vb, vp = vh_headers()
    add(vb, "vh_header_bodies", "white"); add(vp, "vh_header_pins", "steel")
    if pcb_step and os.path.exists(pcb_step):
        # KiCad STEP export keeps sheet coordinates: board spans x 100..200, y -140..-60, underside at z = 0
        a.add(cq.importers.importStep(pcb_step), name="main_controller_pcb", color=col("pcb"), loc=cq.Location(cq.Vector(PCB_X - 150.0, PCB_Y + 100.0, PCB_Z)))
    elif pcb_step != "none":
        add(pcb_placeholder(), "main_controller_pcb", "pcb")
    return a

if __name__ == "__main__":
    pcb = sys.argv[1] if len(sys.argv) > 1 else None
    asm = build(pcb)
    asm.save(os.path.join(OUT, "meridian_ip1.step"))
    names = [c.name for c in asm.children]
    json.dump(names, open(os.path.join(OUT, "parts.json"), "w"))
    build("none").save(os.path.join(OUT, "meridian_ip1_mech.glb"), tolerance=0.08, angularTolerance=0.25)   # mechanics only; the board is a separate full-colour GLB
    print("parts:", len(names), names)
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)))
