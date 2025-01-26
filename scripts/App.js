import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, MeshDistortMaterial, Box } from '@react-three/drei';
import { Dropdown, Slider, Button, Form, Container, Row, Col, Alert, Checkbox } from 'react-bootstrap';
import { useDropzone } from 'react-dropzone';

function App() {
  const [crownFolder, setCrownFolder] = useState('');
  const [prepFolder, setPrepFolder] = useState('');
  const [selectedCase, setSelectedCase] = useState('');
  const [orangeThreshold, setOrangeThreshold] = useState(1.5);
  const [blueThreshold, setBlueThreshold] = useState(1.0);
  const [featureToggle, setFeatureToggle] = useState([]);
  const [cases, setCases] = useState([]);
  const [message, setMessage] = useState('');

  const { getRootProps, getInputProps } = useDropzone({
    accept: '.ply',
    onDrop: (acceptedFiles) => {
      console.log(acceptedFiles);
    }
  });

  // Fetch available cases based on folders
  useEffect(() => {
    if (crownFolder && prepFolder) {
      fetchCases(crownFolder, prepFolder);
    }
  }, [crownFolder, prepFolder]);

  const fetchCases = (crownFolder, prepFolder) => {
    // This can be an API call to the backend that returns a list of cases
    // For example, use fetch to get a list of case files from the server
    setCases([
      { label: 'Case 1', value: 'case1' },
      { label: 'Case 2', value: 'case2' },
      // Add other cases dynamically
    ]);
  };

  // This would be used for calling the backend to fetch mesh data and PCA/curvature logic
  const updateVisualization = () => {
    setMessage('Processing...');
    // Add the logic to call your backend API that performs PCA, calculates distances, etc.
  };

  return (
    <Container>
      <Row className="mt-4">
        <Col md={12} style={{ textAlign: 'center' }}>
          <h1>Interactive Thickness Analysis App</h1>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={6}>
          <Form.Label>Crown Shell Folder:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter path to crown shell folder"
            value={crownFolder}
            onChange={(e) => setCrownFolder(e.target.value)}
          />
        </Col>
        <Col md={6}>
          <Form.Label>Crown Bottom Mesh Folder:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter path to preparation folder"
            value={prepFolder}
            onChange={(e) => setPrepFolder(e.target.value)}
          />
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={12}>
          <Form.Label>Select Case:</Form.Label>
          <Dropdown onSelect={(e) => setSelectedCase(e)}>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
              {selectedCase || 'Select a case'}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {cases.map((caseItem) => (
                <Dropdown.Item key={caseItem.value} eventKey={caseItem.value}>
                  {caseItem.label}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={12}>
          <Form.Label>Orange Region Threshold (Above Distance):</Form.Label>
          <Slider
            value={orangeThreshold}
            min={0}
            max={3}
            step={0.1}
            onChange={(value) => setOrangeThreshold(value)}
          />
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={12}>
          <Form.Label>Blue Region Threshold (Below Distance):</Form.Label>
          <Slider
            value={blueThreshold}
            min={0}
            max={3}
            step={0.1}
            onChange={(value) => setBlueThreshold(value)}
          />
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={12}>
          <Form.Label>Show Features:</Form.Label>
          <Checkbox.Group
            value={featureToggle}
            onChange={(value) => setFeatureToggle(value)}
          >
            <Checkbox value="pca">Show Third PCA Component</Checkbox>
            <Checkbox value="curvature">Show Highest Curvature Points</Checkbox>
          </Checkbox.Group>
        </Col>
      </Row>

      <Row className="mt-4">
        <Col md={12} style={{ textAlign: 'center' }}>
          <Button onClick={updateVisualization}>Update Visualization</Button>
        </Col>
      </Row>

      {message && (
        <Row className="mt-4">
          <Col md={12}>
            <Alert variant="info">{message}</Alert>
          </Col>
        </Row>
      )}

      <Row className="mt-4">
        <Col md={12}>
          <Canvas style={{ height: '70vh' }}>
            <OrbitControls />
            <ambientLight />
            <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
            {/* Replace Box with your 3D mesh and PCA logic */}
            <Box args={[2, 2, 2]} position={[-1.2, 0, 0]}>
              <MeshDistortMaterial color="orange" />
            </Box>
            <Box args={[2, 2, 2]} position={[1.2, 0, 0]}>
              <MeshDistortMaterial color="blue" />
            </Box>
          </Canvas>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
