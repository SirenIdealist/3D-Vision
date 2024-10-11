import os
from tqdm import tqdm
import open3d as o3d

# 对off点云数据进行采样
def sample_points_from_off(off_file, num_points):
    # 读取OFF文件
    mesh = o3d.io.read_triangle_mesh(off_file)
    # 将OFF文件转换为点云
    point_cloud = mesh.sample_points_uniformly(num_points)
    return point_cloud

# 文件夹路径
path = 'E:\\AAA_Dataset\\3D Point Cloud\\ModelNet10\\ModelNet10'
folder_path =[]

# 获取每一个类别的名称
for item in os.listdir(path):
    if not '.' in item:
        folder_path.append(os.path.join(path, item))
        
# 获取文件名
def get_file_name(path):
    return path.split('\\')[-1].split('.')[0]

# 遍历所有文件夹
for file in folder_path:
    # 获得完整的训练集和测试集文件路径
    train_file = os.path.join(file, 'train')
    test_file = os.path.join(file, 'test')
    
    # 对训练集和测试集进行处理
    for filepath in [train_file, test_file]:
        # 获取该文件夹下的所有文件名
        filenames = os.listdir(filepath)
     
        # 处理每个文件（点云）
        for filename in tqdm(filenames):
            # 获取点云文件的完整地址
            old_path = os.path.join(filepath, filename)
            # 如果文件名以.开头，则跳过（这里假设以.开头的文件是无效文件）
            if(filename.startswith('.')):
                continue
            # 读取点云数据
            point_cloud = sample_points_from_off(old_path, 10000)
            # 生成新的文件名（将原文件名的扩展名改为.xyz）
            name = get_file_name(old_path) + '.xyz'
            # 新的文件的地址
            new_path = os.path.join('new'+old_path).replace(get_file_name(old_path) + '.off', name)

            # 创建新的文件夹（如果不存在）
            new_folder = os.path.join(*new_path.split('\\')[:-1])+'\\'

            os.makedirs(new_folder, exist_ok=True)
            # 保存新的点云文件
            o3d.io.write_point_cloud(new_path, point_cloud)
         

