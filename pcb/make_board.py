#!/usr/bin/python3
"""Build the KiCad 7 board from board_def.py: footprints from the stock KiCad libraries, nets, outline, planes.
Usage: /usr/bin/python3 make_board.py place   -> ip1_main.kicad_pcb (unrouted) + ip1_main.dsn + checks
       /usr/bin/python3 make_board.py finish  -> import ip1_main.ses, widen power tracks, pour planes, DRC, save
"""
import sys, os, json, collections, math, re
import pcbnew
from board_def import PARTS, NETS, NC, POWER_NETS, BOARD_W, BOARD_H

HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(HERE, "ip1_main.kicad_pcb")
FPDIR = "/usr/share/kicad/footprints"
mm = pcbnew.FromMM
OX, OY = 100.0, 60.0     # board origin on the KiCad sheet

def pt(x, y): return pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))

def add_zone(b, layer, netname):
    z = pcbnew.ZONE(b); z.SetLayer(layer); z.SetNetCode(b.GetNetsByName()[netname].GetNetCode())
    o = z.Outline(); o.NewOutline()
    for x, y in ((0.5, 0.5), (BOARD_W - 0.5, 0.5), (BOARD_W - 0.5, BOARD_H - 0.5), (0.5, BOARD_H - 0.5)): o.Append(mm(OX + x), mm(OY + y))
    z.SetLocalClearance(mm(0.25)); z.SetMinThickness(mm(0.2))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL); z.SetThermalReliefGap(mm(0.3)); z.SetThermalReliefSpokeWidth(mm(0.5))
    b.Add(z); return z

