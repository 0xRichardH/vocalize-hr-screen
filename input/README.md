# Input Folder - Document Loader Tools

This folder contains documents that can be loaded by the HR Screen Agent using the new document loader tools.

## Available Tools

The HR Screen Agent now includes three new langchain tools for loading documents:

### 1. `get_job_description` Tool
- **Description**: Load and retrieve job descriptions (JD) from the input folder
- **File Patterns**: Looks for files matching:
  - `jd.*`
  - `job_description.*`
  - `job-description.*`
  - `jobdescription.*`
  - `JD.*`
  - `Job_Description.*`
  - `Job-Description.*`
  - `JobDescription.*`

### 2. `get_cv` Tool (Optional)
- **Description**: Load and retrieve CV (Curriculum Vitae) from the input folder
- **File Patterns**: Looks for files matching:
  - `cv.*`
  - `curriculum_vitae.*`
  - `curriculum-vitae.*`
  - `curriculumvitae.*`
  - `CV.*`
  - `Curriculum_Vitae.*`
  - `Curriculum-Vitae.*`
  - `CurriculumVitae.*`

### 3. `get_resume` Tool
- **Description**: Load and retrieve resumes from the input folder
- **File Patterns**: Looks for files matching:
  - `resume.*`
  - `resume_*.*`
  - `resume-*.*`
  - `Resume.*`
  - `Resume_*.*`
  - `Resume-*.*`
  - `RESUME.*`

## Supported File Formats

The tools support various text-based file formats:
- `.txt` - Plain text files
- `.md` - Markdown files
- `.doc` - Word documents (as text)
- `.docx` - Word documents (as text)
- `.pdf` - PDF files (as text)
- Any other text-readable format

## Usage Instructions

1. **Place your documents** in this `input/` folder using the appropriate naming conventions
2. **Use the tools** in the HR Screen Agent by calling:
   - `get_job_description()` - to load job descriptions
   - `get_cv()` - to load CVs (optional)
   - `get_resume()` - to load resumes

## Example Files

This folder contains sample files to demonstrate the functionality:
- `jd.txt` - Sample job description for a Senior Software Engineer position
- `cv.txt` - Sample CV for Dr. Jane Doe, Senior Software Architect
- `resume.txt` - Sample resume for John Smith, Senior Software Engineer

## Features

- **Multiple file support**: Each tool can load multiple files matching the patterns
- **Error handling**: Graceful handling of missing files or read errors
- **Flexible naming**: Supports various naming conventions and case variations
- **Content formatting**: Files are clearly labeled with their filenames in the output

## Integration

These tools are automatically integrated into the HR Screen Agent and can be used during screening conversations to:
- Compare candidate qualifications against job requirements
- Analyze candidate experience and skills
- Provide context-aware screening questions
- Generate detailed assessment reports