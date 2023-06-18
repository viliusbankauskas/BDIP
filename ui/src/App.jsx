import "bootstrap/dist/css/bootstrap.min.css";

import { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import Spinner from "react-bootstrap/Spinner";

import EntriesTable from "./EntriesTable";
import ModalComponent from "./ModalComponent";
import ToastComponent from "./ToastComponent";

function App() {
  const [allEntries, setAllEntries] = useState(null);
  const [similarDataText, setSimmilarText] = useState(null);
  const [similarDataLocation, setSimmilarLocation] = useState(null);
  const [similarDataColor, setSimmilarColor] = useState(null);
  const [selectedRow, setSelectedRow] = useState(null);

  const [showModal, setShowModal] = useState(false);
  const [showToast, setShowToast] = useState(false);

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000");
      const json = await response.json();
      setAllEntries(json);
      console.log("Fetched all entries.");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleEntrySearch = async (entry) => {
    setShowToast(true);

    try {
      const response = await fetch(`http://127.0.0.1:5000/entry`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(entry),
      });
      const json = await response.json();
      setSelectedRow(json.entry);
      setSimmilarText(json.similar_by_text);
      setSimmilarColor(json.similar_by_color);
      setSimmilarLocation(json.similar_by_location);

      setShowModal(true);
      setShowToast(false);

      console.log("Similar: ", json);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleClose = () => {
    setShowModal(false);
    console.log("Refetching:");
    setAllEntries(null);
    fetchEntries();
  };

  return (
    <div>
      <Container
        fluid
        style={{ position: "relative", width: "80%", marginTop: "2em" }}
      >
        {allEntries && allEntries.length > 0 ? (
          <EntriesTable
            title="Entries"
            data={allEntries}
            handleEntrySearch={handleEntrySearch}
          />
        ) : (
          <div
            style={{
              position: "fixed",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
            }}
          >
            <Spinner animation="border" role="status"></Spinner>
          </div>
        )}

        <ToastComponent
          show={showToast}
          handleClose={() => setShowToast(false)}
        />
      </Container>

      <ModalComponent
        show={showModal}
        handleClose={handleClose}
        data={{
          selectedRow,
          similarDataText,
          similarDataLocation,
          similarDataColor,
        }}
      />
    </div>
  );
}

export default App;
