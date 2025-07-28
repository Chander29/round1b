import fitz  # PyMuPDF
from collections import Counter

class PDFProcessor:
    def __init__(self, file_path):
        self.doc = fitz.open(file_path)
        self.body_size, self.heading_styles = self._analyze_font_styles()

    def _analyze_font_styles(self):
        styles = Counter()
        for page in self.doc:
            blocks = page.get_text("dict", flags=4)["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            size = round(span["size"])
                            styles[size] += len(span["text"])
        if not styles:
            return 12, set()
        body_size = max(styles, key=styles.get)
        heading_styles = {s for s in styles if s > body_size * 1.1}
        return body_size, heading_styles

    def get_sections(self):
        sections = []
        current_text_blocks = []
        current_heading = None
        current_page = 1
        headings_found = False

        for page_num, page in enumerate(self.doc):
            blocks = page.get_text("dict", flags=4).get("blocks", [])
            for block in blocks:
                if "lines" in block and block["lines"]:
                    block_text = " ".join(
                        "".join(span["text"] for span in line["spans"]).strip()
                        for line in block["lines"] if line["spans"]
                    ).strip()

                    if not block_text:
                        continue

                    font_sizes = [
                        round(span["size"])
                        for line in block["lines"]
                        for span in line["spans"]
                    ]
                    avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 0

                    is_heading = (
                        round(avg_font_size) in self.heading_styles and
                        len(block_text) < 100 and
                        block_text != current_heading
                    )

                    if is_heading:
                        headings_found = True
                        if current_text_blocks and current_heading:
                            sections.append({
                                "title": current_heading,
                                "text": " ".join(current_text_blocks),
                                "page": current_page
                            })
                        current_heading = block_text
                        current_page = page_num + 1
                        current_text_blocks = []
                    else:
                        if current_heading:
                            current_text_blocks.append(block_text)

        # Add the last collected section
        if current_text_blocks and current_heading:
            sections.append({
                "title": current_heading,
                "text": " ".join(current_text_blocks),
                "page": current_page
            })

        # Fallback only if no headings detected
        if not headings_found and not sections:
            full_text = " ".join([p.get_text() for p in self.doc])
            sections.append({
                "title": "Full Document",
                "text": full_text,
                "page": 1
            })

        self.doc.close()
        return sections
