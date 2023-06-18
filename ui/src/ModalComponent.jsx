/* eslint-disable react/prop-types */
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import EntriesTable from "./EntriesTable";

const ModalComponent = ({ show, handleClose, data }) => {
  return (
    <Modal show={show} onHide={handleClose} dialogClassName="modal-xl">
      <Modal.Header closeButton>
        <Modal.Title>Similar Entries</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <EntriesTable title="Entry" data={data.selectedRow} />
        <br></br>
        <h3>Similar by</h3>
        <hr></hr>
        <EntriesTable title="Color" data={data.similarDataColor} />
        <EntriesTable title="Location" data={data.similarDataLocation} />
        <EntriesTable title="Text" data={data.similarDataText} />
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalComponent;
