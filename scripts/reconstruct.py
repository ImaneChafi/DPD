import pyvista as pv

def reconstruct_mesh(file_path, output_path, num_iterations=30, smoothing_factor=0.1):
    """
    Reconstructs a mesh by filling holes and applying Laplacian smoothing.
    
    Parameters:
        file_path (str): Path to the input mesh file.
        output_path (str): Path to save the reconstructed mesh.
        num_iterations (int): Number of iterations for Laplacian smoothing.
        smoothing_factor (float): Smoothing factor for Laplacian smoothing.
    """
    # Load the mesh
    mesh = pv.read(file_path)
    
    # Check for holes
    print(f"Original mesh has {mesh.n_open_edges} open edges.")
    if mesh.n_open_edges > 0:
        # Fill holes
        filled_mesh = mesh.fill_holes(holes_size=float('inf'))
        print(f"Mesh holes filled. Remaining open edges: {filled_mesh.n_open_edges}")
    else:
        filled_mesh = mesh
    
    # Apply Laplacian smoothing
    smoothed_mesh = filled_mesh.smooth(n_iter=num_iterations, relaxation_factor=smoothing_factor)
    
    # Save the reconstructed mesh
    smoothed_mesh.save(output_path)
    print(f"Reconstructed mesh saved to {output_path}")

if __name__ == "__main__":
    # Input and output file paths
    input_file = "input_mesh.stl"  # Replace with your mesh file path
    output_file = "reconstructed_mesh.stl"  # Replace with your desired output file path

    # Parameters
    smoothing_iterations = 50  # Number of iterations for Laplacian smoothing
    smoothing_relaxation = 0.2  # Relaxation factor for smoothing

    # Run reconstruction
    reconstruct_mesh(input_file, output_file, smoothing_iterations, smoothing_relaxation)
