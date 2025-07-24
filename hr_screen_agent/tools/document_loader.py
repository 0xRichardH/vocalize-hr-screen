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


def _normalize_name(name: str) -> str:
    """Normalize a name for file matching by removing spaces, converting to lowercase."""
    return name.lower().replace(" ", "_").replace("-", "_")


def _create_job_patterns(job_role: Optional[str] = None, company_name: Optional[str] = None) -> List[str]:
    """Create file patterns for job descriptions based on job role and company name."""
    patterns = []
    
    # Base patterns (original functionality)
    base_patterns = [
        "jd.md",
        "job_description.md", 
        "job-description.md",
        "jobdescription.md",
        "JD.md",
        "Job_Description.md",
        "Job-Description.md",
        "JobDescription.md"
    ]
    patterns.extend(base_patterns)
    
    # Add specific patterns based on parameters
    if job_role:
        normalized_role = _normalize_name(job_role)
        role_patterns = [
            f"{normalized_role}.md",
            f"{normalized_role}_jd.md",
            f"{normalized_role}-jd.md",
            f"jd_{normalized_role}.md",
            f"jd-{normalized_role}.md",
            f"job_description_{normalized_role}.md",
            f"job-description-{normalized_role}.md",
        ]
        patterns.extend(role_patterns)
    
    if company_name:
        normalized_company = _normalize_name(company_name)
        company_patterns = [
            f"{normalized_company}_jd.md",
            f"{normalized_company}-jd.md",
            f"jd_{normalized_company}.md",
            f"jd-{normalized_company}.md",
        ]
        patterns.extend(company_patterns)
    
    if job_role and company_name:
        normalized_role = _normalize_name(job_role)
        normalized_company = _normalize_name(company_name)
        combined_patterns = [
            f"{normalized_company}_{normalized_role}.md",
            f"{normalized_company}-{normalized_role}.md",
            f"{normalized_role}_{normalized_company}.md",
            f"{normalized_role}-{normalized_company}.md",
            f"{normalized_company}_{normalized_role}_jd.md",
            f"{normalized_company}-{normalized_role}-jd.md",
        ]
        patterns.extend(combined_patterns)
    
    return patterns


def _create_candidate_patterns(candidate_name: Optional[str] = None, file_type: str = "resume") -> List[str]:
    """Create file patterns for CV/resume based on candidate name."""
    patterns = []
    
    # Base patterns (original functionality)
    if file_type == "cv":
        base_patterns = [
            "cv.pdf",
            "curriculum_vitae.pdf",
            "curriculum-vitae.pdf",
            "curriculumvitae.pdf",
            "CV.pdf",
            "Curriculum_Vitae.pdf",
            "Curriculum-Vitae.pdf",
            "CurriculumVitae.pdf"
        ]
    else:  # resume
        base_patterns = [
            "resume.pdf",
            "resume_*.pdf",
            "resume-*.pdf",
            "Resume.pdf",
            "Resume_*.pdf",
            "Resume-*.pdf",
            "RESUME.pdf"
        ]
    patterns.extend(base_patterns)
    
    # Add specific patterns based on candidate name
    if candidate_name:
        normalized_name = _normalize_name(candidate_name)
        name_patterns = [
            f"{normalized_name}.pdf",
            f"{normalized_name}_{file_type}.pdf",
            f"{normalized_name}-{file_type}.pdf",
            f"{file_type}_{normalized_name}.pdf",
            f"{file_type}-{normalized_name}.pdf",
        ]
        patterns.extend(name_patterns)
        
        # Also try with original case and spaces replaced by underscores/hyphens
        original_underscore = candidate_name.replace(" ", "_")
        original_hyphen = candidate_name.replace(" ", "-")
        if original_underscore != normalized_name:
            patterns.extend([
                f"{original_underscore}.pdf",
                f"{original_underscore}_{file_type}.pdf",
                f"{original_underscore}-{file_type}.pdf",
            ])
        if original_hyphen != normalized_name:
            patterns.extend([
                f"{original_hyphen}.pdf",
                f"{original_hyphen}_{file_type}.pdf",
                f"{original_hyphen}-{file_type}.pdf",
            ])
    
    return patterns


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
    
    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for file_path in files_found:
        if file_path not in seen:
            seen.add(file_path)
            unique_files.append(file_path)
    
    if not unique_files:
        return f"No files found matching patterns {file_patterns[:5]}{'...' if len(file_patterns) > 5 else ''} in '{folder_path}'. Please add the required documents."
    
    # Read content from all matching files
    for file_path in unique_files:
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
        return f"Found {len(unique_files)} file(s) but all were empty or unreadable."
    
    return "\n\n".join(content_parts)


