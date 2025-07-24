import os
from pathlib import Path
from typing import Annotated, List, Optional

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command

# Try to import PDF reading capability
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False


def _read_pdf_file(file_path: Path) -> str:
    """Helper function to read PDF files."""
    if not PDF_AVAILABLE:
        return "Error: PDF reading libraries not available. Please install PyPDF2 or pdfplumber."
    
    try:
        # Try pdfplumber first (better text extraction)
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text_parts = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                return "\n".join(text_parts)
        except ImportError:
            pass
        
        # Fallback to PyPDF2
        import PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_parts = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            return "\n".join(text_parts)
            
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"


def _read_markdown_file(file_path: Path) -> str:
    """Helper function to read markdown files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        return f"Error reading markdown file: {str(e)}"


def _read_document_files(folder_path: str, file_patterns: List[str], file_type: str = "text") -> str:
    """Helper function to read document files from a folder based on patterns."""
    input_dir = Path(folder_path)
    
    if not input_dir.exists():
        return f"Input folder '{folder_path}' does not exist. Please create it and add the required documents."
    
    files_found = []
    content_parts = []
    
    # Look for files matching the patterns
    for pattern in file_patterns:
        matching_files = list(input_dir.glob(pattern))
        files_found.extend(matching_files)
    
    if not files_found:
        return f"No files found matching patterns {file_patterns} in '{folder_path}'. Please add the required documents."
    
    # Read content from all matching files
    for file_path in files_found:
        try:
            if file_type == "pdf":
                content = _read_pdf_file(file_path)
            elif file_type == "markdown":
                content = _read_markdown_file(file_path)
            else:
                # Default text reading
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
            
            if content:
                content_parts.append(f"=== {file_path.name} ===\n{content}")
        except Exception as e:
            content_parts.append(f"=== {file_path.name} ===\nError reading file: {str(e)}")
    
    if not content_parts:
        return f"Found {len(files_found)} file(s) but all were empty or unreadable."
    
    return "\n\n".join(content_parts)


@tool(
    "get_job_description",
    description="Load and retrieve the job description (JD) from the input folder. Expects markdown (.md) files with patterns like 'jd.md', 'job_description.md', 'job-description.md', etc.",
)
def get_job_description(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Load and retrieve the job description from the input folder.
    
    This tool searches for job description files in the 'input' folder using common naming patterns
    for markdown files like 'jd.md', 'job_description.md', 'job-description.md', etc.
    
    Returns:
        The content of the job description markdown file(s) found in the input folder.
    """
    
    # Define patterns for job description markdown files
    jd_patterns = [
        "jd.md",
        "job_description.md", 
        "job-description.md",
        "jobdescription.md",
        "JD.md",
        "Job_Description.md",
        "Job-Description.md",
        "JobDescription.md"
    ]
    
    content = _read_document_files("input", jd_patterns, "markdown")
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "get_cv",
    description="Load and retrieve the CV (Curriculum Vitae) from the input folder. This is optional. Expects PDF files with patterns like 'cv.pdf', 'curriculum_vitae.pdf', etc.",
)
def get_cv(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Load and retrieve the CV (Curriculum Vitae) from the input folder.
    
    This tool searches for CV files in the 'input' folder using common naming patterns
    for PDF files like 'cv.pdf', 'curriculum_vitae.pdf', 'curriculum-vitae.pdf', etc.
    
    This tool is optional and may not find any files if CVs are not provided.
    
    Returns:
        The content of the CV PDF file(s) found in the input folder, or a message if none found.
    """
    
    # Define patterns for CV PDF files
    cv_patterns = [
        "cv.pdf",
        "curriculum_vitae.pdf",
        "curriculum-vitae.pdf",
        "curriculumvitae.pdf",
        "CV.pdf",
        "Curriculum_Vitae.pdf",
        "Curriculum-Vitae.pdf",
        "CurriculumVitae.pdf"
    ]
    
    content = _read_document_files("input", cv_patterns, "pdf")
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "get_resume",
    description="Load and retrieve the Resume from the input folder. Expects PDF files with patterns like 'resume.pdf', 'resume_*.pdf', etc.",
)
def get_resume(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Load and retrieve the Resume from the input folder.
    
    This tool searches for resume files in the 'input' folder using common naming patterns
    for PDF files like 'resume.pdf', 'resume_*.pdf', etc.
    
    Returns:
        The content of the resume PDF file(s) found in the input folder.
    """
    
    # Define patterns for resume PDF files
    resume_patterns = [
        "resume.pdf",
        "resume_*.pdf",
        "resume-*.pdf",
        "Resume.pdf",
        "Resume_*.pdf",
        "Resume-*.pdf",
        "RESUME.pdf"
    ]
    
    content = _read_document_files("input", resume_patterns, "pdf")
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )