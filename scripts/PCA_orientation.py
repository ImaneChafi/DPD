import os
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd

class CrownBottom:
    def __init__(self, path, die_name, marginline_name, offset, n_iter, pass_band, dist_margin_undercut, dist_margin_smooth):
        self.path = path
        self.die_name = die_name
        self.marginline_name = marginline_name
        self.offset = offset
        self.n_iter = n_iter
        self.pass_band = pass_band
        self.dist_margin_undercut = dist_margin_undercut
        self.dist_margin_smooth = dist_margin_smooth

    def fit_plane_to_margin_line(self):
        margin_line_mesh_o3d = o3d.io.read_point_cloud(os.path.join(self.path, self.marginline_name))
        points = np.asarray(margin_line_mesh_o3d.points)
        
        if points.shape[0] == 0:
            raise ValueError(f"No points found in margin line: {self.marginline_name}")

        # Apply PCA to find the orientation of the margin line
        pca = PCA(n_components=3)
        pca.fit(points)

        # Assuming the margin line is a closed loop, you can get four evenly spaced points along the curve
        num_points = len(points)
        indices = np.round(np.linspace(0, num_points - 1, 2)).astype(int)
        plane_points = points[indices]
        print("plane corners: ", len(plane_points), plane_points)
        # The plane should be parallel to the second and third principal components
        normal = pca.components_[2]  # Using the third principal component as the normal
        
        # Now, use one of the plane_points and the normal to define the plane
        point_on_plane = plane_points[0]

        # Generate a mesh for the plane parallel to second and third PCs, passing through the extracted points
        plane_mesh = self.generate_plane_mesh(normal, point_on_plane, points)
        return plane_mesh, pca
    
    def generate_plane_mesh(self, normal, point, points):
        # Define the plane size dynamically based on margin points bounds
        min_pt = points.min(axis=0)
        max_pt = points.max(axis=0)
        center = (min_pt + max_pt) / 2
        length = max(max_pt - min_pt) * 1.5  # Making sure the plane is sufficiently large
        plane = o3d.geometry.TriangleMesh.create_box(width=length, height=length, depth=0.02)
        plane.translate(-plane.get_center())  # Reset the center to origin
        plane.translate(center)  # Move to the new center
        
        # Align the plane normal to the fitted normal vector
        rotation_axis = np.cross([0, 0, 1], normal)
        rotation_angle = np.arccos(normal[2] / np.linalg.norm(normal))
        R = plane.get_rotation_matrix_from_axis_angle(rotation_axis * rotation_angle)
        plane.rotate(R, center=plane.get_center())  # Rotate around its current center
        
        return plane

    def calculate_average_z_of_margin_line(self):
        margin_line_mesh_o3d = o3d.io.read_point_cloud(os.path.join(self.path, self.marginline_name))
        margin_line_points = np.asarray(margin_line_mesh_o3d.points)
        avg_z_margin_line = np.mean(margin_line_points[:, 2])  # Calculate average y-value
        return avg_z_margin_line

    def calculate_high_curvature_points_from_stl(self, num_points=10):
        # Calculate the average y-value of the margin line points
        avg_z_margin_line = self.calculate_average_z_of_margin_line()

        # Load the mesh from an STL file
        mesh = o3d.io.read_triangle_mesh(os.path.join(self.path, self.die_name))
        mesh.compute_vertex_normals()
        
        vertices = np.asarray(mesh.vertices)
        # Filter vertices to consider only those above the average y-value of the margin line
        filtered_vertices = vertices[vertices[:, 2] > avg_z_margin_line]  # Keep only vertices with z > average z

        if len(filtered_vertices) > 0:
            curvature_values = np.random.rand(len(filtered_vertices))  # Simulated curvature values

            # Find indices of the 10 highest simulated curvature values
            indices_of_highest_curvature = np.argsort(-curvature_values)[:10]

            # Select the high curvature points based on the indices
            high_curvature_points = filtered_vertices[indices_of_highest_curvature]
        else:
            print("No vertices found above the specified z-value.")
            high_curvature_points = np.array([])  # Empty array if no vertices meet the criterion

        print("high prep: ", high_curvature_points)

        return high_curvature_points

    def find_vertical_direction(self):
        margin_line_mesh_o3d = o3d.io.read_point_cloud(os.path.join(self.path, self.marginline_name))
        points = np.asarray(margin_line_mesh_o3d.points)

        if points.shape[0] == 0:
            raise ValueError(f"No points found in margin line: {self.marginline_name}")

        # Apply PCA to find the orientation of the margin line
        pca = PCA(n_components=3)
        pca.fit(points)

        # The third principal component is expected to be the least variant and thus aligns with the vertical axis
        vertical_direction = pca.components_[2]
        longitudinal_direction = pca.components_[0]  # First principal component
        transverse_direction = pca.components_[1]  # Second principal component

        print("Vertical direction (PCA third component):", vertical_direction)
        print("Longitudinal direction:", longitudinal_direction)
        print("Transverse direction:", transverse_direction)
        return vertical_direction

    def visualize_axes(self, center_point, directions, vis):
        colors = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]  # Red, Green, Black for each axis
        for i, direction in enumerate(directions):
            line_points = [center_point - direction * 10, center_point + direction * 10]
            lines = [[0, 1]]
            line_set = o3d.geometry.LineSet(
                points=o3d.utility.Vector3dVector(line_points),
                lines=o3d.utility.Vector2iVector(lines),
            )
            line_set.colors = o3d.utility.Vector3dVector([colors[i]])
            vis.add_geometry(line_set)
    def visualize_die_and_margin_line(self, case_name):
        # Load the meshes and point cloud
        die_mesh_o3d = o3d.io.read_triangle_mesh(os.path.join(self.path, self.die_name))
        die_mesh_o3d.paint_uniform_color([0, 0, 0.8])
        
        margin_line_mesh_o3d = o3d.io.read_point_cloud(os.path.join(self.path, self.marginline_name))
        
        plane_mesh_o3d, pca = self.fit_plane_to_margin_line()
        
        # Calculate high curvature points for the die (STL) and create a point cloud for them
        high_curvature_points_die = self.calculate_high_curvature_points_from_stl()
        high_curvature_points_die_cloud = o3d.geometry.PointCloud()
        high_curvature_points_die_cloud.points = o3d.utility.Vector3dVector(high_curvature_points_die)
        high_curvature_points_die_cloud.paint_uniform_color([0, 1, 0])  # Green color for high curvature points of the die
        
        # Calculate the vertical direction using PCA
        vertical_direction = self.find_vertical_direction()
        center_point = np.mean(np.asarray(margin_line_mesh_o3d.points), axis=0)
        line_points = [center_point - vertical_direction * 10, center_point + vertical_direction * 10]
        lines = [[0, 1]]
        colors = [[0, 0, 0]]
        
        # Create a line set for the vertical direction
        vertical_line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(line_points),
            lines=o3d.utility.Vector2iVector(lines),
        )
        vertical_line_set.colors = o3d.utility.Vector3dVector(colors)
        
        # Create a sphere to mark the center point
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.5)
        sphere.translate(center_point)
        sphere.paint_uniform_color([1, 0, 0])  # Red color for the marker
        
        # Visualize the geometry
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(die_mesh_o3d)
        vis.add_geometry(margin_line_mesh_o3d)
        vis.add_geometry(plane_mesh_o3d)
        vis.add_geometry(high_curvature_points_die_cloud)
        vis.add_geometry(vertical_line_set)
        vis.add_geometry(sphere)
        
        # Set the camera view for a side view
        ctr = vis.get_view_control()
        param = ctr.convert_to_pinhole_camera_parameters()
        param.extrinsic = np.array([[1, 0, 0, 0],
                                    [0, 0, -1, 0],
                                    [0, 1, 0, -5],
                                    [0, 0, 0, 1]])
        ctr.convert_from_pinhole_camera_parameters(param)
        
        # Capture the screen image after rendering
        vis.poll_events()
        vis.update_renderer()
        vis.capture_screen_image(os.path.join("/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/preps", case_name + ".png"))
        
        vis.destroy_window()

    
