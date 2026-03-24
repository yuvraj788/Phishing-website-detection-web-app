const axios = require("axios");
const dotenv = require("dotenv");

dotenv.config();

const PYTHON_ML_API = process.env.PYTHON_ML_API;

const getPredictionFromPython = async (url) => {
  try {
    const response = await axios.post(`${PYTHON_ML_API}/predict`, {
      url,
    });

    if (!response.data.success) {
      throw new Error(response.data.error || "Python ML service failed");
    }

    return response.data.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(
        error.response.data.error || "Error from Python ML service"
      );
    }

    throw new Error("Unable to connect to Python ML service");
  }
};

module.exports = { getPredictionFromPython };