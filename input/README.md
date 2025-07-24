# Input Folder - Simple Document Tools

This folder contains documents that can be accessed by the HR Screen Agent using two simple and intuitive document tools.

## Available Tools

The HR Screen Agent includes two straightforward langchain tools for document access:

### 1. `list_input_files` Tool
- **Description**: Lists all files in the input folder with details
- **Parameters**: None
- **Returns**: A formatted list showing:
  - File names
  - File types (PDF, Markdown, Text, etc.)
  - File sizes
- **Purpose**: Lets the LLM see what documents are available before deciding which to read

### 2. `read_input_file` Tool
- **Description**: Reads the content of a specific file by name
- **Parameters**: 
  - `filename`: The exact name of the file to read (e.g., "resume.pdf", "jd.md")
- **Returns**: The full content of the specified file
- **Purpose**: Allows the LLM to read any specific document it chooses

## Supported File Formats

The tools automatically handle different file types:
- **📄 PDF files (.pdf)**: Extracts text content using advanced PDF libraries
- **📝 Markdown files (.md, .markdown)**: Reads markdown content with formatting
- **📃 Text files (.txt, .text)**: Reads plain text content
- **🔧 Other formats**: Attempts to read as text files

## How It Works

The approach is intentionally simple and LLM-friendly:

1. **🔍 Discovery**: LLM calls `list_input_files()` to see all available documents
2. **🎯 Selection**: LLM decides which files are relevant based on the context
3. **📖 Reading**: LLM calls `read_input_file(filename)` for each file it wants to read

## Example Usage

```python
# First, see what files are available
list_input_files()
# Returns: List of all files with types and sizes

# Then read specific files as needed
read_input_file("jd.md")           # Read job description
read_input_file("resume.pdf")      # Read candidate resume  
read_input_file("notes.txt")       # Read any other document
```

## Current Example Files

This folder contains various sample documents:

### Job Descriptions
- `jd.md` - Generic job description (Markdown)
- `tech_innovators_inc_senior_software_engineer.md` - Specific company JD (Markdown)

### Candidate Documents  
- `resume.pdf` - Generic resume (PDF)
- `cv.pdf` - Generic CV (PDF)
- `John_Smith.pdf` - John Smith's resume (PDF)
- `john_smith_resume.pdf` - John Smith's resume (PDF)
- `Jane_Doe.pdf` - Jane Doe's CV (PDF)
- `jane_doe_cv.pdf` - Jane Doe's CV (PDF)

### Documentation
- `README.md` - This documentation file (Markdown)

## Benefits of This Approach

### 🎯 **LLM-Friendly**
- Simple, intuitive interface
- LLM makes intelligent decisions about which files to read
- No complex pattern matching or parameter guessing

### 🔧 **Flexible**
- Works with any file naming convention
- Supports multiple file formats automatically
- Easy to add new document types

### ⚡ **Efficient**
- Only reads files that are actually needed
- LLM can see file sizes before reading
- No unnecessary file operations

### 🛡️ **Robust**
- Clear error messages for missing files
- Graceful handling of different file formats
- Automatic file type detection

## File Organization Tips

While the tools work with any file names, here are some suggestions:

### Job Descriptions
- Use descriptive names: `senior_engineer_jd.md`, `data_scientist_role.md`
- Include company names: `google_swe_jd.md`, `startup_fullstack.md`

### Candidate Documents
- Include candidate names: `john_smith_resume.pdf`, `jane_doe_cv.pdf`
- Be descriptive: `experienced_backend_engineer.pdf`, `senior_architect_cv.pdf`

### General Documents
- Use clear names: `interview_notes.txt`, `requirements.md`, `feedback.txt`

## Integration with HR Screen Agent

The HR Screen Agent can now:

1. **📋 Inventory Documents**: See all available files at a glance
2. **🎯 Targeted Reading**: Read only relevant documents based on context
3. **🔄 Dynamic Workflow**: Adapt reading strategy based on available files
4. **💡 Intelligent Matching**: Compare job requirements with candidate profiles
5. **📊 Comprehensive Analysis**: Access all relevant documents for thorough screening

## Technical Details

### PDF Processing
- **Primary**: `pdfplumber` for superior text extraction
- **Fallback**: `PyPDF2` for basic PDF reading
- **Error Handling**: Graceful handling of corrupted or protected PDFs

### Text Processing
- **Encoding**: UTF-8 support for international characters
- **Formats**: Automatic detection of markdown, text, and other formats
- **Preservation**: Maintains original formatting and structure

### Dependencies
- `PyPDF2>=3.0.0` - Basic PDF text extraction
- `pdfplumber>=0.9.0` - Advanced PDF text extraction

## Philosophy

This simplified approach follows the principle of **"Let the LLM decide"**:

- ✅ **Simple tools** that do one thing well
- ✅ **Clear interfaces** that are easy to understand
- ✅ **Flexible usage** that adapts to different scenarios
- ✅ **LLM intelligence** to make the right choices
- ❌ **No complex parameters** or pattern matching
- ❌ **No rigid assumptions** about file naming
- ❌ **No over-engineering** that limits flexibility

The result is a clean, intuitive system that scales well and is easy to maintain! 🚀