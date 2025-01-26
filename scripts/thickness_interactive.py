import os
import numpy as np
import pyvista as pv
from scipy.spatial import KDTree
import dash
from dash import dcc, html, Input, Output, State
import dash_uploader as du
import plotly.graph_objects as go

# Initialize the Dash app - Interactive app for thickness analysis
# @2024 Imane Chafi

app = dash.Dash(__name__)
server = app.server

# Upload folders
du.configure_upload(app, "./uploads")

# Layout of the app
app.layout = html.Div([
    html.H1("Interactive Thickness Analysis App", style={"textAlign": "center"}),

    # Folder inputs
    html.Div([
        html.Label("Crown Shell Folder:"),
        dcc.Input(id="crown-folder", type="text", placeholder="Enter path to crown shell folder", style={"width": "80%"}),
        html.Br(),
        html.Label("Crown Bottom Mesh Folder:"),
        dcc.Input(id="prep-folder", type="text", placeholder="Enter path to preparation folder", style={"width": "80%"}),
    ], style={"marginBottom": "20px"}),

    # Dropdown to select cases
    html.Div([
        html.Label("Select Case:"),
        dcc.Dropdown(id="case-dropdown", placeholder="Select a case", style={"width": "80%"}),
    ], style={"marginBottom": "20px"}),

    # Threshold slider
    html.Div([
        html.Label("Below Distance Threshold (Red Region):"),
        dcc.Slider(id="red-threshold", min=0.5, max=2, step=0.1, value=1.0, 
                   marks={i: str(i) for i in np.arange(0.5, 2.1, 0.5)}),
    ], style={"marginBottom": "20px"}),

    # 3D Visualization
    dcc.Graph(id="distance-heatmap", style={"height": "70vh"}),

    # Output message
    html.Div(id="output-message", style={"textAlign": "center", "marginTop": "20px"})
])

# Helper function to compute distances
def compute_distances(prep_mesh, crown_mesh):
    tree = KDTree(crown_mesh.points)
    distances, _ = tree.query(prep_mesh.points)
    return distances

# Helper function to generate 3D visualization
def create_3d_visualization(prep_mesh, crown_mesh, distances, red_threshold):
    # Assign colors based on thresholds
    red_mask = distances < red_threshold
    colors = np.full((prep_mesh.n_points, 3), [0.5, 0.5, 0.5])  # Default gray
    colors[red_mask] = [1, 0, 0]  # Red

    # Add colors as a scalar field for the preparation mesh
    prep_mesh["colors"] = colors

    # Convert prep mesh to Plotly-friendly format
    prep_vertices = prep_mesh.points
    prep_faces = prep_mesh.faces.reshape(-1, 4)[:, 1:]  # PyVista faces include counts; strip them
    prep_colors = prep_mesh["colors"]

    # Convert crown mesh to Plotly-friendly format
    crown_vertices = crown_mesh.points
    crown_faces = crown_mesh.faces.reshape(-1, 4)[:, 1:]  # Same as above

    # Create Plotly traces
    prep_trace = go.Mesh3d(
        x=prep_vertices[:, 0],
        y=prep_vertices[:, 1],
        z=prep_vertices[:, 2],
        i=prep_faces[:, 0],
        j=prep_faces[:, 1],
        k=prep_faces[:, 2],
        vertexcolor=prep_colors,
        opacity=1.0,
        name="Preparation Mesh",
    )

    crown_trace = go.Mesh3d(
        x=crown_vertices[:, 0],
        y=crown_vertices[:, 1],
        z=crown_vertices[:, 2],
        i=crown_faces[:, 0],
        j=crown_faces[:, 1],
        k=crown_faces[:, 2],
        color="gray",
        opacity=0.3,
        name="Crown Shell",
    )

    # Combine traces into a Plotly figure
    fig = go.Figure(data=[prep_trace, crown_trace])
    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig

# Callback to populate case dropdown based on folder inputs
@app.callback(
    Output("case-dropdown", "options"),
    Input("crown-folder", "value"),
    Input("prep-folder", "value"),
)
def populate_cases(crown_folder, prep_folder):
    if not crown_folder or not prep_folder:
        return []
    crown_files = [f for f in os.listdir(crown_folder) if f.endswith("_shell_registered.stl")]
    prep_files = [f for f in os.listdir(prep_folder) if f.endswith("_crownb_registered.stl")]
    cases = [f.split("_")[0] for f in crown_files if f.split("_")[0] in [g.split("_")[0] for g in prep_files]]
    return [{"label": case, "value": case} for case in cases]

# Callback to update the heatmap and visualizations
@app.callback(
    Output("distance-heatmap", "figure"),
    Output("output-message", "children"),
    Input("case-dropdown", "value"),
    Input("red-threshold", "value"),
    State("crown-folder", "value"),
    State("prep-folder", "value"),
)
def update_visualization(selected_case, red_threshold, crown_folder, prep_folder):
    if not selected_case or not crown_folder or not prep_folder:
        return dash.no_update, "Please select a case and ensure folders are valid."

    # Load meshes
    crown_path = os.path.join(crown_folder, f"{selected_case}_shell_registered.stl")
    prep_path = os.path.join(prep_folder, f"{selected_case}_crownb_registered.stl")
    crown_mesh = pv.read(crown_path)
    prep_mesh = pv.read(prep_path)

    # Compute distances
    distances = compute_distances(prep_mesh, crown_mesh)

    # Generate visualization
    fig = create_3d_visualization(prep_mesh, crown_mesh, distances, red_threshold)
    return fig, f"Visualization updated for case: {selected_case}"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
