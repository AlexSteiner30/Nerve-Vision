import torch
import model
from text_to_vec import *
import open3d as o3d

import numpy as np

Generator = model.Generator().cuda()
Generator_f = model.Generator().cuda()
Autoencoder = model.Autoencoder().cuda()

vertices_path = "../TrainedModels/vertices.pt" 
faces_path = "../TrainedModels/faces.pt" 

checkpoint = torch.load(vertices_path)
Generator.load_state_dict(checkpoint['G_state_dict'])

checkpoint_f = torch.load(faces_path)
Generator_f.load_state_dict(checkpoint_f['G_state_dict'])

autoencoder_path = "../TrainedModels/autoencoder.pt" 
checkpoint_ae = torch.load(autoencoder_path)
Autoencoder.load_state_dict(checkpoint_ae['autoencoder'])

def create_mesh(vertices, faces):
    vertices = np.array(vertices)
    faces = np.array(faces)

    mesh = o3d.geometry.TriangleMesh()
    
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(faces)

    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()

    return mesh

def predict(z):
    with torch.no_grad():
        sample = Generator(z).cpu()
        points = sample.numpy()[0]

        sample = Generator_f(z).cpu()
        faces = sample.numpy()[0]

    vertices = Autoencoder(torch.from_numpy(points).to('cuda')).cpu().detach().numpy()
    vertices = np.array(vertices, dtype=np.float32)
        
    vertices = Autoencoder(torch.from_numpy(points).to('cuda')).cpu().detach().numpy()
    faces = np.array(faces, dtype=np.float32)

    print(faces[0])

    mesh = create_mesh(vertices, faces)

    o3d.visualization.draw_geometries([mesh])

predict(torch.from_numpy(text_to_vec(process_text(correct_prompt("old tractor"))).astype(np.float64)).reshape(1,512, 1).repeat(13, 1, 1).cuda().float())