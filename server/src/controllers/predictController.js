const { isValidUrl } = require("../utils/validators");
const { getPredictionFromPython } = require("../services/pythonService");

const predictUrlController = async (req, res) => {
  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({
        success: false,
        error: "URL is required",
      });
    }

    if (!isValidUrl(url)) {
      return res.status(400).json({
        success: false,
        error: "Please enter a valid URL",
      });
    }

    const result = await getPredictionFromPython(url);

    return res.status(200).json({
      success: true,
      data: result,
    });
  } catch (error) {
    return res.status(500).json({
      success: false,
      error: error.message || "Internal server error",
    });
  }
};

module.exports = { predictUrlController };