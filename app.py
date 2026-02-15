from flask import Flask, render_template, request, jsonify, send_from_directory
from database import init_db, add_review, get_reviews
import os

app = Flask(__name__)

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html')

@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    """API endpoint to get all reviews"""
    reviews = get_reviews()
    return jsonify(reviews)

@app.route('/api/reviews', methods=['POST'])
def create_review():
    """API endpoint to create a new review"""
    data = request.json
    
    # Validate data
    if not data.get('name') or not data.get('rating') or not data.get('text'):
        return jsonify({'error': 'All fields are required'}), 400
    
    if not (1 <= int(data.get('rating')) <= 5):
        return jsonify({'error': 'Rating must be between 1-5'}), 400
    
    # Add review to database
    review = add_review(
        name=data['name'],
        rating=int(data['rating']),
        text=data['text']
    )
    
    return jsonify(review), 201

@app.route('/download/scanYourWeb.zip')
def download_file():
    """Endpoint for downloading the ZIP file with the application"""
    from flask import make_response
    
    response = make_response(send_from_directory('static', 'scanYourWeb.zip', as_attachment=True))
    
    # Add security headers to prevent browser blocking
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename=scanYourWeb.zip'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'none'"
    
    return response

if __name__ == '__main__':
    # For Railway, use port from environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
