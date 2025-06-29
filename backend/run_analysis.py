import os
import subprocess
import sys
import shutil

def run_script(script_path):
    """Run a Python script and handle any errors."""
    try:
        print(f"\nRunning {os.path.basename(script_path)}...")
        # Change to the script's directory before running it
        script_dir = os.path.dirname(script_path)
        original_dir = os.getcwd()
        os.chdir(script_dir)
        
        result = subprocess.run([sys.executable, os.path.basename(script_path)], check=True)
        
        # Change back to original directory
        os.chdir(original_dir)
        print(f"Successfully completed {os.path.basename(script_path)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {os.path.basename(script_path)}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error running {os.path.basename(script_path)}: {e}")
        return False

def ensure_directories():
    """Ensure all necessary directories exist."""
    directories = [
        'Classified_Author_CompetencyScore',
        'Classified_Project_CompetencyScore',
        'CompetencyScore',
        'logs',
        'PythonAuthorEmail_data',
        'PythonCommits_data',
        'PythonFiles'
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def main():
    # Get the current directory (backend folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Ensure all necessary directories exist
    ensure_directories()
    
    # Define paths to the scripts
    pydriller_script = os.path.join(current_dir, "PyDriller_ExtractData.py")
    analyze_script = os.path.join(current_dir, "AnalyzeCompetencyScore.py")
    visualize_script = os.path.join(current_dir, "..", "visualization", "Visualize_Code")
    
    # Run PyDriller_ExtractData.py first
    print("Step 1: Running PyDriller_ExtractData.py")
    if not run_script(pydriller_script):
        print("Failed to run PyDriller_ExtractData.py. Stopping execution.")
        return
    
    # Run AnalyzeCompetencyScore.py
    print("\nStep 2: Running AnalyzeCompetencyScore.py")
    if not run_script(analyze_script):
        print("Failed to run AnalyzeCompetencyScore.py.")
        return
    
    # Run visualization script
    print("\nStep 3: Running visualization")
    if not run_script(visualize_script):
        print("Failed to run visualization script.")
        return
    
    print("\nAnalysis complete! All scripts have been executed successfully.")

if __name__ == "__main__":
    main() 