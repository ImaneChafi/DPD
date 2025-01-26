import os
import numpy as np
import pandas as pd
import pyvista as pv
from scipy.spatial import cKDTree

def compute_distances(shell_mesh, die_mesh):
    # Create a KDTree for the die mesh points
    die_tree = cKDTree(die_mesh.points)

    # For each point in the shell mesh, find the nearest point in the die mesh
    distances, _ = die_tree.query(shell_mesh.points)

    # Segment distances (adjust how tip, side, and intersection are defined)
    tip_indices = np.where(shell_mesh.points[:, 2] > np.percentile(shell_mesh.points[:, 2], 90))
    side_indices = np.where((shell_mesh.points[:, 2] > np.percentile(shell_mesh.points[:, 2], 10)) & 
                            (shell_mesh.points[:, 2] < np.percentile(shell_mesh.points[:, 2], 90)))
    intersection_indices = np.where(shell_mesh.points[:, 2] <= np.percentile(shell_mesh.points[:, 2], 10))

    tip_distances = distances[tip_indices]
    side_distances = distances[side_indices]
    intersection_distances = distances[intersection_indices]

    return {
        'max': np.max(distances),
        'min': np.min(distances),
        'tip_max': np.max(tip_distances),
        'side_max': np.max(side_distances),
        'intersection_max': np.max(intersection_distances),
        'std_dev': np.std(distances)
    }

def analyze_folder(folder_path):
    results = []
    
    for root, dirs, files in os.walk(folder_path):
        shell_file = None
        die_file = None

        for file in files:
            if 'shell' in file.lower():
                shell_file = os.path.join(root, file)
            elif 'die' in file.lower():
                die_file = os.path.join(root, file)

        if shell_file and die_file:
            # Load the meshes
            shell_mesh = pv.read(shell_file)
            die_mesh = pv.read(die_file)
            
            # Compute distances
            distance_data = compute_distances(shell_mesh, die_mesh)
            distance_data['folder'] = root
            results.append(distance_data)

    return pd.DataFrame(results)

def summarize_results(df):
    # Exclude non-numeric columns (like 'folder') from calculations
    numeric_df = df.select_dtypes(include=[np.number])
    
    overall_stats = {
        'mean': numeric_df.mean(),
        'std': numeric_df.std()
    }
    return overall_stats

def main(folder_path):
    # Analyze all subfolders
    df = analyze_folder(folder_path)
    
    # Compute overall statistics
    overall_stats = summarize_results(df)
    
    # Print the DataFrame (normal table format)
    print("\nDistance Analysis Table:\n")
    print(df.to_string(index=False))
    
    # Print the summary statistics
    print("\nOverall Averages:\n")
    print(overall_stats['mean'])
    
    print("\nOverall Standard Deviations:\n")
    print(overall_stats['std'])


# Set your folder path
folder_path = '/Users/imanechafi/Desktop/PhD/data/Journal_data/Canines/canine_ori/cb_23'
main(folder_path)
