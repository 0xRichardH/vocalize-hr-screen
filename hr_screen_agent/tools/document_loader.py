import os
from pathlib import Path
from typing import Annotated, List, Optional

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command


def _read_document_files(folder_path: str, file_patterns: List[str]) -> str:
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
    description="Load and retrieve the job description (JD) from the input folder. Looks for files with patterns like 'jd.*', 'job_description.*', 'job-description.*', etc.",
)
def get_job_description(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Load and retrieve the job description from the input folder.
    
    This tool searches for job description files in the 'input' folder using common naming patterns
    like 'jd.*', 'job_description.*', 'job-description.*', etc. It supports various file formats
    including .txt, .md, .pdf (as text), .docx (as text), etc.
    
    Returns:
        The content of the job description file(s) found in the input folder.
    """
    
    # Define patterns for job description files
    jd_patterns = [
        "jd.*",
        "job_description.*", 
        "job-description.*",
        "jobdescription.*",
        "JD.*",
        "Job_Description.*",
        "Job-Description.*",
        "JobDescription.*"
    ]
    
    content = _read_document_files("input", jd_patterns)
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "get_cv",
    description="Load and retrieve the CV (Curriculum Vitae) from the input folder. This is optional. Looks for files with patterns like 'cv.*', 'curriculum_vitae.*', etc.",
)
def get_cv(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Load and retrieve the CV (Curriculum Vitae) from the input folder.
    
    This tool searches for CV files in the 'input' folder using common naming patterns
    like 'cv.*', 'curriculum_vitae.*', 'curriculum-vitae.*', etc. It supports various file formats
    including .txt, .md, .pdf (as text), .docx (as text), etc.
    
    This tool is optional and may not find any files if CVs are not provided.
    
    Returns:
        The content of the CV file(s) found in the input folder, or a message if none found.
    """
    
    # Define patterns for CV files
    cv_patterns = [
        "cv.*",
        "curriculum_vitae.*",
        "curriculum-vitae.*",
        "curriculumvitae.*",
        "CV.*",
        "Curriculum_Vitae.*",
        "Curriculum-Vitae.*",
        "CurriculumVitae.*"
    ]
    
    content = _read_document_files("input", cv_patterns)
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "get_resume",
    description="Load and retrieve the Resume from the input folder. Looks for files with patterns like 'resume.*', 'resume_*.*', etc.",
)
def get_resume(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Load and retrieve the Resume from the input folder.
    
    This tool searches for resume files in the 'input' folder using common naming patterns
    like 'resume.*', 'resume_*.*', etc. It supports various file formats
    including .txt, .md, .pdf (as text), .docx (as text), etc.
    
    Returns:
        The content of the resume file(s) found in the input folder.
    """
    
    # Define patterns for resume files
    resume_patterns = [
        "resume.*",
        "resume_*.*",
        "resume-*.*",
        "Resume.*",
        "Resume_*.*",
        "Resume-*.*",
        "RESUME.*"
    ]
    
    content = _read_document_files("input", resume_patterns)
    
    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )