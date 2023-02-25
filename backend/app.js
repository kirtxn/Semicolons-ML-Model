const express = require("express");
const axios = require("axios");
const app = express();
app.use(express.json());

app.post("/rank-employees", async (req, res) => {
  const jobDescription = req.body.jobDescription;

  // Call the Flask endpoint to rank employees
  const response = await axios.post(
    "http://localhost:5000/api/rank-employees",
    {
      jobDescription,
    }
  );

  // Return the ranked employees to the client
  const rankedEmployees = response.data;
  res.json(rankedEmployees);
});

app.post("/api/get-resume-skills", async (req, res) => {
  try {
    const resume = req.file;
    const response = await axios.post(
      "http://localhost:5000/get-resume-skills",
      {
        resume,
      }
    );
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Error processing file" });
  }
});
app.listen(3000, () => {
  console.log("Node.js server listening on port 3000");
});
