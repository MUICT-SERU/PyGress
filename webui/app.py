from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import pandas as pd

app = Flask(__name__, static_folder="static", template_folder="templates")

# --- Path Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_CSV = os.path.join(BASE_DIR, '..', 'backend', 'DataPyPI.csv')
RESULTS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'backend', 'CompetencyScore'))
VISUALIZATION_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'visualization'))

@app.route("/", methods=["GET"])
def index():
    return render_template("competencyTools.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        github_url = request.json.get('github_url', '').strip()
        if not github_url:
            return jsonify({'error': 'No GitHub URL provided'}), 400

        # Clean up directories and files
        app.cleanup_directories()
        
        # Add GitHub URL to DataPyPI.csv
        df = pd.DataFrame({'github_url': [github_url]})
        df.to_csv(DATA_CSV, index=False)
        
        # Run analysis
        if app.run_analysis():
            # Get the project name from the GitHub URL
            project_name = github_url.split('/')[-1]
            visualization_file = f"{project_name}_Visualization.html"
            
            if os.path.exists(os.path.join(VISUALIZATION_DIR, visualization_file)):
                return jsonify({
                    'message': 'Analysis completed successfully',
                    'visualization': visualization_file
                }), 200
            else:
                return jsonify({'error': 'Visualization file not found'}), 500
        else:
            return jsonify({'error': 'Analysis failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Serve results files ---
@app.route("/results/<path:filename>")
def results_file(filename):
    return send_from_directory(RESULTS_DIR, filename)

# --- Serve visualization files ---
@app.route("/visualization/<path:filename>")
def visualization_file(filename):
    return send_from_directory(VISUALIZATION_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
