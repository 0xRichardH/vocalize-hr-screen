# Input Folder - Enhanced Document Loader Tools

This folder contains documents that can be loaded by the HR Screen Agent using the enhanced document loader tools with intelligent name-based search capabilities.

## Available Tools

The HR Screen Agent includes three enhanced langchain tools for loading documents:

### 1. `get_job_description` Tool
- **Description**: Load and retrieve job descriptions (JD) from the input folder
- **File Format**: Expects **Markdown (.md)** files
- **Search Parameters**:
  - `job_role` (Optional): Target specific job roles (e.g., "Senior Software Engineer")
  - `company_name` (Optional): Target specific companies (e.g., "Tech Innovators Inc")
- **File Patterns**: 
  - **Generic**: `jd.md`, `job_description.md`, `job-description.md`, etc.
  - **Role-specific**: `{role}.md`, `{role}_jd.md`, `jd_{role}.md`, etc.
  - **Company-specific**: `{company}_jd.md`, `jd_{company}.md`, etc.
  - **Combined**: `{company}_{role}.md`, `{company}_{role}_jd.md`, etc.

### 2. `get_cv` Tool (Optional)
- **Description**: Load and retrieve CV (Curriculum Vitae) from the input folder
- **File Format**: Expects **PDF (.pdf)** files
- **Search Parameters**:
  - `candidate_name` (Optional): Target specific candidates (e.g., "Jane Doe")
- **File Patterns**:
  - **Generic**: `cv.pdf`, `curriculum_vitae.pdf`, `curriculum-vitae.pdf`, etc.
  - **Name-specific**: `{name}.pdf`, `{name}_cv.pdf`, `cv_{name}.pdf`, etc.

### 3. `get_resume` Tool
- **Description**: Load and retrieve resumes from the input folder
- **File Format**: Expects **PDF (.pdf)** files
- **Search Parameters**:
  - `candidate_name` (Optional): Target specific candidates (e.g., "John Smith")
- **File Patterns**:
  - **Generic**: `resume.pdf`, `resume_*.pdf`, `resume-*.pdf`, etc.
  - **Name-specific**: `{name}.pdf`, `{name}_resume.pdf`, `resume_{name}.pdf`, etc.

## Enhanced Search Capabilities

### Name Normalization
All search parameters are automatically normalized for flexible file matching:
- Spaces converted to underscores: `"John Smith"` → `"john_smith"`
- Converted to lowercase for case-insensitive matching
- Hyphens normalized: `"Data-Scientist"` → `"data_scientist"`

### Flexible File Naming
The tools support various naming conventions:
- **Underscores**: `john_smith_resume.pdf`, `tech_innovators_inc_jd.md`
- **Hyphens**: `jane-doe-cv.pdf`, `senior-software-engineer.md`
- **Mixed case**: `John_Smith.pdf`, `TechInnovators_JD.md`
- **Combined formats**: `company_role_jd.md`, `candidate_name_resume.pdf`

## Usage Examples

### Job Description Search
```python
# Generic search (finds all JD files)
get_job_description()

# Search by job role
get_job_description(job_role="Senior Software Engineer")

# Search by company
get_job_description(company_name="Tech Innovators Inc")

# Search by both (most specific)
get_job_description(job_role="Senior Software Engineer", company_name="Tech Innovators Inc")
```

### Candidate Document Search
```python
# Generic search (finds all CVs)
get_cv()

# Search for specific candidate's CV
get_cv(candidate_name="Jane Doe")

# Generic resume search
get_resume()

# Search for specific candidate's resume
get_resume(candidate_name="John Smith")
```

## File Format Requirements

- **Job Descriptions**: Must be in **Markdown (.md)** format
- **CVs and Resumes**: Must be in **PDF (.pdf)** format

## PDF Reading Capabilities

The tools use advanced PDF reading libraries to extract text content:
- **Primary**: `pdfplumber` - for better text extraction and layout preservation
- **Fallback**: `PyPDF2` - for basic PDF text extraction
- **Error Handling**: Graceful handling of corrupted or unreadable PDFs

## Current Example Files

This folder contains sample files demonstrating the functionality:

### Job Descriptions (Markdown)
- `jd.md` - Generic job description for Senior Software Engineer
- `tech_innovators_inc_senior_software_engineer.md` - Company + role specific JD

### CVs (PDF)
- `cv.pdf` - Generic CV file
- `Jane_Doe.pdf` - Jane Doe's CV (name-specific)
- `jane_doe_cv.pdf` - Jane Doe's CV (name + type specific)

### Resumes (PDF)
- `resume.pdf` - Generic resume file
- `John_Smith.pdf` - John Smith's resume (name-specific)
- `john_smith_resume.pdf` - John Smith's resume (name + type specific)

## Features

- **🎯 Intelligent Search**: Target specific job roles, companies, or candidates
- **🔄 Backward Compatibility**: Generic patterns still work for existing files
- **📝 Name Normalization**: Flexible handling of various naming conventions
- **🔍 Pattern Matching**: Extensive pattern coverage for different file naming styles
- **📄 Format-specific Processing**: Optimized handling for markdown and PDF formats
- **🚫 Duplicate Elimination**: Automatically removes duplicate matches
- **⚡ Performance**: Efficient file searching with glob patterns
- **🛡️ Error Handling**: Graceful handling of missing files, read errors, and corrupted PDFs

## Integration

These enhanced tools are automatically integrated into the HR Screen Agent and enable:
- **Targeted Document Retrieval**: Find specific job descriptions by role/company
- **Candidate-Specific Analysis**: Load documents for specific candidates
- **Intelligent Matching**: Compare candidate profiles with targeted job requirements
- **Context-Aware Screening**: Provide personalized screening based on specific documents
- **Scalable Document Management**: Handle multiple job roles, companies, and candidates

## Dependencies

The document loader tools require the following Python packages:
- `PyPDF2>=3.0.0` - Basic PDF text extraction
- `pdfplumber>=0.9.0` - Advanced PDF text extraction with layout preservation

## Best Practices

### File Naming Recommendations
- **Job Descriptions**: Use format `{company}_{role}_jd.md` for best searchability
- **CVs**: Use format `{candidate_name}_cv.pdf` or `{candidate_name}.pdf`
- **Resumes**: Use format `{candidate_name}_resume.pdf` or `{candidate_name}.pdf`

### Search Strategy
1. **Start Specific**: Use role/company/candidate parameters when available
2. **Fall Back Generic**: Use generic search if specific files not found
3. **Combine Parameters**: Use both job role and company for most targeted results