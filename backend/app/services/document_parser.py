import fitz
from typing import List, Dict

class DocumentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_text(self) -> List[Dict]:
        """
        Extracts text per page and associates it with the nearest section heading from the TOC.
        Returns a list of dicts: {"text": str, "metadata": dict}
        """
        doc = None
        try:
            doc = fitz.open(self.file_path)
        except Exception as e:
            # Fallback stub conceptually placed here (e.g. Unstructured.io)
            raise RuntimeError(f"PyMuPDF failed to open {self.file_path}. Error: {e}")

        # The Table of Contents (TOC) acts as our section headings
        # Format: [level, title, page_number, ...]
        toc = doc.get_toc()
        
        current_section = "AWS IAM User Guide"
        toc_idx = 0
        
        page_texts = []
        for page_num in range(1, doc.page_count + 1):
            
            # Keep catching up the TOC index to the current page
            # (Allows tracking the deepest relevant section title for the page)
            while toc_idx < len(toc) and toc[toc_idx][2] == page_num:
                current_section = toc[toc_idx][1]
                toc_idx += 1
                
            page = doc.load_page(page_num - 1)
            # Extract plain text layout block
            text = page.get_text("text").strip()
            
            if text:
                page_texts.append({
                    "text": text,
                    "metadata": {
                        "page_number": page_num,
                        "section_title": current_section,
                        "source_file": self.file_path.split("/")[-1]
                    }
                })
                
        doc.close()
        return page_texts
