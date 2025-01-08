# import os

# from flask import Flask, render_template_string, jsonify
# from scraper import scrape_twitter
# from utils.webdriver import setup_driver

# app = Flask(__name__)


# @app.route("/")
# def home():
#     html_template = """
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>Twitter Trends</title>
#             <style>
#                 body {
#                     font-family: Arial, sans-serif;
#                     max-width: 800px;
#                     margin: 0 auto;
#                     padding: 20px;
#                     background-color: #f5f8fa;
#                 }
#                 .container {
#                     background-color: white;
#                     padding: 20px;
#                     border-radius: 10px;
#                     box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#                 }
#                 button {
#                     background-color: #1da1f2;
#                     color: white;
#                     border: none;
#                     padding: 10px 20px;
#                     border-radius: 20px;
#                     cursor: pointer;
#                     font-size: 16px;
#                 }
#                 button:hover {
#                     background-color: #1991db;
#                 }
#                 h1 {
#                     color: #1da1f2;
#                 }
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <h1>Twitter Trends Scraper</h1>
#                 <button onclick="window.location.href='/run-script';">Fetch Latest Trends</button>
#             </div>
#         </body>
#     </html>
#     """
#     return render_template_string(html_template)


# @app.route("/run-script")
# def run_script():
#     data = scrape_twitter()

#     if not data:
#         return render_template_string("""
#             <h1>Error</h1>
#             <p>Failed to fetch trends. Please try again later.</p>
#             <button onclick="window.location.href='/';">Go Back</button>
#         """)

#     html_template = f"""
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>Twitter Trends Results</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     max-width: 800px;
#                     margin: 0 auto;
#                     padding: 20px;
#                     background-color: #f5f8fa;
#                 }}
#                 .container {{
#                     background-color: white;
#                     padding: 20px;
#                     border-radius: 10px;
#                     box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#                 }}
#                 .trend {{
#                     padding: 10px;
#                     margin: 5px 0;
#                     background-color: #f7f9fa;
#                     border-radius: 5px;
#                 }}
#                 button {{
#                     background-color: #1da1f2;
#                     color: white;
#                     border: none;
#                     padding: 10px 20px;
#                     border-radius: 20px;
#                     cursor: pointer;
#                     font-size: 16px;
#                     margin-top: 20px;
#                 }}
#                 button:hover {{
#                     background-color: #1991db;
#                 }}
#                 pre {{
#                     background-color: #f7f9fa;
#                     padding: 15px;
#                     border-radius: 5px;
#                     overflow-x: auto;
#                 }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <h1>Current Twitter Trends</h1>
#                 <p>Fetched at: {data['timestamp']}</p>

#                 <div class="trends">
#                     <div class="trend">1. {data['trend1']}</div>
#                     <div class="trend">2. {data['trend2']}</div>
#                     <div class="trend">3. {data['trend3']}</div>
#                     <div class="trend">4. {data['trend4']}</div>
#                     <div class="trend">5. {data['trend5']}</div>
#                 </div>

#                 <button onclick="window.location.href='/';">Fetch New Trends</button>

#                 <h3>Raw Data:</h3>
#                 <pre>{str(data)}</pre>
#             </div>
#         </body>
#     </html>
#     """
#     return render_template_string(html_template)
# @app.route("/health")
# def health_check():
#     try:
#         driver = setup_driver()
#         driver.quit()
#         return jsonify({"status": "healthy", "browser": "working"})
#     except Exception as e:
#         return jsonify({"status": "unhealthy", "error": str(e)}), 500

# if __name__ == "__main__":
#     # Get port from environment variable or default to 8080
#     port = int(os.environ.get("PORT", 8080))
    
#     # Run the application
#     app.run(
#         host="0.0.0.0",
#         port=port,
#         debug=os.environ.get("FLASK_DEBUG", "0") == "1"
#     )
import os
import logging
from datetime import datetime
from flask import Flask, render_template_string, jsonify, Response
from scraper import scrape_twitter
from utils.webdriver import setup_driver
from typing import Union, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# HTML Templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Trends Scraper</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f8fa;
            line-height: 1.6;
        }
        .container {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .button {
            background-color: #1da1f2;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: background-color 0.2s;
            text-decoration: none;
            display: inline-block;
        }
        .button:hover {
            background-color: #1991db;
        }
        .trend {
            padding: 15px;
            margin: 10px 0;
            background-color: #f7f9fa;
            border-radius: 8px;
            border-left: 4px solid #1da1f2;
        }
        .error {
            color: #dc3545;
            padding: 15px;
            background-color: #ffe6e6;
            border-radius: 8px;
            margin: 10px 0;
        }
        h1 {
            color: #1da1f2;
            margin-bottom: 25px;
        }
        pre {
            background-color: #f7f9fa;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 14px;
        }
        .timestamp {
            color: #657786;
            font-size: 14px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

HOME_TEMPLATE = """
{% extends "base_template" %}
{% block content %}
<h1>Twitter Trends Scraper</h1>
<a href="/run-script" class="button">Fetch Latest Trends</a>
{% endblock %}
"""

RESULTS_TEMPLATE = """
{% extends "base_template" %}
{% block content %}
<h1>Current Twitter Trends</h1>
<div class="timestamp">Fetched at: {{ data.timestamp }}</div>

<div class="trends">
    {% for i in range(1, 6) %}
    <div class="trend">{{ i }}. {{ data['trend' + i|string] }}</div>
    {% endfor %}
</div>

<a href="/" class="button" style="margin-top: 20px;">Fetch New Trends</a>

<h3>Raw Data:</h3>
<pre>{{ raw_data }}</pre>
{% endblock %}
"""

ERROR_TEMPLATE = """
{% extends "base_template" %}
{% block content %}
<h1>Error</h1>
<div class="error">
    <p>{{ error_message }}</p>
</div>
<a href="/" class="button">Go Back</a>
{% endblock %}
"""

@app.route("/")
def home() -> str:
    """Render the home page"""
    try:
        return render_template_string(
            HOME_TEMPLATE, 
            base_template=BASE_TEMPLATE
        )
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        return render_error("An unexpected error occurred")

@app.route("/run-script")
def run_script() -> str:
    """Run the Twitter scraper and display results"""
    try:
        logger.info("Starting Twitter scraping process")
        data = scrape_twitter()
        
        if not data:
            return render_error("Failed to fetch trends. Please try again later.")
        
        return render_template_string(
            RESULTS_TEMPLATE,
            base_template=BASE_TEMPLATE,
            data=data,
            raw_data=str(data)
        )
    except Exception as e:
        logger.error(f"Error running scraper: {str(e)}")
        return render_error(f"An error occurred while fetching trends: {str(e)}")

@app.route("/health")
def health_check() -> Response:
    """Health check endpoint for monitoring"""
    try:
        # Test WebDriver setup
        driver = setup_driver()
        driver.quit()
        
        # Return success response
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "browser": "working"
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }), 500

def render_error(message: str) -> str:
    """Helper function to render error template"""
    return render_template_string(
        ERROR_TEMPLATE,
        base_template=BASE_TEMPLATE,
        error_message=message
    )

if __name__ == "__main__":
    # Get port from environment variable or default to 8080
    port = int(os.environ.get("PORT", 8080))
    
    # Run the application
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "0") == "1"
    )
