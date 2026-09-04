from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
step_path = ".\\Data\\01124_index_2.step"
shape = read_step_file(
    step_path,
)
topo = TopologyExplorer(shape)
solids = list(topo.solids())
shells = list(topo.shells())
faces = list(topo.faces())
print("======================")
print("OCC STEP")
print("======================")
print("Solid 数量:", len(solids))
print("Shell 数量:", len(shells))
print("Face 数量:", len(faces))
print("======================")
