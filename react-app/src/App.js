import logo from './logo.svg';
//import './App.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Gallery from './Gallery';

function App() {
  return (
    <Container>
        <Row>
            <h1>Flask Image Gallery</h1>
        </Row>
        <Gallery/>
    </Container>
  );
}

export default App;
