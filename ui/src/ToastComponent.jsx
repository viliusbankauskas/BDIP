/* eslint-disable react/prop-types */
import { useEffect, useState } from "react";
import Toast from "react-bootstrap/Toast";

function ToastComponent({ show, handleClose }) {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    if (show) {
      const interval = setInterval(() => {
        setSeconds((seconds) => seconds + 1);
      }, 1000);
      return () => clearInterval(interval);
    } else {
      setSeconds(0);
    }
  }, [show]);

  return (
    <Toast
      onClose={handleClose}
      show={show}
      style={{
        position: "fixed",
        top: 0,
        margin: "2em",
        right: 0,
      }}
    >
      <Toast.Header>
        <strong className="me-auto">Info</strong>
        <small>{seconds}s ago</small>
      </Toast.Header>
      <Toast.Body>Searching for similar entries.</Toast.Body>
    </Toast>
  );
}

export default ToastComponent;
