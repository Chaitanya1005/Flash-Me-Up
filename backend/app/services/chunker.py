import re

def chunk_text(text: str, max_chunk_length: int = 1500) -> list[str]:
    """
    Splits text into meaningful chunks, preferably by paragraph or sentences,
    to avoid cutting off mid-sentence.
    """
    # Split by double newline (paragraphs)
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        if len(current_chunk) + len(p) < max_chunk_length:
            current_chunk += p + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks
