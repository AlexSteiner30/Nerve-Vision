import torch
from mesh_generation import generate_mesh
from model import Generator
import open3d as o3d
from text_to_vec import *

import logging
logger = logging.getLogger("trimesh")
logger.setLevel(logging.ERROR)

Generator = Generator(num_points=2048).cuda()

model_path = "../TrainedModels/chair.pt" 
model_path = "300.pt" 
checkpoint = torch.load(model_path)
Generator.load_state_dict(checkpoint['G_state_dict'])

z = torch.from_numpy(text_to_vec("Tall deep square bathtub with a small indented step inside it")).reshape(1,1,128).cuda()

with torch.no_grad():
    sample = Generator(z).cpu()

    points = sample.numpy().reshape(2048,3)

    mesh = generate_mesh(points)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    o3d.visualization.draw_geometries([pcd])