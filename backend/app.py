from flask
import Flask, request, jsonify
from models.classifier import predict_image
from routes.price_scraper import get_price_from_amazon, get_price_from_ebay

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files: return jsonify({"error": "No image uploaded"}), 400

image = request.files['image']
predicted_item = predict_image(image)

# Example: Use the predicted item (like "t-shirt") to fetch price from Amazon/eBay
amazon_price = get_price_from_amazon(predicted_item).get('price')
ebay_price = (get_price_from_ebay(predicted_item).get('price'))

# Example: Averaging the prices
average_price = (amazon_price + ebay_price) / 2

return jsonify({ "item": predicted_item, "amazon_price": amazon_price, "ebay_price": ebay_price, "average_price": average_price })
if __name__ == '__main__': app.run(debug=True)

