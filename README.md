# PyGress 🐍📊

A comprehensive Python competency analysis tool that analyzes GitHub repositories to assess developer competency levels using CEFR (Common European Framework of Reference for Languages) standards.

## 🌟 Features

- **GitHub Repository Analysis**: Automatically clones and analyzes Python repositories
- **CEFR Competency Assessment**: Evaluates code complexity using A1-C2 proficiency levels
- **Interactive Visualizations**: Generates dynamic charts and graphs using Plotly
- **Web Interface**: User-friendly Flask-based web application
- **Multi-Project Support**: Process multiple repositories simultaneously
- **Author Tracking**: Track individual developer contributions and competency evolution
- **Commit Analysis**: Analyze code changes before and after commits

## 📋 Prerequisites

- Python 3.7+
- Git
- Internet connection for repository cloning

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Greeedhub_PyGress
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install flask pandas pydriller plotly pytz git
   ```

3. **Install PyCEFR** (automatically handled by the application):
   The application will automatically clone the PyCEFR repository for competency analysis.

## 🏗️ Project Structure

```
Greeedhub_PyGress/
├── backend/                          # Core analysis modules
│   ├── AnalyzeCompetencyScore.py     # Main competency analysis script
│   ├── CalculateCompetencyScore.py   # Score calculation and categorization
│   ├── PyDriller_ExtractData.py      # Git repository data extraction
│   ├── run_analysis.py               # Orchestration script
│   └── DataPyPI.csv                  # Repository URLs database
├── webui/                            # Web interface
│   ├── app.py                        # Flask application
│   ├── templates/                    # HTML templates
│   └── static/                       # Static assets
├── visualization/                    # Visualization scripts
│   └── Visualize_Code               # Plotly visualization generator
└── run.py                           # Main application entry point
```

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the application**:
   ```bash
   python run.py
   ```

2. **Open your browser** and navigate to `http://localhost:5000`

3. **Enter a GitHub repository URL** and click "Generate Analysis"

4. **View results**:
   - Competency scores for each developer
   - Interactive visualizations
   - Project-level analysis

### Command Line Interface

1. **Add repository URLs** to `backend/DataPyPI.csv`:
   ```csv
   github_url
   https://github.com/username/repository
   ```

2. **Run the analysis**:
   ```bash
   python backend/run_analysis.py
   ```

3. **View results** in the generated directories:
   - `backend/CompetencyScore/` - Raw competency data
   - `backend/Classified_Project_CompetencyScore/` - Project-organized results
   - `backend/Classified_Author_CompetencyScore/` - Author-organized results
   - `visualization/` - Interactive HTML visualizations

## 📊 Understanding the Results

### Competency Levels (CEFR)

- **A1 (Beginner)**: Basic Python syntax and simple operations
- **A2 (Elementary)**: Basic functions and data structures
- **B1 (Intermediate)**: Object-oriented programming concepts
- **B2 (Upper Intermediate)**: Advanced Python features and patterns
- **C1 (Advanced)**: Complex algorithms and design patterns
- **C2 (Mastery)**: Expert-level Python programming

### Output Files

1. **CSV Files**: Raw competency scores for each file
2. **JSON Files**: Categorized data by project and author
3. **HTML Visualizations**: Interactive charts showing:
   - Spider charts for overall competency distribution
   - Time-series analysis of competency evolution
   - Individual developer competency profiles

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PyCEFR**: For the competency analysis framework
- **PyDriller**: For Git repository mining capabilities
- **Plotly**: For interactive visualizations
- **Flask**: For the web interface framework

---

**Note**: This tool is designed for educational and research purposes. Competency assessments should be used as one of many indicators of developer skill, not as the sole measure of programming ability. 
