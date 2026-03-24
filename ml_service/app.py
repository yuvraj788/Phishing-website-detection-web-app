from flask import Flask, request, jsonify
from flask_cors import CORS
from src.predictor import predict_url

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Phishing Detection ML Service is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "success": False,
                "error": "URL is required"
            }), 400

        url = data["url"].strip()

        if not url:
            return jsonify({
                "success": False,
                "error": "URL cannot be empty"
            }), 400

        result = predict_url(url)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/test-predict", methods=["GET"])
def test_predict():
    url = request.args.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "Please provide a url query parameter"
        }), 400

    result = predict_url(url)

    return jsonify({
        "success": True,
        "data": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)