def place():
    b = pcbnew.BOARD()
    b.SetCopperLayerCount(4)
    ds = b.GetDesignSettings()
    ds.SetBoardThickness(mm(1.6))
    ds.m_MinClearance = mm(0.15); ds.m_TrackMinWidth = mm(0.15); ds.m_ViasMinSize = mm(0.5); ds.m_MinThroughDrill = mm(0.3)
    ds.m_CopperEdgeClearance = mm(0.3)
    # nets
    netmap = {}
    for name in NETS:
        ni = pcbnew.NETINFO_ITEM(b, name); b.Add(ni); netmap[name] = ni
    pad2net = {}
    for name, pads in NETS.items():
        for p in pads:
            assert p not in pad2net, f"pad {p} on two nets: {pad2net[p]} and {name}"
            pad2net[p] = name
    # footprints
    problems = []
    for ref, (fp, val, x, y, rot) in PARTS.items():
        lib, name = fp.split(":")
        f = pcbnew.FootprintLoad(os.path.join(FPDIR, lib + ".pretty"), name)
        assert f is not None, f"footprint not found: {fp}"
        f.SetReference(ref); f.SetValue(val)
        f.SetPosition(pt(x, y)); f.SetOrientationDegrees(rot)
        b.Add(f)
        seen = set()
        for pad in f.Pads():
            num = pad.GetNumber()
            if not num: continue
            seen.add(num)
            key = f"{ref}.{num}"
            if key in pad2net: pad.SetNet(netmap[pad2net[key]])
            elif num not in NC.get(ref, []): problems.append(f"unconnected pad {key}")
        for key in [k for k in pad2net if k.split(".")[0] == ref]:
            if key.split(".")[1] not in seen: problems.append(f"netlist pad {key} does not exist on {fp}")
    missing = sorted({p.split(".")[0] for p in pad2net} - set(PARTS))
    if missing: problems.append("refs in nets but not in PARTS: " + ",".join(missing))
    # outline with 3 mm corner radius
    r = 3.0
    def seg(x1, y1, x2, y2):
        s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(pt(x1, y1)); s.SetEnd(pt(x2, y2)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); b.Add(s)
    def arc(cx, cy, sx, sy, ang):
        s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetCenter(pt(cx, cy)); s.SetStart(pt(sx, sy)); s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(ang, pcbnew.DEGREES_T)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); b.Add(s)
    W, H = BOARD_W, BOARD_H
    seg(r, 0, W - r, 0); seg(W, r, W, H - r); seg(W - r, H, r, H); seg(0, H - r, 0, r)
    arc(W - r, r, W - r, 0, 90); arc(W - r, H - r, W, H - r, 90); arc(r, H - r, r, H, 90); arc(r, r, 0, r, 90)
    # title text on silk
    t = pcbnew.PCB_TEXT(b); t.SetText("MERIDIAN IP-1 MAIN CONTROLLER  REV A  (hypothetical demo design)"); t.SetPosition(pt(50, 78.3)); t.SetLayer(pcbnew.F_SilkS)
    t.SetTextSize(pcbnew.VECTOR2I(mm(0.8), mm(0.8))); t.SetTextThickness(mm(0.12)); b.Add(t)
    b.SetLayerType(pcbnew.In1_Cu, pcbnew.LT_POWER); b.SetLayerType(pcbnew.In2_Cu, pcbnew.LT_POWER)
    b.SetLayerName(pcbnew.In1_Cu, "GND.Cu"); b.SetLayerName(pcbnew.In2_Cu, "PWR.Cu")
    add_zone(b, pcbnew.In1_Cu, "GND"); add_zone(b, pcbnew.In2_Cu, "+3V3")
    pcbnew.SaveBoard(PCB, b); pcbnew.SaveBoard(os.path.join(HERE, "ip1_main_unrouted.kicad_pcb"), b)
    # courtyard overlap check (bounding boxes of courtyards)
    b = pcbnew.LoadBoard(PCB)
    boxes = []
    for f in b.GetFootprints():
        bb = f.GetBoundingBox(False, False)
        boxes.append((f.GetReference(), pcbnew.ToMM(bb.GetLeft()) - OX, pcbnew.ToMM(bb.GetTop()) - OY, pcbnew.ToMM(bb.GetRight()) - OX, pcbnew.ToMM(bb.GetBottom()) - OY))
    ov = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, c = boxes[i], boxes[j]
            if a[1] < c[3] - 0.05 and c[1] < a[3] - 0.05 and a[2] < c[4] - 0.05 and c[2] < a[4] - 0.05:
                ov.append(f"{a[0]}x{c[0]}")
    off = [f"{n}({l:.1f},{t:.1f},{r_:.1f},{bt:.1f})" for n, l, t, r_, bt in boxes if l < 0.3 or t < 0.3 or r_ > W - 0.3 or bt > H - 0.3]
    print("parts", len(PARTS), "nets", len(NETS), "pads on nets", len(pad2net))
    print("PROBLEMS:", problems or "none")
    print("OVERLAPS:", " ".join(ov) or "none")
    print("OFF BOARD:", " ".join(off) or "none")
    ok = pcbnew.ExportSpecctraDSN(b, os.path.join(HERE, "ip1_main.dsn"))
    print("dsn export:", ok)
    for f in b.GetFootprints():
        if f.GetReference() in ("J1", "J3", "J10", "J11"):
            print(f.GetReference(), [(p.GetNumber(), round(pcbnew.ToMM(p.GetPosition().x) - OX, 2), round(pcbnew.ToMM(p.GetPosition().y) - OY, 2), round(pcbnew.ToMM(p.GetDrillSize().x), 2)) for p in f.Pads()])

