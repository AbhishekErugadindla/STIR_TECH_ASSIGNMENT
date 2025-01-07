import os

from flask import Flask, render_template_string, jsonify
from scraper import scrape_twitter
from utils.webdriver import setup_driver

app = Flask(__name__)


@app.route("/")
def home():
    html_template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Twitter Trends</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f8fa;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                button {
                    background-color: #1da1f2;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #1991db;
                }
                h1 {
                    color: #1da1f2;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Twitter Trends Scraper</h1>
                <button onclick="window.location.href='/run-script';">Fetch Latest Trends</button>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_template)


@app.route("/run-script")
def run_script():
    data = scrape_twitter()

    if not data:
        return render_template_string("""
            <h1>Error</h1>
            <p>Failed to fetch trends. Please try again later.</p>
            <button onclick="window.location.href='/';">Go Back</button>
        """)

    html_template = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Twitter Trends Results</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f8fa;
                }}
                .container {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .trend {{
                    padding: 10px;
                    margin: 5px 0;
                    background-color: #f7f9fa;
                    border-radius: 5px;
                }}
                button {{
                    background-color: #1da1f2;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 16px;
                    margin-top: 20px;
                }}
                button:hover {{
                    background-color: #1991db;
                }}
                pre {{
                    background-color: #f7f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Current Twitter Trends</h1>
                <p>Fetched at: {data['timestamp']}</p>

                <div class="trends">
                    <div class="trend">1. {data['trend1']}</div>
                    <div class="trend">2. {data['trend2']}</div>
                    <div class="trend">3. {data['trend3']}</div>
                    <div class="trend">4. {data['trend4']}</div>
                    <div class="trend">5. {data['trend5']}</div>
                </div>

                <button onclick="window.location.href='/';">Fetch New Trends</button>

                <h3>Raw Data:</h3>
                <pre>{str(data)}</pre>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_template)
@app.route("/health")
def health_check():
    try:
        driver = setup_driver()
        driver.quit()
        return jsonify({"status": "healthy", "browser": "working"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
