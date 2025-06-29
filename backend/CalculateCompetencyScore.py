import csv
import os
import json
from collections import defaultdict
from typing import Set

def categorize_and_calculate(file_path, projects_with_underscores):
    # Dictionary to store categorized data
    categorized_data = defaultdict(dict)
    
    # Read the CSV file
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        
        # Process each row in the CSV
        for row in reader:
            if len(row) != 7:
                print(f"Skipping malformed row: {row}")
                continue  # Skip rows that don't have exactly 7 values
            
            repo, file_name, _, _, _, _, level = row
            
            # Extract attributes from the file name
            parts = file_name.split('_')
            project_name = extract_project_name(file_name, projects_with_underscores)  # Extracting project name correctly
            author_id = parts[-5]
            author_date_format = parts[-4]
            author_time_format = parts[-3]
            classification = parts[-2].lower()  # Convert classification to lowercase
            
            if classification == 'after':
                classification = 'After'
            elif classification == 'before':
                classification = 'Before'

            # Initialize data for the repository if it's the first occurrence
            if repo not in categorized_data:
                categorized_data[repo] = {
                    "CommitHash": repo,
                    "ProjectName": project_name,
                    "AuthorID": author_id,
                    "AuthorDateFormat": author_date_format,
                    "AuthorTimeFormat": author_time_format,
                    "Levels": {
                        "After": {f"{level}": 0 for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']},  # Initialize all levels with 0
                        "Before": {f"{level}": 0 for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']},  # Initialize all levels with 0
                        "Difference": defaultdict(int)  # Use uppercase keys
                    }
                }
                
            # Update level counts based on classification
            levels = categorized_data[repo]["Levels"]
            level_counts = levels[classification]  # Use lowercase keys
            level_counts[level] += 1
                
    # Calculate the difference between "After" and "Before"
    for repo, data in categorized_data.items():
        after_levels = data["Levels"]["After"]  # Use uppercase keys
        before_levels = data["Levels"]["Before"]  # Use uppercase keys
        difference_levels = data["Levels"]["Difference"]  # Use uppercase keys
        
        # Ensure all levels from 'A1' to 'C2' are included, even if they don't exist
        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            after_count = after_levels[level]
            before_count = before_levels[level]
            difference_levels[level] = after_count - before_count
    
    return categorized_data

def save_to_json(data, output_folder):
    for repo, repo_data in data.items():
        json_filename = os.path.join(output_folder, f"{repo}.json")
        os.makedirs(os.path.dirname(json_filename), exist_ok=True)
        
        # Write data to JSON file
        with open(json_filename, 'w') as jsonfile:
            json.dump(repo_data, jsonfile, indent=4)

def extract_project_name(file_name, projects_with_underscores):
    """
    Extracts project name from the file name.

    Args:
        file_name (str): The name of the CSV file.
        projects_with_underscores (Set[str]): Set of project names containing underscores.

    Returns:
        str: Project name extracted from the file name.
    """
    for project_name in projects_with_underscores:
        if project_name in file_name:
            return project_name
    return file_name.split('_')[1]

def get_projects_with_underscores(all_projects_file: str) -> Set[str]:
    """
    Extracts project names containing underscores from the CSV file.

    Args:
        all_projects_file (str): Path to the CSV file containing project names.

    Returns:
        Set[str]: Set of project names containing underscores.
    """
    projects_with_underscores = set()
    with open(all_projects_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            project_name = row['ProjectName']
            if '_' in project_name:
                projects_with_underscores.add(project_name)
    return projects_with_underscores

def main():
    # Input folder containing all {ProjectName}_CompetencyScore.csv files
    input_folder = 'CompetencyScore'

    # Output folder for classified JSON files based on ProjectName
    classified_project_folder = 'Classified_Project_CompetencyScore'

    # Output folder for classified JSON files based on AuthorID
    classified_author_folder = 'Classified_Author_CompetencyScore'

    # Path to the CSV file containing project names
    all_projects_file = 'filtered_all_projects.csv'

    # Get projects with underscores
    projects_with_underscores = get_projects_with_underscores(all_projects_file)

    # Iterate through all CSV files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('_CompetencyScore.csv'):
            file_path = os.path.join(input_folder, file_name)

            # Check if the file name contains underscores
            if '_' not in file_name:
                # Create a folder based on the file name
                folder_name = file_name[:-17]  # Remove '_CompetencyScore.csv'
                project_folder = os.path.join(classified_project_folder, folder_name)
                os.makedirs(project_folder, exist_ok=True)

                # Move the file to the created folder
                dest_file_path = os.path.join(project_folder, file_name)
                shutil.move(file_path, dest_file_path)
                continue  # Skip the rest of the loop for this file
            
            # Categorize and calculate data for the current CSV file
            categorized_data = categorize_and_calculate(file_path, projects_with_underscores)

            # Save categorized data to JSON files based on ProjectName
            for repo, repo_data in categorized_data.items():
                project_name = repo_data['ProjectName']
                # print(f"Analyzing {project_name}")
                author_time_format = repo_data['AuthorTimeFormat']
                
                # Check if the project name contains underscores
                if '_' in project_name:
                    project_name = extract_project_name(file_name, projects_with_underscores)
                
                # # Check if the AuthorTimeFormat matches the pattern
                if not author_time_format.isdigit() or len(author_time_format) != 6:
                    continue  # Skip this entry if the AuthorTimeFormat doesn't match the pattern
        
                project_folder = os.path.join(classified_project_folder, project_name)
                save_to_json({repo: repo_data}, project_folder)


            # Save categorized data to JSON files based on AuthorID
            for repo, repo_data in categorized_data.items():
                author_id = repo_data['AuthorID']
                author_folder = os.path.join(classified_author_folder, author_id)
                save_to_json({repo: repo_data}, author_folder)


if __name__ == "__main__":
    main()

