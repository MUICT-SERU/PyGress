import subprocess
import os
import shutil
import csv
import time
import glob
from datetime import datetime

def clone_repository():
    print("Step 2.1: Clone PyCEFR repo")
    if not os.path.exists('pycefr'):
        subprocess.run(['git', 'clone', 'https://github.com/anapgh/pycefr.git'])
        print("Successfully cloned pycefr\n")
    else:
        print("Directory 'pycefr' already exists. Skipping cloning.\n")

def create_directory(directory_name):
    print(f"Step 2.2: Create directory: {directory_name}")
    if not os.path.exists(directory_name):
        os.makedirs(directory_name, exist_ok=True)
        print(f"Successfully created {directory_name}\n")
    else:
        print(f"Directory '{directory_name}' already exists. Skipping creation.\n")

def create_csv_files():
    print("Step 2.3: Create csv files (filtered_all_projects.csv)")
    if not os.path.exists('filtered_all_projects.csv'):
        with open(r'C:\Users\Oily_brd\Desktop\Greeedhub_PyGress\backend\DataPyPI.csv', 'r', encoding='utf-8') as input_file, \
             open('filtered_all_projects.csv', 'w', newline='', encoding='utf-8') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)
            writer.writerow(['URL', 'ProjectName', 'Path', 'Status', 'DeadAliveStatus'])
            next(reader)
            for row in reader:
                url, project_name = row[0], row[1]
                # Remove .git extension if present
                project_name = project_name.replace('.git', '')
                path = f'../PythonFiles/{project_name}'
                writer.writerow([url, project_name, path, '', ''])
        print("Successfully created filtered_all_projects.csv\n")
    else:
        print("File 'filtered_all_projects.csv' already exists. Skipping creation.\n")

def change_directory(directory_name):
    time.sleep(0.5)
    print(f"Step 2.4: Change Directory to {directory_name}\n")
    os.chdir(directory_name)

def run_dict_py():
    print("Step 2.5: Run dict.py\n")
    subprocess.run(['python', 'dict.py'])

def append_to_csv(source_file, target_file, header=None):
    if not os.path.exists(source_file):
        print(f"[Warning] File '{source_file}' not found. Skipping append.")
        return

    with open(source_file, 'r', encoding='utf-8') as source:
        with open(target_file, 'a', newline='', encoding='utf-8') as target:
            reader = csv.reader(source)
            writer = csv.writer(target)

            if os.path.getsize(target_file) == 0 and header is not None:
                writer.writerow(header)

            next(reader, None)
            for row in reader:
                if any(field.strip() for field in row):
                    writer.writerow(row)

