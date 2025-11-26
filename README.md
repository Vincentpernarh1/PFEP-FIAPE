
# PFEP-FIAPE RPA System

## 📋 Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Module Documentation](#module-documentation)
- [Workflow](#workflow)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **PFEP-FIAPE RPA System** is an advanced automation solution designed for Stellantis/FIAT that automates the process of downloading, processing, and comparing various production reports from RTM (Real-Time Manufacturing) systems. The system handles multiple report types (Reports 29, 32, and 61) and performs comprehensive data analysis including phase-in/phase-out comparisons and weight data enrichment from the E-PER (Electronic Parts Catalog) system.

### Key Capabilities
- **Automated Report Generation**: Generates and downloads multiple vehicle model reports concurrently
- **Multi-threaded Processing**: Parallel download execution for improved performance
- **Data Integration**: Combines data from RTM, PFEP, and E-PER systems
- **Weight Enrichment**: Automatically scrapes missing weight data from E-PER using Playwright
- **Phase Analysis**: Identifies parts being phased-in and phased-out across vehicle models
- **GUI Monitoring**: Real-time process monitoring through Tkinter interface

---

## 🏗️ System Architecture

The system consists of four main Python modules:

```
┌─────────────────────────────────────────────────────────┐
│                    Extract.py (Main)                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │  GUI Interface (Tkinter)                           │ │
│  │  - Process Monitoring                              │ │
│  │  - Log Display                                     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Report Downloaders (Multi-threaded)               │ │
│  │  - Report 32 (Standard)                            │ │
│  │  - Report 29 (Multi-step)                          │ │
│  │  - Report 61 (Multi-step)                          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Post-Processing Pipeline                          │ │
│  │  - CSV Merging                                     │ │
│  │  - Data Filtering                                  │ │
│  │  - Excel Conversion                                │ │
│  │  - Comparison Table Generation                     │ │
│  │  - Weight Enrichment (E-PER Integration)           │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    Selenium          Playwright           Pandas
  (Edge Driver)     (Chromium)         (Data Processing)
```

---

## ✨ Features

### 1. **Report 32 (Standard Download)**
- Downloads bill of materials (BOM) data
- Converts ElementNode to PartNumber format
- Removes trailing digits and leading zeros

### 2. **Report 29 (Production Planning)**
- Processes multiple vehicle models (Toro, Rampage, Renegade, Commanda, Compass)
- Handles batch processing in chunks of 5 models
- Monitors report generation status in real-time
- Merges individual model files into consolidated output

### 3. **Report 61 (Detailed Component Analysis)**
- Advanced filtering logic based on:
  - Column 6 = 2
  - Column 7 ∈ {1, 2, 3}
  - Column 8 ∈ {1}
- Includes `fQty` (quantity) data
- Generates unique keys: `PartNumber_Model`
- Handles duplicate removal

### 4. **E-PER Web Scraping (E_PER.py)**
- Automated login to E-PER system
- Part number search and weight extraction
- Converts grams to kilograms
- Headless browser operation support
- Error handling for missing parts

### 5. **Comparison Analysis**
- **Phase-In Detection**: Parts in RTM but not in PFEP
- **Phase-Out Detection**: Parts in PFEP but not in RTM
- Weight validation and correction
- Description enrichment from Report 32
- Generates multi-sheet Excel output:
  - `Comparativo`: Main comparison table
  - `todos_peso_a_corrigir`: All parts with weight = 1kg
  - `correcao unico por desc`: Unique parts by MATRICULA needing correction

### 6. **GUI Features**
- Real-time log monitoring
- Process status tracking
- Thread-safe logging with queue system
- Professional dark theme interface

---

## 💻 Requirements

### Software Dependencies

```python
# Core Libraries
Python 3.8+

# Web Automation
selenium >= 4.0.0
playwright >= 1.40.0

# Data Processing
pandas >= 1.3.0
openpyxl >= 3.0.0
xlsxwriter >= 3.0.0

# Date Handling
python-dateutil >= 2.8.0

# GUI
tkinter (built-in with Python)

# System
pathlib (built-in with Python)
threading (built-in with Python)
queue (built-in with Python)
subprocess (built-in with Python)
```

### Browser Drivers
- **Edge WebDriver** (`msedgedriver.exe`) - for Selenium automation
- **Chromium** - for Playwright automation (installed in `Driver/chrome-win/chrome.exe`)

### System Requirements
- Windows 10/11 (PowerShell compatible)
- Minimum 4GB RAM (8GB recommended)
- Network access to:
  - `rtmcarroceria.fiat.com.br`
  - `eper-ltm.parts.fiat.com`

---

## 📦 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/Vincentpernarh1/PFEP-FIAPE.git
cd PFEP-FIAPE
```

### Step 2: Install Python Dependencies
```powershell
pip install selenium playwright pandas openpyxl xlsxwriter python-dateutil
```

### Step 3: Install Playwright Browsers
```powershell
python -m playwright install chromium
```

### Step 4: Download Edge WebDriver
1. Check your Microsoft Edge version: `edge://version/`
2. Download matching EdgeDriver from [Microsoft Edge Driver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
3. Place `msedgedriver.exe` in the `Driver/` folder

### Step 5: Verify Chromium Installation
Ensure Chromium browser is located at:
```
Driver/chrome-win/chrome.exe
```

---

## ⚙️ Configuration

### 1. User Credentials (`Usuario.json`)
```json
{
  "Usuario": "YOUR_USERNAME",
  "Senha": "YOUR_PASSWORD"
}
```
⚠️ **Security Note**: Never commit credentials to version control. Add `Usuario.json` to `.gitignore`.

### 2. Vehicle Models (`Modelos.json`)
```json
{
    "Toro": "2261 - 0 (**)",
    "Rampage": "2910 - 0 (**)",
    "Renegade": "5211 - 1 (**)",
    "Commanda": "5980 - 0 (**)",
    "Compass": "5511 - 1 (**)"
}
```
**Format**: `"InternalName": "ModelCode - Version (*)"`

### 3. Global Configuration Variables

Located in `Extract.py`:
```python
# Directory Structure
DRIVER_FOLDER_NAME = "Driver"
DRIVER_NAME = "msedgedriver.exe"
REPORTS_FOLDER_NAME = "Reports"
MODELS_SUBFOLDER_NAME_61 = "Modelos_61"
MODELS_SUBFOLDER_NAME_29 = "Modelos_29"

# URLs
BASE_URL = "rtmcarroceria.fiat.com.br/bom/Functions/AllactivitiesList.aspx?idPlant=240"
BASE_URL_RELATORIO_61 = "rtmcarroceria.fiat.com.br/bom/Elab/elab61.aspx?idPlant=240&idElaborationType=61"
BASE_URL_RELATORIO_29 = "rtmcarroceria.fiat.com.br/bom/Elab/elab29.aspx?idPlant=240&idElaborationType=29"

# Configuration Files
JSON_CREDENTIALS_FILE = "Usuario.json"
JSON_MODELS_FILE = "Modelos.json"
```

---

## 🚀 Usage

### Running the Main Application

#### Option 1: GUI Mode (Recommended)
```powershell
python Extract.py
```
1. The GUI window will open
2. Click **"🚀 Start Process"** button
3. Monitor progress in the log panel
4. Wait for completion message

#### Option 2: Test Mode (Individual Components)
```powershell
# Test Report 61 only
python teste.py

# Test E-PER scraping
python E_PER.py

# Test specific report extraction
python Extraction_report_61.py
```

### Expected Runtime
- **Report 32**: ~2 minutes
- **Report 29**: ~15-30 minutes (5 models × 3-6 min each)
- **Report 61**: ~15-30 minutes (5 models × 3-6 min each)
- **Post-Processing**: ~5 minutes
- **Total**: ~40-70 minutes

---

## 📁 Project Structure

```
PFEP-FIAPE/
│
├── Extract.py                 # Main application with GUI
├── E_PER.py                   # E-PER weight scraping module
├── Extraction_report_61.py    # Legacy Report 61 processor
├── teste.py                   # Test/development script
│
├── Usuario.json               # User credentials (DO NOT COMMIT)
├── Modelos.json               # Vehicle model definitions
├── Modelos copy.json          # Backup model definitions
│
├── README.md                  # This documentation
│
├── Driver/                    # Browser drivers
│   ├── msedgedriver.exe       # Edge WebDriver
│   └── chrome-win/            # Chromium browser
│       └── chrome.exe
│
└── Reports/                   # Generated reports (auto-created)
    ├── Modelos_61/            # Individual Report 61 files
    ├── Modelos_29/            # Individual Report 29 files
    ├── Relatorio 32.xlsx      # Report 32 output
    ├── Todos Modelos_61.xlsx  # Merged Report 61
    ├── Todos Modelos_29.xlsx  # Merged Report 29
    └── Todos Comparativos.xlsx # Final comparison analysis
```

---

## 📚 Module Documentation

### `Extract.py` - Main Application

#### Class: `App`
**Purpose**: Tkinter GUI application for process monitoring

**Key Methods**:
- `__init__(self, root)`: Initialize GUI components
- `log_message(self, message)`: Display message in log widget
- `start_process_thread(self)`: Launch RPA process in background thread
- `process_queue(self)`: Handle thread-safe logging
- `check_thread(self)`: Monitor background process completion

#### Function: `main_script_logic()`
**Purpose**: Orchestrates the entire RPA workflow

**Process Flow**:
1. Initialize paths and credentials
2. Create directory structure
3. Launch download threads (32, 29, 61)
4. Wait for completion
5. Execute post-processing pipeline
6. Generate comparison tables

#### Function: `download_standard_report(report_id, new_filename_base, driver_path, reports_path, credentials)`
**Purpose**: Download standard reports (e.g., Report 32)

**Parameters**:
- `report_id`: Report identifier (e.g., "32")
- `new_filename_base`: Output filename without extension
- `driver_path`: Path to Edge WebDriver
- `reports_path`: Output directory
- `credentials`: Login credentials dictionary

**Process**:
1. Configure Edge browser with download directory
2. Authenticate using basic auth URL
3. Select report from dropdown
4. Click download link
5. Wait for file completion
6. Rename and move to final location

#### Function: `process_report_61(new_filename_base, driver_path, reports_path, credentials, base_path)`
**Purpose**: Generate and download Report 61 for all models

**Process**:
1. Load models from `Modelos.json`
2. Split models into chunks of 5
3. For each chunk:
   - Navigate to Report 61 page
   - Set date to 6 months future
   - Submit each model
   - Capture Activity IDs
   - Wait for report generation
   - Download all reports by Activity ID
4. Handle StaleElementReferenceException with re-finding elements

**Key Features**:
- Activity ID mapping for reliable download
- Chunk-based processing to avoid timeouts
- Automatic retry on errors
- Progress logging

#### Function: `merge_models_61(reports_path, base_path)`
**Purpose**: Merge individual Report 61 CSV files into consolidated output

**Process**:
1. Read all CSV files from `Modelos_61/` folder
2. For each file:
   - Extract first 8 columns
   - Add `fQty` column
   - Apply filters:
     - Column 6 (index 5) = 2
     - Column 7 (index 6) ∈ {1, 2, 3}
     - Column 8 (index 7) ∈ {1}
   - Remove duplicates by Column 5
   - Add model code
3. Concatenate all DataFrames
4. Save to `Todos Modelos_61.csv`

#### Function: `process_merged_report_61(reports_path)`
**Purpose**: Convert merged CSV to Excel with enhanced columns

**Transformations**:
1. Rename `vcCode` → `PartNumber`
2. Convert PartNumber to numeric (remove non-numeric)
3. Create `chave` = `PartNumber_Model`
4. Export to Excel format
5. Delete intermediate CSV

#### Function: `Create_Compare_Table(reports_path, credentials)`
**Purpose**: Generate comprehensive phase-in/phase-out analysis

**Input Files**:
- `PFEP - Dados.xlsx` (header at row 9)
- `Relatorio 32.xlsx`
- `Todos Modelos_61.xlsx`

**Process**:
1. **Load and Normalize Data**:
   - Load PFEP with header row 9
   - Create normalized keys (lowercase, trimmed)
   - Create sets for comparison

2. **Phase-In Analysis** (parts in RTM but not PFEP):
   - Identify new parts
   - Merge descriptions/weights from Report 32
   - Filter out parts without descriptions
   - Call `update_weights()` for weight enrichment

3. **Phase-Out Analysis** (parts in PFEP but not RTM):
   - Identify obsolete parts
   - Extract model and part number

4. **Weight Correction Sheets**:
   - `todos_peso_a_corrigir`: All parts with weight = 1kg
   - `correcao unico por desc`: Unique parts by MATRICULA

5. **Output Format**:
   ```
   [Phase-In Columns] | [Empty] | [Phase-Out Columns]
   ```

#### Function: `update_weights(phase_in_df, pfep_df, credentials)`
**Purpose**: Enrich weight data from PFEP and E-PER

**Algorithm**:
1. Filter rows with weight = 1kg
2. Create PFEP lookup dictionaries:
   - `pn_to_weight`: Part Number → Weight
   - `desc_to_weight`: Description → Weight
3. For each part with weight=1:
   - Try matching by Part Number
   - Fallback to matching by Description
   - Update if valid weight found
4. Collect remaining parts with weight=1
5. Call `E_PER()` to scrape missing weights
6. Update DataFrame with scraped weights

**Returns**: Updated DataFrame with enriched weights

---

### `E_PER.py` - E-PER Web Scraping Module

#### Function: `E_PER(pns_for_scraping, credentials)`
**Purpose**: Scrape part weights from E-PER system using Playwright

**Parameters**:
- `pns_for_scraping`: List of part numbers (strings)
- `credentials`: Dictionary with `Usuario` and `Senha` keys

**Process**:
1. **Browser Setup**:
   - Launch Chromium in headless mode
   - Navigate to E-PER login page

2. **Authentication**:
   - Fill username and password
   - Select login type: "Fiat AUTO/MyUser/Link.e.entry"
   - Submit and wait for network idle

3. **Menu Navigation**:
   - Click "Marca" menu
   - Select 4th language option

4. **Part Search Loop**:
   - For each part number:
     - Fill search field (remove last digit)
     - Press Enter
     - Wait for page load
     - Locate "Peso em gramas:" label
     - Extract weight value
     - Convert grams → kilograms
     - Store in results dictionary

5. **Error Handling**:
   - Timeout exceptions per part
   - Browser interaction errors
   - Missing weight data

**Returns**: Dictionary `{part_number: weight_kg}`

**Example**:
```python
credentials = {"Usuario": "SC74349", "Senha": "Caneca050315"}
pns = ["77994840", "34343424"]
weights = E_PER(pns, credentials)
# Output: {"77994840": 0.245, "34343424": 1.350}
```

---

## 🔄 Workflow

### Complete Process Flow

```mermaid
graph TD
    A[Start Extract.py] --> B[Load Configurations]
    B --> C[Create Directory Structure]
    C --> D[Launch Parallel Downloads]
    
    D --> E1[Thread: Report 32]
    D --> E2[Thread: Report 29]
    D --> E3[Thread: Report 61]
    
    E1 --> F[Wait for All Threads]
    E2 --> F
    E3 --> F
    
    F --> G[Merge Report 61 Files]
    G --> H[Process Report 61 to Excel]
    H --> I[Merge Report 29 Files]
    I --> J[Process Report 29 to Excel]
    J --> K[Convert Report 32 to Excel]
    K --> L[Create Comparison Table]
    L --> M[Update Weights from PFEP]
    M --> N{Missing Weights?}
    N -->|Yes| O[E-PER Scraping]
    O --> P[Update DataFrame]
    N -->|No| P
    P --> Q[Generate Multi-Sheet Excel]
    Q --> R[Process Complete]
```

### Detailed Step-by-Step

1. **Initialization** (0-5 seconds)
   - Load `Usuario.json` and `Modelos.json`
   - Verify driver paths
   - Create `Reports/`, `Modelos_61/`, `Modelos_29/` folders

2. **Parallel Downloads** (20-40 minutes)
   - **Thread 1 (Report 32)**:
     - Navigate to activities list
     - Select Report 32 from dropdown
     - Click List Files → Download
     - Save to `Reports/`
   
   - **Thread 2 (Report 29)**:
     - Process 5 models in chunks
     - For each chunk:
       - Submit all 5 models
       - Wait for generation (up to 15 min)
       - Download each individually
     - Save to `Reports/Modelos_29/`
   
   - **Thread 3 (Report 61)**:
     - Process 5 models in chunks
     - For each chunk:
       - Submit all 5 models
       - Map Activity IDs to model names
       - Wait for generation (up to 15 min)
       - Download by Activity ID
     - Save to `Reports/Modelos_61/`

3. **Post-Processing** (5-10 minutes)
   - **Report 61**:
     - Load all CSV files
     - Apply filtering logic
     - Merge into single DataFrame
     - Add PartNumber and chave columns
     - Export to Excel
   
   - **Report 29**:
     - Load all CSV files
     - Add model codes
     - Merge into single DataFrame
     - Export to Excel
   
   - **Report 32**:
     - Load CSV
     - Clean PartNumber column
     - Export to Excel

4. **Comparison Analysis** (5-10 minutes)
   - Load PFEP-Dados, Report 32, Todos Modelos_61
   - Normalize keys (lowercase, trim)
   - Identify phase-in parts (RTM - PFEP)
   - Identify phase-out parts (PFEP - RTM)
   - Merge descriptions/weights from Report 32
   - Update weights from PFEP lookup
   - Scrape missing weights from E-PER
   - Generate 3-sheet Excel output

---

## ⚠️ Error Handling

### Common Issues and Solutions

#### 1. **Stale Element Reference Exception**
**Symptom**: `selenium.common.exceptions.StaleElementReferenceException`

**Cause**: DOM elements change between finding and clicking

**Solution**: Implemented in `process_report_61()`:
```python
# Re-find element on each iteration
row_xpath = f"//table[@id='dgElaborationRequests']//tr[contains(., '{activity_id}')]"
report_row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))
list_files_link = report_row.find_element(...)
```

#### 2. **Download Timeout**
**Symptom**: Files not appearing in download folder

**Cause**: Slow server response, network issues

**Solution**:
```python
def wait_and_get_downloaded_file(download_path, timeout=120):
    # Waits up to 2 minutes for file completion
    # Checks for .crdownload and .tmp exclusion
```

#### 3. **Report Generation Timeout**
**Symptom**: Reports stuck in "Processing" state

**Solution**:
- Maximum wait: 15 minutes
- Periodic refresh every 5 seconds
- Checks for gold background (processing indicator)
- Proceeds with available reports if timeout

#### 4. **Authentication Failure**
**Symptom**: Login redirects or "Invalid credentials" message

**Solution**:
- Verify `Usuario.json` credentials
- Check network connectivity
- Ensure VPN if required
- Use authenticated URL: `https://user:pass@domain.com`

#### 5. **Missing Chromium Driver**
**Symptom**: `FileNotFoundError: Chromium not found`

**Solution**:
```powershell
# Install Playwright browsers
python -m playwright install chromium

# Verify path
Test-Path "Driver/chrome-win/chrome.exe"
```

#### 6. **Weight Not Found in E-PER**
**Symptom**: `"Peso not found for PN {pn}"`

**Cause**: Part number doesn't exist in E-PER catalog

**Handling**:
- Logs warning
- Continues with next part
- Weight remains 1kg in output (flagged for manual review)

---

## 🔧 Troubleshooting

### Debug Mode

Enable detailed logging in `Extract.py`:
```python
# Disable headless mode
edge_options.add_argument("--headless")  # Comment this line

# Increase Selenium logging
edge_options.add_argument("--log-level=0")  # Change from 3 to 0
```

### Performance Optimization

#### Reduce Memory Usage
```python
# In pandas read operations
df = pd.read_csv(file, low_memory=False, chunksize=10000)
for chunk in df:
    process(chunk)
```

#### Speed Up Downloads
```python
# Reduce chunk size for faster iteration
chunk_size = 3  # Default is 5
```

### Logging Best Practices

The GUI uses thread-safe logging:
```python
# In main_script_logic, stdout is redirected
sys.stdout = self.queue_handler

# All print statements automatically appear in GUI
print(f"Processing {model_name}...")
```

### Manual Intervention Points

1. **After Downloads**: Check `Reports/Modelos_61/` and `Reports/Modelos_29/` for completeness
2. **Before Comparison**: Verify `PFEP - Dados.xlsx` is in `Reports/` folder
3. **After Processing**: Review `Todos Comparativos.xlsx` for accuracy

---

## 🧪 Testing

### Unit Testing Individual Components

#### Test Report 61 Download
```powershell
python Extraction_report_61.py
```

#### Test E-PER Scraping
```python
# Edit E_PER.py credentials section
credentials = {"Usuario": "YOUR_USER", "Senha": "YOUR_PASS"}
pns_for_scraping = ["77994840"]  # Test with one part

# Run
python E_PER.py
```

#### Test Data Processing
```python
import pandas as pd

# Test CSV reading
df = pd.read_csv("Reports/Modelos_61/Toro.csv", encoding='utf-16')
print(df.head())

# Test filtering
filtered = df[(df.iloc[:, 5] == 2) & (df.iloc[:, 6].isin([1,2,3]))]
print(f"Filtered rows: {len(filtered)}")
```

---

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit: `git commit -am 'Add new feature'`
5. Push: `git push origin feature/new-feature`
6. Create Pull Request

### Code Style Guidelines

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings to all functions
- Include type hints where applicable
- Comment complex logic

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No credentials committed
- [ ] Error handling implemented
- [ ] Logging added for debugging

---

## 📄 License

This project is proprietary software for Stellantis/FIAT internal use only.

**Copyright © 2025 Stellantis. All rights reserved.**

---

## 📞 Support

For issues or questions:
- **Developer**: Vincent Pernarnha
- **Repository**: https://github.com/Vincentpernarh1/PFEP-FIAPE
- **Email**: [Contact through Stellantis internal channels]

---

## 📈 Version History

### v3.0.0 (Current)
- ✅ Multi-threaded download support
- ✅ GUI monitoring interface
- ✅ E-PER weight scraping integration
- ✅ Advanced comparison analysis with weight correction
- ✅ Multi-sheet Excel output
- ✅ Comprehensive error handling

### v2.0.0
- Report 29 support added
- Chunk-based processing
- Activity ID mapping for Report 61

### v1.0.0
- Initial release
- Report 32 and 61 support
- Basic merging functionality

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Database integration for historical tracking
- [ ] Email notifications on completion/errors
- [ ] Advanced analytics dashboard
- [ ] API integration for real-time data
- [ ] Machine learning for anomaly detection
- [ ] Cloud deployment support
- [ ] Multi-plant configuration
- [ ] Automated report scheduling

### Performance Improvements
- [ ] Async/await for network operations
- [ ] Database caching for PFEP lookups
- [ ] Incremental processing (process only changes)
- [ ] Distributed processing across machines

---

## 🙏 Acknowledgments

- **Stellantis/FIAT** - Project sponsorship and requirements
- **RTM Team** - System access and documentation
- **E-PER Team** - Parts catalog integration support

---

**Last Updated**: November 26, 2025
**Document Version**: 1.0
**Project Version**: 3.0.0