def finish():
    b = pcbnew.LoadBoard(os.path.join(HERE, "ip1_main_unrouted.kicad_pcb"))
    ses = os.path.join(HERE, "ip1_main.ses")
    nets = b.GetNetsByName()
    txt = open(ses).read()
    tok = re.findall(r'"[^"]*"|[()]|[^\s()]+', txt)
    def parse(i):
        out = []
        while i < len(tok):
            t = tok[i]
            if t == "(": sub, i = parse(i + 1); out.append(sub)
            elif t == ")": return out, i + 1
            else: out.append(t.strip('"')); i += 1
        return out, i
    tree = parse(0)[0][0]
    routes = [x for x in tree if isinstance(x, list) and x[0] == "routes"][0]
    res = [x for x in routes if isinstance(x, list) and x[0] == "resolution"][0]
    k = {"um": 1e-3, "mm": 1.0, "mil": 0.0254}[res[1]] / float(res[2])      # file units -> mm
    lay = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu, "GND.Cu": pcbnew.In1_Cu, "PWR.Cu": pcbnew.In2_Cu}
    nout = [x for x in routes if isinstance(x, list) and x[0] == "network_out"][0]
    for n in nout[1:]:
        code = nets[n[1]].GetNetCode()
        for it in n[2:]:
            if it[0] == "wire":
                p = it[1]; layer = lay[p[1]]; w = float(p[2]) * k; xy = [float(v) * k for v in p[3:]]
                pts = list(zip(xy[0::2], xy[1::2]))
                for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                    t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(x1), mm(-y1))); t.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(-y2)))
                    t.SetWidth(mm(w)); t.SetLayer(layer); t.SetNetCode(code); b.Add(t)
            elif it[0] == "via":
                v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(float(it[2]) * k), mm(-float(it[3]) * k)))
                v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNetCode(code); b.Add(v)
    # widen power tracks where they were routed at the default width
    pw = set(POWER_NETS)
    # --- plane fan-out: every SMD pad on GND / +3V3 gets a short stub and a via into its plane; then GND stitching vias ---
    from shapely.geometry import Point, LineString, box as sbox
    from shapely.strtree import STRtree
    F, B = pcbnew.F_Cu, pcbnew.B_Cu
    tm = pcbnew.ToMM
    obs = {F: [], B: []}; holes = []; smd = []
    for f in b.GetFootprints():
        for p in f.Pads():
            bb = p.GetBoundingBox(); g = sbox(tm(bb.GetLeft()), tm(bb.GetTop()), tm(bb.GetRight()), tm(bb.GetBottom()))
            if p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
                obs[F].append((g, p.GetNetCode())); obs[B].append((g, p.GetNetCode()))
                holes.append((tm(p.GetPosition().x), tm(p.GetPosition().y), tm(p.GetDrillSize().x) / 2))
            else:
                obs[F if p.IsOnLayer(F) else B].append((g, p.GetNetCode())); smd.append((g, f.GetReference(), p))
    for t in b.GetTracks():
        if t.GetClass() == "PCB_VIA":
            x, y = tm(t.GetPosition().x), tm(t.GetPosition().y); g = Point(x, y).buffer(tm(t.GetWidth()) / 2)
            obs[F].append((g, t.GetNetCode())); obs[B].append((g, t.GetNetCode())); holes.append((x, y, 0.15))
        else:
            g = LineString([(tm(t.GetStart().x), tm(t.GetStart().y)), (tm(t.GetEnd().x), tm(t.GetEnd().y))]).buffer(tm(t.GetWidth()) / 2)
            obs[t.GetLayer()].append((g, t.GetNetCode()))
    trees = {L: STRtree([g for g, _ in obs[L]]) for L in (F, B)}
    extra = {F: [], B: []}
    pad_tree = STRtree([g for g, _, _ in smd])
    CL = 0.22
    def clear(geom, layer, code):
        for i in trees[layer].query(geom.buffer(CL)):
            g, n = obs[layer][i]
            if n != code and g.distance(geom) < CL: return False
        return all(n == code or g.distance(geom) >= CL for g, n in extra[layer])
    def via_ok(x, y, code):
        if not (OX + 1.2 <= x <= OX + BOARD_W - 1.2 and OY + 1.2 <= y <= OY + BOARD_H - 1.2): return False
        c = Point(x, y)
        if any(math.hypot(x - hx, y - hy) < hr + 0.15 + 0.35 for hx, hy, hr in holes): return False
        if any(smd[i][0].distance(c) < 0.45 for i in pad_tree.query(c.buffer(0.5))): return False     # no via-in-pad
        ring = c.buffer(0.3)
        return clear(ring, F, code) and clear(ring, B, code)
    def add_via(x, y, code):
        v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y))); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetLayerPair(F, B); v.SetNetCode(code); b.Add(v)
        g = Point(x, y).buffer(0.3); extra[F].append((g, code)); extra[B].append((g, code)); holes.append((x, y, 0.15))
    fan_ok = fan_fail = 0; failed = []
    for g, ref, p in smd:
        name = p.GetNetname()
        if name not in ("GND", "+3V3") or (ref == "U4" and p.GetNumber() == "29") or not p.IsOnLayer(F): continue
        code = p.GetNetCode(); px, py = tm(p.GetPosition().x), tm(p.GetPosition().y); done = False
        for d in [0.9 + 0.15 * i for i in range(16)]:
            for k in range(16):
                a = k * math.pi / 8; x, y = px + d * math.cos(a), py + d * math.sin(a)
                stub = LineString([(px, py), (x, y)]).buffer(0.125)
                if via_ok(x, y, code) and clear(stub, F, code):
                    t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(px), mm(py))); t.SetEnd(pcbnew.VECTOR2I(mm(x), mm(y))); t.SetWidth(mm(0.25)); t.SetLayer(F); t.SetNetCode(code); b.Add(t)
                    extra[F].append((stub, code)); add_via(x, y, code); done = True; break
            if done: break
        if done: fan_ok += 1
        else: fan_fail += 1; failed.append(f"{ref}.{p.GetNumber()}")
    gnd = nets["GND"].GetNetCode(); stitch = 0
    for iy in range(1, 10):
        for ix in range(1, 13):
            x, y = OX + ix * 8.0 - 2.0, OY + iy * 8.0
            if via_ok(x, y, gnd): add_via(x, y, gnd); stitch += 1
    print("plane fan-out vias:", fan_ok, "no room:", fan_fail, failed, "| GND stitching vias:", stitch)
    # --- pours: GND on both outer layers; all planes use thermal relief on through-hole pins only ---
    add_zone(b, F, "GND"); add_zone(b, B, "GND")
    for z in b.Zones(): z.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)
    # REV A as built for the story: J1 pin 2 (GND) is tied SOLID to every plane (no thermal relief) -> this is the hard-to-solder joint
    for f in b.GetFootprints():
        if f.GetReference() == "J1":
            for pad in f.Pads():
                if pad.GetNumber() == "2": pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
    b.BuildConnectivity()
    n_via = sum(1 for t in b.GetTracks() if t.GetClass() == "PCB_VIA"); n_tr = len(b.GetTracks()) - n_via
    print("track segments", n_tr, "vias", n_via, "unrouted connections:", b.GetConnectivity().GetUnconnectedCount(False))
    pcbnew.SaveBoard(PCB, b)
    rep = os.path.join(HERE, "ip1_main_drc.txt")
    pcbnew.WriteDRCReport(b, rep, pcbnew.EDA_UNITS_MILLIMETRES, True)
    txt = open(rep).read()
    print("DRC:", " | ".join(l.strip() for l in txt.splitlines() if l.startswith("** Found")))
    print("DRC kinds:", dict(collections.Counter(re.findall(r"^\[(\w+)\]", txt, re.M))))
    for blk in re.split(r"\n(?=\[)", txt):
        if blk.startswith("[") and not blk.startswith(("[silk", "[lib_footprint")): print("  ", " / ".join(l.strip() for l in blk.splitlines()[:4])[:260])

if __name__ == "__main__":
    {"place": place, "finish": finish}[sys.argv[1]]()