def analyze_projects():
    print("Step 2.6: Analyze the projects\n")

    with open('../all_projects_done.csv', 'w', newline='', encoding='utf-8') as done_file:
        writer = csv.DictWriter(done_file, fieldnames=['URL', 'ProjectName', 'Path', 'Status', 'DeadAliveStatus'])
        writer.writeheader()

    with open('../all_projects_undone.csv', 'w', newline='', encoding='utf-8') as undone_file:
        writer = csv.DictWriter(undone_file, fieldnames=['URL', 'ProjectName', 'Path', 'Status', 'DeadAliveStatus'])
        writer.writeheader()

    done_projects = []
    undone_projects = []

    with open('../filtered_all_projects.csv', 'r', encoding='utf-8') as all_projects_file:
        reader = csv.DictReader(all_projects_file)
        for row in reader:
            if row['Status'] == 'Succeeded':
                done_projects.append(row)
            elif row['Status'] == 'NotSucceeded':
                undone_projects.append(row)

    with open('../all_projects_done.csv', 'a', newline='', encoding='utf-8') as done_file:
        writer = csv.DictWriter(done_file, fieldnames=['URL', 'ProjectName', 'Path', 'Status', 'DeadAliveStatus'])
        if done_projects:
            writer.writerows(done_projects)

    with open('../all_projects_undone.csv', 'a', newline='', encoding='utf-8') as undone_file:
        writer = csv.DictWriter(undone_file, fieldnames=['URL', 'ProjectName', 'Path', 'Status', 'DeadAliveStatus'])
        if undone_projects:
            writer.writerows(undone_projects)

    with open('../filtered_all_projects.csv', 'r', encoding='utf-8') as all_projects_file:
        reader = csv.DictReader(all_projects_file)
        for row in reader:
            if row['Status'] != 'Succeeded':
                file_path = f'../CompetencyScore/{row["ProjectName"]}_CompetencyScore.csv'
                if os.path.exists(file_path):
                    os.remove(file_path)

    all_projects = []
    with open('../filtered_all_projects.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_projects.append(row)

    done_count = len(done_projects)
    undone_count = len(undone_projects)

    for row in all_projects:
        done_project_flag = 0
        if row['Status'] != 'Succeeded':
            project_name = row['ProjectName']
            path = row['Path']
            print(f"\nAnalyzing project: {project_name}")

            if not path:
                print(f"Skipping {project_name}, path is empty")
                done_project_flag = 1
                continue

            # Try both with and without .git extension
            project_path = os.path.join('../PythonFiles', project_name).replace("\\", "/")
            project_path_git = os.path.join('../PythonFiles', f"{project_name}.git").replace("\\", "/")
            
            if os.path.exists(project_path):
                actual_path = project_path
            elif os.path.exists(project_path_git):
                actual_path = project_path_git
            else:
                print(f"Project path '{project_path}' or '{project_path_git}' does not exist")
                done_project_flag = 1
                continue

            for author_id in os.listdir(actual_path):
                author_path = os.path.join(actual_path, author_id).replace("\\", "/")
                if not os.path.isdir(author_path):
                    continue

                for commit_dir in os.listdir(author_path):
                    commit_path = os.path.join(author_path, commit_dir).replace("\\", "/")
                    if not os.path.isdir(commit_path):
                        continue

                    print(f"Analyzing commit: {commit_path}")
                    try:
                        # Run pycerfl.py and capture both stdout and stderr
                        result = subprocess.run(['python', 'pycerfl.py', 'directory', commit_path], 
                                             capture_output=True, 
                                             text=True)
                        
                        # Log the output and errors
                        log_file = f'../logs/{project_name}_{commit_dir}_pycerfl.log'
                        os.makedirs('../logs', exist_ok=True)
                        timestamp = datetime.now().isoformat()
                        with open(log_file, 'w', encoding='utf-8') as f:
                            f.write(f"=== Timestamp ===\n{timestamp}\n")
                            f.write(f"=== STDOUT ===\n{result.stdout}\n")
                            f.write(f"=== STDERR ===\n{result.stderr}\n")
                            f.write(f"=== RETURN CODE ===\n{result.returncode}\n")
                        # Append to central Timestamp.log
                        with open('../logs/Timestamp.log', 'a', encoding='utf-8') as tslog:
                            tslog.write(f"{timestamp} {os.path.basename(log_file)}\n")

                        if os.path.exists('data.csv'):
                            target_file = f'../CompetencyScore/{project_name}_CompetencyScore.csv'
                            append_to_csv('data.csv', target_file, header=['Repository', 'File Name', 'Class', 'Start Line', 'End Line', 'Displacement', 'Level'])
                            os.remove('data.csv')
                        else:
                            print(f"[Warning] data.csv not generated for {commit_path}")
                            print(f"Check log file: {log_file}")
                            done_project_flag = 1

                    except UnicodeDecodeError as e:
                        print(f"UnicodeDecodeError: {e} — Skipping this commit.")
                        done_project_flag = 1
                        continue

            if done_project_flag == 0:
                row['Status'] = 'Succeeded'
                done_count += 1
            else:
                row['Status'] = 'NotSucceeded'
                undone_count += 1

            with open('../filtered_all_projects.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['URL', 'ProjectName', 'Path', 'Status', 'DeadAliveStatus'])
                writer.writeheader()
                writer.writerows(all_projects)

            print("\nAnalysis complete for project:", project_name)

            with open('../projects_counts.txt', 'w') as txt_file:
                txt_file.write(f"Number of successfully recorded projects: {done_count}\n")
                txt_file.write(f"Number of unsuccessfully recorded projects: {undone_count}\n")

def calculate_competencyScore():
    print("Step 7: Calculate CompetencyScore")
    subprocess.run(['python', 'CalculateCompetencyScore.py'])

def classify_folders(input_folder, csv_file):
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            project_name = row['ProjectName']
            status = row['DeadAliveStatus']
            source_folder = os.path.join(input_folder, project_name)
            if status.lower() == 'dead':
                destination_folder = os.path.join('CompetencyScore_Dead', project_name)
            elif status.lower() == 'alive':
                destination_folder = os.path.join('CompetencyScore_Alive', project_name)
            else:
                print(f"Ignoring project '{project_name}' with invalid status '{status}'")
                continue

            if os.path.exists(source_folder):
                shutil.move(source_folder, destination_folder)
                print(f"Moved '{project_name}' to '{destination_folder}'")
            else:
                print(f"Project '{project_name}' not found in '{input_folder}'")

if __name__ == "__main__":
    # Delete the central Timestamp.log file before running new analysis
    tslog_path = os.path.join('..', 'logs', 'Timestamp.log')
    if os.path.exists(tslog_path):
        os.remove(tslog_path)
    clone_repository()
    create_directory("CompetencyScore")
    create_csv_files()
    change_directory("pycefr")
    run_dict_py()
    time.sleep(2)
    analyze_projects()
    change_directory("..")
    calculate_competencyScore()
    classify_folders("Classified_Project_CompetencyScore", "filtered_all_projects.csv")
