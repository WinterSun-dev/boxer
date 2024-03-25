import ezdxf



def make_dxf(polylines):
    doc = ezdxf.new("R2000")
    msp = doc.modelspace()
    for p in polylines:
        msp.add_lwpolyline(p.vertices)

    doc.saveas("box_diagram.dxf")