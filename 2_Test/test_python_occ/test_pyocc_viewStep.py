from occwl.compound import Compound
from occwl.viewer import Viewer

# 加载
compound = Compound.load_from_step("Data\\01124_index_2.step")

# 显示所有 Solid
v = Viewer()
for solid in compound.solids():
    v.display(solid)

v.fit()
v.show()