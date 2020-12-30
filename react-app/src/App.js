import logo from './logo.svg';
//import './App.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import Gallery from './Gallery';

function App() {
  return (
    <Container>
        <Row>
            <h1>Flask Image Gallery</h1>
        </Row>
        <Row>
            <Gallery/>
        </Row>
    </Container>
  );
}

export default App;
