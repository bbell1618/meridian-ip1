"""Convert a STEP file to GLB keeping part names and colours (used for the KiCad board model)."""
import sys
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.RWGltf import RWGltf_CafWriter
from OCP.TColStd import TColStd_IndexedDataMapOfStringString
from OCP.Message import Message_ProgressRange
src, dst = sys.argv[1], sys.argv[2]
tol = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
app = XCAFApp_Application.GetApplication_s()
doc = TDocStd_Document(TCollection_ExtendedString("XmlXCAF")); app.InitDocument(doc)
r = STEPCAFControl_Reader(); r.SetColorMode(True); r.SetNameMode(True)
assert r.ReadFile(src) == 1; r.Transfer(doc)
st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main()); ls = TDF_LabelSequence(); st.GetFreeShapes(ls)
for i in range(1, ls.Length() + 1):
    BRepMesh_IncrementalMesh(st.GetShape_s(ls.Value(i)), tol, False, 0.35, True)
w = RWGltf_CafWriter(TCollection_AsciiString(dst), True)
print("written:", w.Perform(doc, TColStd_IndexedDataMapOfStringString(), Message_ProgressRange()))
