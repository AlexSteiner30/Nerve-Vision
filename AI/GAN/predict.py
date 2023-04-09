import torch
from mesh_generation import generate_mesh
from model import Generator
import open3d as o3d
from text_to_vec import *
import time

import numpy as np

Generator = Generator(num_points=2048).cuda()

model_path = "../TrainedModels/chair.pt" 
model_path = "300.pt" 
checkpoint = torch.load(model_path)
Generator.load_state_dict(checkpoint['G_state_dict'])

z = torch.from_numpy(text_to_vec(process_text(correct_prompt("bench"))) + np.random.normal(0, 0.01, 128).astype(np.float64)).reshape(1,1,128).cuda().float()
print(z.type())

with torch.no_grad():
    start = time.time()

    sample = Generator(z).cpu()

    points = sample.numpy().reshape(2048,3)

    end = time.time()
    print(end - start)

    mesh = generate_mesh(points)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    o3d.io.write_triangle_mesh("mesh.obj", mesh)

    o3d.visualization.draw_geometries([pcd])