from pathlib import Path
from typing import Annotated

import pdfplumber
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command


def _read_pdf_file(file_path: Path) -> str:
    """Helper function to read PDF files."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text_parts = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            return "\n".join(text_parts)
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"


def _read_text_file(file_path: Path) -> str:
    """Helper function to read text/markdown files."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return f"Error reading text file: {str(e)}"


@tool(
    "list_input_files",
    description="List all files in the input folder. Shows filename, file type, and size to help choose which files to read.",
)
def list_input_files(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """List all files in the input folder.

    This tool shows all available files in the input directory with their types and sizes,
    allowing you to see what documents are available before deciding which ones to read.

    Returns:
        A formatted list of all files in the input folder with their details.
    """

    input_dir = Path("input")

    if not input_dir.exists():
        content = "Input folder does not exist. Please create it and add documents."
        return Command(
            update={
                "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
            }
        )

    files = list(input_dir.glob("*"))

    if not files:
        content = "Input folder is empty. Please add documents to the input folder."
        return Command(
            update={
                "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
            }
        )

    # Filter out directories and sort files
    files = [f for f in files if f.is_file()]
    files.sort()

    if not files:
        content = "No files found in input folder (only directories present)."
        return Command(
            update={
                "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
            }
        )

    # Format file list
    file_list = ["Available files in input folder:\n"]

    for file_path in files:
        # Get file size
        size_bytes = file_path.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

        # Get file type
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            file_type = "PDF"
        elif suffix in [".md", ".markdown"]:
            file_type = "Markdown"
        elif suffix in [".txt", ".text"]:
            file_type = "Text"
        else:
            file_type = f"{suffix[1:].upper() if suffix else 'Unknown'}"

        file_list.append(f"• {file_path.name} ({file_type}, {size_str})")

    content = "\n".join(file_list)

    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "read_input_file",
    description="Read the content of a specific file from the input folder. Supports PDF, Markdown (.md), and Text (.txt) files.",
)
def read_input_file(
    filename: Annotated[
        str, "The name of the file to read (e.g., 'resume.pdf', 'jd.md', 'notes.txt')"
    ],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Read the content of a specific file from the input folder.

    This tool can read various file formats:
    - PDF files (.pdf) - Extracts text content from PDF documents
    - Markdown files (.md, .markdown) - Reads markdown content
    - Text files (.txt, .text) - Reads plain text content

    Args:
        filename: The name of the file to read from the input folder

    Returns:
        The content of the specified file.
    """

    input_dir = Path("input")
    file_path = input_dir / filename

    # Check if input folder exists
    if not input_dir.exists():
        content = "Input folder does not exist. Please create it and add documents."
        return Command(
            update={
                "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
            }
        )

    # Check if file exists
    if not file_path.exists():
        content = f"File '{filename}' not found in input folder. Use list_input_files to see available files."
        return Command(
            update={
                "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
            }
        )

    # Check if it's actually a file (not a directory)
    if not file_path.is_file():
        content = (
            f"'{filename}' is not a file. Use list_input_files to see available files."
        )
        return Command(
            update={
                "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
            }
        )

    # Determine file type and read accordingly
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        file_content = _read_pdf_file(file_path)
        file_type = "PDF"
    elif suffix in [".md", ".markdown"]:
        file_content = _read_text_file(file_path)
        file_type = "Markdown"
    elif suffix in [".txt", ".text"]:
        file_content = _read_text_file(file_path)
        file_type = "Text"
    else:
        # Try to read as text file for other extensions
        file_content = _read_text_file(file_path)
        file_type = f"{suffix[1:].upper() if suffix else 'Unknown'}"

    # Format the response
    content = f"=== {filename} ({file_type}) ===\n{file_content}"

    return Command(
        update={
            "messages": [ToolMessage(content, tool_call_id=tool_call_id)],
        }
    )
