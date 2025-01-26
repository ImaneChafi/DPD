import pyvista as pv
import numpy as np

def normalize_mesh(mesh):
    """Center the mesh and scale it to fit within a unit cube."""
    # Center the mesh around the origin
    center = np.array(mesh.center)
    mesh.translate(-center, inplace=True)

    # Scale the mesh to fit within a unit cube
    bounds = mesh.bounds
    scale = np.max(np.array(bounds[1::2]) - np.array(bounds[::2]))
    mesh.scale(1 / scale, inplace=True)

    return mesh

def flip_mesh(mesh, axis='x'):
    """Flip the mesh by 180 degrees along a specified axis."""
    if axis == 'x':
        flip_matrix = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    elif axis == 'y':
        flip_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif axis == 'z':
        flip_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'")
    
    # Apply the flipping transformation
    mesh.points = np.dot(mesh.points, flip_matrix.T)
    
    return mesh

def align_mesh_top(mesh1, mesh2):
    """Align the top of mesh2 with the top of mesh1 based on their bounding box along the z-axis."""
    # Get the bounds (min and max) for both meshes along the z-axis
    z_max1 = mesh1.bounds[5]  # max z for mesh1
    z_max2 = mesh2.bounds[5]  # max z for mesh2

    # Compute the translation needed to align the tops
    translation_z = z_max1 - z_max2

    # Apply the translation to mesh2 along the z-axis
    mesh2.translate([0, 0, translation_z], inplace=True)

    return mesh2

def overlay_and_normalize_meshes(mesh_path1, mesh_path2, flip_axis='x'):
    # Load the meshes
    mesh1 = pv.read(mesh_path1)
    mesh2 = pv.read(mesh_path2)

    # Normalize both meshes
    mesh1 = normalize_mesh(mesh1)
    mesh2 = normalize_mesh(mesh2)

    # Flip one of the meshes (if needed)
    mesh2 = flip_mesh(mesh2, axis=flip_axis)

    # Align the top of mesh2 with the top of mesh1
    mesh2 = align_mesh_top(mesh1, mesh2)

    # Create a Plotter object
    plotter = pv.Plotter()

    # Add the meshes to the plotter
    plotter.add_mesh(mesh1, color='blue', opacity=1, label='Mesh 1')
    plotter.add_mesh(mesh2, color='red', opacity=1, label='Mesh 2')

    # Add a legend
    plotter.add_legend()

    # Show the plot
    plotter.show()

# Example usage
mesh_path1 = '/Users/imanechafi/Desktop/PhD/CBCT_segmentation/127302829_shell_occlusion_l.stl'
mesh_path2 = '/Users/imanechafi/Desktop/PhD/CBCT_segmentation/000.dcm_Segmentation.seg1_Lower Teeth.stl'

# Overlay and normalize meshes, flipping mesh2 along the z-axis
overlay_and_normalize_meshes(mesh_path1, mesh_path2, flip_axis='z')