def create_image_grid(image_folder, output_path, grid_size):
    # Collect all image file paths
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    
    # Open all images
    images = [Image.open(os.path.join(image_folder, img)) for img in image_files]
    
    if not images:
        raise ValueError("No images found in the specified folder.")
    
    # Get dimensions of the images
    widths, heights = zip(*(i.size for i in images))
    
    # Calculate grid size
    grid_width, grid_height = grid_size
    if grid_width * grid_height != len(images):
        raise ValueError("Grid size does not match the number of images.")
    
    total_width = max(widths) * grid_width
    total_height = max(heights) * grid_height
    
    # Create a new blank image
    new_image = Image.new('RGB', (total_width, total_height))
    
    x_offset = 0
    y_offset = 0
    
    for i in range(grid_height):
        for j in range(grid_width):
            img_index = i * grid_width + j
            if img_index >= len(images):
                break
            img = images[img_index]
            new_image.paste(img, (x_offset, y_offset))
            x_offset += img.width
        y_offset += images[0].height
        x_offset = 0
    
    # Save the final image grid
    new_image.save(output_path)

def main():
    die_folder = '/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/dies'
    margin_folder = '/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/margins'
    output_folder = '/Users/imanechafi/Desktop/PhD/data/marginline_tests/Incisors/preps'

    die_files = [f for f in os.listdir(die_folder) if f.endswith('.stl')]
    margin_files = [f for f in os.listdir(margin_folder) if f.endswith('_margin.ply')]

    curvature_points_all_cases = []    

    for die_file in die_files:
        base_name = os.path.splitext(die_file)[0]
        margin_file = base_name + '_margin.ply'
        
        if margin_file in margin_files:
            case_name = base_name
            crown_bottom_example = CrownBottom(die_folder, die_file, margin_folder + '/' + margin_file, 0.035, 1000, 0.5, 0.1, 1.5)
            crown_bottom_example.visualize_die_and_margin_line(case_name)
            
            # Collect curvature points for statistical analysis
            high_curvature_points = crown_bottom_example.calculate_high_curvature_points_from_stl()
            if high_curvature_points.size > 0:
                curvature_points_all_cases.append(high_curvature_points)


    # Statistical analysis
    total_cases = len(die_files)
    successful_pca_cases = len(curvature_points_all_cases)
    print(f'Total cases: {total_cases}')
    print(f'Successful PCA cases: {successful_pca_cases}')

    # Combine all high curvature points into a single array for visualization
    all_curvature_points = np.vstack(curvature_points_all_cases)

    # Create a 3D scatter plot of all curvature points
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(all_curvature_points[:, 0], all_curvature_points[:, 1], all_curvature_points[:, 2], c='r', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title('High Curvature Points Distribution')
    plt.show()

    # Create a heatmap of the curvature points
    df = pd.DataFrame(all_curvature_points, columns=['X', 'Y', 'Z'])
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Heatmap of High Curvature Points')
    plt.show()

if __name__ == "__main__":
    main()
