const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const predictRoutes = require("./routes/predictRoutes");

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Node backend is running",
  });
});

app.use("/api", predictRoutes);

const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});