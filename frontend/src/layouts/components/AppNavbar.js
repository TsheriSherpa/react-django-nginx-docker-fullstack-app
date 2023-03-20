import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';

export default function AppNavbar({navbarTitle}) {
    return (
        <>
            <Navbar expand="xxl" className="fixed-top" style={{ backgroundColor: "#1d1d1d" }}>
                <Container fluid>
                    <Navbar.Brand>
                        <span style={{ color: "#adadad", fontWeight: "bold" }}>Payment Service</span>
                    </Navbar.Brand>
                    {/* <Nav>
                        <Nav.Link href="#home">Home</Nav.Link>
                        <Nav.Link href="#features">Features</Nav.Link>
                        <Nav.Link href="#pricing">Pricing</Nav.Link>
                    </Nav> */}
                </Container>
            </Navbar>
        </>
    )
}