import dash
from dash import dcc, html, Input, Output
import numpy as np
import pyvista as pv
from sklearn.decomposition import PCA
import trimesh
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Interactive PCA and Extrusion Visualization", style={"textAlign": "center"}),

    # Input fields for file paths
    html.Div([
        html.Label("Preparation Die File Path:"),
        dcc.Input(id="prep-path", type="text", placeholder="Enter path to the prep die file", style={"width": "80%"}),
        html.Br(),
        html.Label("Margin Line File Path:"),
        dcc.Input(id="margin-path", type="text", placeholder="Enter path to the margin line file", style={"width": "80%"}),
    ], style={"marginBottom": "20px"}),

    # 3D Visualization
    dcc.Graph(id="3d-visualization", style={"height": "70vh"}),

    # Output message
    html.Div(
        id="output-message",
        style={
            "textAlign": "center",
            "marginTop": "20px",
            "padding": "10px",
            "borderRadius": "10px",
            "display": "inline-block",
            "fontSize": "18px"
        }
    )
])

# Function to calculate PCA components
def calculate_pca_component(points):
    pca = PCA(n_components=3)
    pca.fit(points)
    return pca.components_

# Callback to update the 3D visualization and the status rectangle
@app.callback(
    [Output("3d-visualization", "figure"),
     Output("output-message", "children"),
     Output("output-message", "style")],
    [Input("prep-path", "value"),
     Input("margin-path", "value")]
)
def update_visualization(prep_path, margin_path):
    if not prep_path or not margin_path:
        return {}, "Please provide both file paths.", {"display": "none"}

    # Load meshes
    try:
        prep_mesh = pv.read(prep_path)
        margin_mesh = pv.read(margin_path)
    except Exception as e:
        return {}, f"Error loading files: {e}", {"display": "none"}

    # Extract margin points and create a spline
    margin_points = np.array(margin_mesh.points)
    margin_spline = pv.Spline(margin_points, n_points=100)

    # Use Z-axis as the extrusion direction
    extrusion_direction_z = np.array([0, 0, 1]) * 10

    # Perform extrusion and create convex hull
    extruded_margin = margin_spline.extrude(extrusion_direction_z)
    hull = trimesh.convex.convex_hull(extruded_margin.points)
    convex_hull = pv.wrap(hull)

    # Calculate points above margin line and outside the convex hull
    margin_line_z = np.max(margin_points[:, 2])
    above_margin_points = prep_mesh.points[prep_mesh.points[:, 2] > margin_line_z]
    inside_mask = prep_mesh.select_enclosed_points(convex_hull, inside_out=True)['SelectedPoints']
    outside_points = prep_mesh.points[inside_mask == 1]
    final_points = outside_points[outside_points[:, 2] > margin_line_z]

    # Count red points
    num_red_points = final_points.shape[0]

    # Determine the rectangle style and message based on the number of red points
    if num_red_points < 10:
        status_message = "Normal"
        status_style = {
            "backgroundColor": "green",
            "color": "white",
            "padding": "10px",
            "borderRadius": "10px",
            "display": "inline-block"
        }
    elif 10 <= num_red_points < 30:
        status_message = "Warning"
        status_style = {
            "backgroundColor": "orange",
            "color": "white",
            "padding": "10px",
            "borderRadius": "10px",
            "display": "inline-block"
        }
    else:
        status_message = "Undercuts Found"
        status_style = {
            "backgroundColor": "red",
            "color": "white",
            "padding": "10px",
            "borderRadius": "10px",
            "display": "inline-block"
        }

    # Create 3D Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=prep_mesh.points[:, 0], y=prep_mesh.points[:, 1], z=prep_mesh.points[:, 2],
        mode="markers", marker=dict(size=3, color="blue"), name="Prep Mesh"
    ))
    fig.add_trace(go.Scatter3d(
        x=margin_points[:, 0], y=margin_points[:, 1], z=margin_points[:, 2],
        mode="lines", line=dict(color="red", width=4), name="Margin Spline"
    ))
    if len(final_points) > 0:
        fig.add_trace(go.Scatter3d(
            x=final_points[:, 0], y=final_points[:, 1], z=final_points[:, 2],
            mode="markers", marker=dict(size=5, color="red"), name="Final Points"
        ))
    fig.update_layout(scene=dict(aspectmode="data"), title="3D Visualization")

    return fig, status_message, status_style

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