@tool(
    "get_job_description",
    description="Load and retrieve the job description (JD) from the input folder. Expects markdown (.md) files. Can search by job role and/or company name for more targeted results.",
)
def get_job_description(
    job_role: Annotated[Optional[str], "The job role/position title to search for (e.g., 'Senior Software Engineer', 'Data Scientist'). Optional."] = None,
    company_name: Annotated[Optional[str], "The company name to search for (e.g., 'Tech Innovators Inc', 'Google'). Optional."] = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
) -> Command:
    """Load and retrieve the job description from the input folder.
    
    This tool searches for job description files in the 'input' folder using common naming patterns
    for markdown files. It can search generically or target specific job roles and companies.
    
    Args:
        job_role: Optional job role/position title to search for more targeted results
        company_name: Optional company name to search for more targeted results
    
    Returns:
        The content of the job description markdown file(s) found in the input folder.
    """
    
    # Create patterns based on provided parameters
    jd_patterns = _create_job_patterns(job_role, company_name)
    
    content = _read_document_files("input", jd_patterns, "markdown")
    
    # Add context about the search parameters
    search_info = []
    if job_role:
        search_info.append(f"Job Role: {job_role}")
    if company_name:
        search_info.append(f"Company: {company_name}")
    
    if search_info:
        search_context = f"Search Parameters - {', '.join(search_info)}\n\n"
        content = search_context + content
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "get_cv",
    description="Load and retrieve the CV (Curriculum Vitae) from the input folder. This is optional. Expects PDF files. Can search by candidate name for more targeted results.",
)
def get_cv(
    candidate_name: Annotated[Optional[str], "The candidate's name to search for (e.g., 'John Smith', 'Jane Doe'). Optional."] = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
) -> Command:
    """Load and retrieve the CV (Curriculum Vitae) from the input folder.
    
    This tool searches for CV files in the 'input' folder using common naming patterns
    for PDF files. It can search generically or target a specific candidate's CV.
    
    This tool is optional and may not find any files if CVs are not provided.
    
    Args:
        candidate_name: Optional candidate name to search for more targeted results
    
    Returns:
        The content of the CV PDF file(s) found in the input folder, or a message if none found.
    """
    
    # Create patterns based on candidate name
    cv_patterns = _create_candidate_patterns(candidate_name, "cv")
    
    content = _read_document_files("input", cv_patterns, "pdf")
    
    # Add context about the search parameters
    if candidate_name:
        search_context = f"Search Parameters - Candidate: {candidate_name}\n\n"
        content = search_context + content
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "get_resume",
    description="Load and retrieve the Resume from the input folder. Expects PDF files. Can search by candidate name for more targeted results.",
)
def get_resume(
    candidate_name: Annotated[Optional[str], "The candidate's name to search for (e.g., 'John Smith', 'Jane Doe'). Optional."] = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
) -> Command:
    """Load and retrieve the Resume from the input folder.
    
    This tool searches for resume files in the 'input' folder using common naming patterns
    for PDF files. It can search generically or target a specific candidate's resume.
    
    Args:
        candidate_name: Optional candidate name to search for more targeted results
    
    Returns:
        The content of the resume PDF file(s) found in the input folder.
    """
    
    # Create patterns based on candidate name
    resume_patterns = _create_candidate_patterns(candidate_name, "resume")
    
    content = _read_document_files("input", resume_patterns, "pdf")
    
    # Add context about the search parameters
    if candidate_name:
        search_context = f"Search Parameters - Candidate: {candidate_name}\n\n"
        content = search_context + content
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )