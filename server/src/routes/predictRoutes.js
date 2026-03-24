const express = require("express");
const { predictUrlController } = require("../controllers/predictController");

const router = express.Router();

router.post("/predict", predictUrlController);

module.exports = router;