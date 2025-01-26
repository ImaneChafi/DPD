import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# Load the STL files for the preparation and the crown shell
crown_mesh = pv.read("/Users/imanechafi/Downloads/OneDrive_3_2024-06-07 2/cb_31/6027-31/registered/shell31_registered.stl")
prep_mesh = pv.read("/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/prep_auto/shrunken_mesh.stl")

# Compute the closest point distance between the meshes
def compute_distances(prep, crown):
    # Use KDTree for fast nearest-neighbor lookup
    tree = KDTree(crown.points)
    distances, indices = tree.query(prep.points)
    return distances, indices

# Get distances and their corresponding points
distances, indices = compute_distances(prep_mesh, crown_mesh)

# 1. Image with distances > 3 mm in red, everything else in gray (on the preparation)
def plot_distances_above_threshold(prep_mesh, crown_mesh, distances, threshold):
    # Create color arrays for the preparation
    colors = np.full((prep_mesh.n_points, 3), [0.5, 0.5, 0.5])  # Gray by default
    above_threshold = distances > threshold
    colors[above_threshold] = [1, 0, 0]  # Red for distances > threshold

    # Set color as a custom array for visualization
    prep_mesh["colors"] = colors

    # Plot
    plotter = pv.Plotter()
    plotter.add_mesh(prep_mesh, scalars="colors", rgb=True, opacity=1.0)  # Preparation with custom colors
    plotter.add_mesh(crown_mesh, color="gray", opacity=0.3, show_edges=True)  # Gray and transparent crown shell
    plotter.show(screenshot="distances_above_3mm.png")

# 2. Image with distances < 1.5 mm in blue, everything else in gray (on the preparation)
def plot_distances_below_threshold(prep_mesh, crown_mesh, distances, threshold):
    # Create color arrays for the preparation
    colors = np.full((prep_mesh.n_points, 3), [0.5, 0.5, 0.5])  # Gray by default
    below_threshold = distances < threshold
    colors[below_threshold] = [0, 0, 1]  # Blue for distances < threshold

    # Set color as a custom array for visualization
    prep_mesh["colors"] = colors

    # Plot
    plotter = pv.Plotter()
    plotter.add_mesh(prep_mesh, scalars="colors", rgb=True, opacity=1.0)  # Preparation with custom colors
    plotter.add_mesh(crown_mesh, color="gray", opacity=0.3, show_edges=True)  # Gray and transparent crown shell
    plotter.show(screenshot="distances_below_1.5mm.png")

# 3. Heatmap of distances between meshes
def plot_heatmap_of_distances(prep_mesh, crown_mesh, distances):
    # Assign the distance values as a scalar field to the preparation mesh
    prep_mesh["Distance"] = distances

    # Plot the preparation mesh using a heatmap
    plotter = pv.Plotter()
    plotter.add_mesh(prep_mesh, scalars="Distance", cmap="jet", opacity=1.0)  # Heatmap on the preparation mesh
    plotter.add_mesh(crown_mesh, color="gray", opacity=0.3, show_edges=True)  # Gray and transparent crown shell
    plotter.show(screenshot="heatmap_of_distances.png")

# Create the first image: distances > 3mm in red
plot_distances_above_threshold(prep_mesh, crown_mesh, distances, threshold=3)

# Create the second image: distances < 1.5mm in blue
plot_distances_below_threshold(prep_mesh, crown_mesh, distances, threshold=1.5)

# Create the heatmap of distances between meshes
plot_heatmap_of_distances(prep_mesh, crown_mesh, distances)

print("Images saved: distances_above_3mm.png, distances_below_1.5mm.png, heatmap_of_distances.png")