# Input Folder - Document Loader Tools

This folder contains documents that can be loaded by the HR Screen Agent using the new document loader tools.

## Available Tools

The HR Screen Agent now includes three new langchain tools for loading documents:

### 1. `get_job_description` Tool
- **Description**: Load and retrieve job descriptions (JD) from the input folder
- **File Format**: Expects **Markdown (.md)** files
- **File Patterns**: Looks for files matching:
  - `jd.md`
  - `job_description.md`
  - `job-description.md`
  - `jobdescription.md`
  - `JD.md`
  - `Job_Description.md`
  - `Job-Description.md`
  - `JobDescription.md`

### 2. `get_cv` Tool (Optional)
- **Description**: Load and retrieve CV (Curriculum Vitae) from the input folder
- **File Format**: Expects **PDF (.pdf)** files
- **File Patterns**: Looks for files matching:
  - `cv.pdf`
  - `curriculum_vitae.pdf`
  - `curriculum-vitae.pdf`
  - `curriculumvitae.pdf`
  - `CV.pdf`
  - `Curriculum_Vitae.pdf`
  - `Curriculum-Vitae.pdf`
  - `CurriculumVitae.pdf`

### 3. `get_resume` Tool
- **Description**: Load and retrieve resumes from the input folder
- **File Format**: Expects **PDF (.pdf)** files
- **File Patterns**: Looks for files matching:
  - `resume.pdf`
  - `resume_*.pdf`
  - `resume-*.pdf`
  - `Resume.pdf`
  - `Resume_*.pdf`
  - `Resume-*.pdf`
  - `RESUME.pdf`

## File Format Requirements

- **Job Descriptions**: Must be in **Markdown (.md)** format
- **CVs and Resumes**: Must be in **PDF (.pdf)** format

## PDF Reading Capabilities

The tools use advanced PDF reading libraries to extract text content:
- **Primary**: `pdfplumber` - for better text extraction and layout preservation
- **Fallback**: `PyPDF2` - for basic PDF text extraction
- **Error Handling**: Graceful handling of corrupted or unreadable PDFs

## Usage Instructions

1. **Place your documents** in this `input/` folder using the appropriate naming conventions and file formats
2. **Use the tools** in the HR Screen Agent by calling:
   - `get_job_description()` - to load job descriptions (markdown files)
   - `get_cv()` - to load CVs (PDF files, optional)
   - `get_resume()` - to load resumes (PDF files)

## Example Files

This folder contains sample files to demonstrate the functionality:
- `jd.md` - Sample job description for a Senior Software Engineer position (Markdown format)
- `cv.pdf` - Sample CV for Dr. Jane Doe, Senior Software Architect (PDF format)
- `resume.pdf` - Sample resume for John Smith, Senior Software Engineer (PDF format)

## Features

- **Format-specific processing**: Optimized handling for markdown and PDF formats
- **Multiple file support**: Each tool can load multiple files matching the patterns
- **Error handling**: Graceful handling of missing files, read errors, and corrupted PDFs
- **Flexible naming**: Supports various naming conventions and case variations
- **Content formatting**: Files are clearly labeled with their filenames in the output
- **Advanced PDF extraction**: Uses multiple PDF libraries for reliable text extraction

## Integration

These tools are automatically integrated into the HR Screen Agent and can be used during screening conversations to:
- Compare candidate qualifications against job requirements
- Analyze candidate experience and skills from PDF documents
- Provide context-aware screening questions based on markdown job descriptions
- Generate detailed assessment reports comparing PDF resumes/CVs with markdown job requirements

## Dependencies

The document loader tools require the following Python packages:
- `PyPDF2>=3.0.0` - Basic PDF text extraction
- `pdfplumber>=0.9.0` - Advanced PDF text extraction with layout preservation