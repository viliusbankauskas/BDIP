/* eslint-disable react/prop-types */
import { createClient } from "@supabase/supabase-js";
import { useState, useEffect } from "react";

import Table from "react-bootstrap/Table";

const SUPABASE_URL = "https://rhsviqitxauosudiuaew.supabase.co";
const SUPABASE_ANON_KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJoc3ZpcWl0eGF1b3N1ZGl1YWV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODU3OTU4MjgsImV4cCI6MjAwMTM3MTgyOH0.E-HB9Io5yL_f24uGWl0meRmtvlzv5Se6BaJfo1ZGy8g";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const EntriesTable = ({ title, data, handleEntrySearch = null }) => {
  const response = Array.isArray(data) ? data : [data];
  const [imageUrls, setImageUrls] = useState({});

  useEffect(() => {
    const fetchImageUrls = async () => {
      let urls = {};

      for (const item of response) {
        const { data, error } = supabase.storage
          .from("blobs")
          .getPublicUrl(item.wikidata_id + ".jpg");
        if (error) {
          console.error("Error fetching image URL:", error);
        } else {
          urls[item.wikidata_id] = data.publicUrl;
        }
      }
      setImageUrls(urls);
    };

    fetchImageUrls();
  }, []);

  return (
    <div>
      <br></br>
      <h4>{title}</h4>
      {response && response.length > 0 ? (
        <div style={{ overflow: "auto", maxHeight: "1000px" }}>
          <Table striped bordered hover responsive="md">
            <thead
              style={{
                position: "sticky",
                top: 0,
              }}
            >
              <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Description</th>
                <th>Color</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Image</th>
              </tr>
            </thead>
            <tbody>
              {response.map((item) => (
                <tr
                  key={item.wikidata_id}
                  onClick={
                    handleEntrySearch ? () => handleEntrySearch(item) : null
                  }
                  style={{ cursor: handleEntrySearch ? "pointer" : "default" }}
                >
                  <td>{item.name}</td>
                  <td>{item.wikidata_id}</td>
                  <td>{item.description}</td>
                  <td>{item.top_color}</td>
                  <td>{item.latitude}</td>
                  <td>{item.longitude}</td>
                  <td>
                    <img src={imageUrls[item.wikidata_id]} />
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      ) : (
        <p>No similar entries.</p>
      )}
    </div>
  );
};

export default EntriesTable;
