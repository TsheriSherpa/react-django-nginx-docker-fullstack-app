import { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";


export default function AddAppModal({ modalOpen, setToggleModal }) {
    const [name, setName] = useState("")
    const [error, setError] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const handleModalToggle = () => {
        setError("")
        setToggleModal(!modalOpen)
    }
    
    const handleSubmit = (e) => {
        setError("")
        e.preventDefault();

        if (name == "" || username == "" || password == "") {
            setError('Please fill all the fields')
        }else if (password.length < 8) {
            setError('Secret key must be 8 characters long')
        } else {}

        if (error == "") {
            console.log("submitting form");
        }

    }

    return (
        <Modal show={modalOpen} onHide={() => handleModalToggle()} className="modal-lg">
            <Modal.Header closeButton>
                <Modal.Title>Add App Modal</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    { error && <span style={{ color:"red" }}>{error}</span>}
                    <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                        <Form.Label>App Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter App Name"
                            onChange={(e) => setName(e.target.value)}
                            required
                            autoFocus
                        />
                        </Form.Group>
                    <Form.Group className="mb-3" controlId="exampleForm.ControlInput2">
                        <Form.Label>App Username</Form.Label>
                        <Form.Control
                            type="text"
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter App Username"
                            autoFocus
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="exampleForm.ControlInput3">
                        <Form.Label>App Secret</Form.Label>
                        <Form.Control
                            onChange={(e) => setPassword(e.target.value)}
                            minLength="10"
                            type="password"
                            placeholder="Enter App Secret"
                            autoFocus
                            required
                        />
                    </Form.Group>
                    <Button variant="primary" type="submit" style={{ marginRight: "10px" }} onClick={handleSubmit}>
                        Save
                    </Button>
                    <Button variant="secondary" onClick={() => handleModalToggle()}>
                        Close
                    </Button>
                </Form>
            </Modal.Body>
            <Modal.Footer>
            </Modal.Footer>
        </Modal>
    );
}