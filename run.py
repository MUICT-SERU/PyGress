import os
import shutil
import subprocess
from webui.app import app
import pandas as pd

def cleanup_directories():
    """Clean up all specified directories and files."""
    directories_to_clean = [
        'backend/Classified_Author_CompetencyScore',
        'backend/Classified_Project_CompetencyScore',
        'backend/CompetencyScore',
        'backend/logs',
        'backend/PythonAuthorEmail_data',
        'backend/PythonCommits_data',
        'backend/PythonFiles'
    ]
    
    files_to_clean = [
        'backend/all_projects_done.csv',
        'backend/all_projects_undone.csv',
        'backend/filtered_all_projects.csv',
        'backend/projects_counts.txt'
    ]
    
    # Remove directories
    for directory in directories_to_clean:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"Cleaned up directory: {directory}")
    
    # Remove files
    for file in files_to_clean:
        if os.path.exists(file):
            os.remove(file)
            print(f"Cleaned up file: {file}")

    # Remove Timestamp.log specifically if it exists
    timestamp_log = 'backend/logs/Timestamp.log'
    if os.path.exists(timestamp_log):
        os.remove(timestamp_log)
        print(f"Cleaned up file: {timestamp_log}")

def run_analysis():
    """Run the analysis script."""
    try:
        result = subprocess.run(['python', 'backend/run_analysis.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running analysis: {e}")
        return False

# Make these functions available to the app
app.cleanup_directories = cleanup_directories
app.run_analysis = run_analysis

print("✅ Flask is starting...")

if __name__ == "__main__":
    app.run(debug=True)

