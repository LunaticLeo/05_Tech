import networkx as nx
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE

def build_face_adjacency_graph(step_file_path: str) -> nx.Graph:
    """
    从STEP文件构建面-边邻接图 (Face-Edge Adjacency Graph)

    图的节点：每个面 (TopoDS_Face)
    图的边：如果两个面共享一条边，则它们之间存在一条连接

    Args:
        step_file_path: STEP文件的路径

    Returns:
        networkx.Graph: 面邻接图
    """
    # 1. 读取STEP文件
    reader = STEPControl_Reader()
    status = reader.ReadFile(step_file_path)
    if status != 1:  # IFSelect_RetDone = 1
        raise RuntimeError(f"无法读取STEP文件: {step_file_path}")

    reader.TransferRoots()
    shape = reader.OneShape()

    # 2. 使用TopologyExplorer遍历拓扑
    topo = TopologyExplorer(shape)

    # 获取所有面
    faces = list(topo.faces())
    print(f"共找到 {len(faces)} 个面")

    # 3. 构建面到索引的映射（提高查找效率）
    face_to_idx = {face: i for i, face in enumerate(faces)}

    # 4. 构建面-边索引: 每条边 -> 包含它的面的列表，同时保存边对象
    edge_to_faces = {}
    for face in faces:
        # print(len(list(topo.edges_from_face(face))))
        for edge in topo.edges_from_face(face):
            edge_key = hash(edge)
            if edge_key not in edge_to_faces:
                edge_to_faces[edge_key] = {'edge': edge, 'faces': []}
            # 避免重复添加同一个面
            if face not in edge_to_faces[edge_key]['faces']:
                edge_to_faces[edge_key]['faces'].append(face)

    # 5. 构建邻接图
    graph = nx.Graph()
    # 为每个面添加节点
    for i, face in enumerate(faces):
        graph.add_node(i, face=face)

    # 遍历每条边，如果一条边连接两个面，则在图中添加一条边
    for item in edge_to_faces.values():
        face_list = item['faces']
        shared_edge = item['edge']   # 这就是共享边对象
        if len(face_list) == 2:
            f1_idx = face_to_idx[face_list[0]]
            f2_idx = face_to_idx[face_list[1]]
            graph.add_edge(f1_idx, f2_idx, edge=shared_edge)
        elif len(face_list) > 2:
            # 非流形情况：一条边连接多个面，两两之间都建立连接
            for i in range(len(face_list)):
                for j in range(i + 1, len(face_list)):
                    f1_idx = face_to_idx[face_list[i]]
                    f2_idx = face_to_idx[face_list[j]]
                    graph.add_edge(f1_idx, f2_idx, edge=shared_edge)

    print(f"图中共有 {graph.number_of_nodes()} 个节点，{graph.number_of_edges()} 条边")
    return graph


if __name__ == "__main__":
    # 使用示例
    step_file = "Data\\00002_index_1.step"  # 替换为你的STEP文件路径
    try:
        adj_graph = build_face_adjacency_graph(step_file)

        # 打印图的基本信息
        print(f"节点数: {adj_graph.number_of_nodes()}")
        print(f"边数: {adj_graph.number_of_edges()}")

        # 可选: 使用NetworkX的绘图功能进行可视化
        # import matplotlib.pyplot as plt
        # nx.draw(adj_graph, with_labels=True)
        # plt.show()

    except Exception as e:
        print(f"错误: {e}")