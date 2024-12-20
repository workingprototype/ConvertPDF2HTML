import fitz  # PyMuPDF

def pdf_to_html_with_positions(pdf_path, output_html):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # HTML header
    html_content = '''
    <html>
    <head><style>
        body { margin: 0; padding: 0; }
        div { position: absolute; }
    </style></head>
    <body>
    '''

    # Initialize counters
    total_text_instances = 0

    # Loop through all the pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text_instances = page.get_text("dict")["blocks"]

        # Log: Number of blocks found
        print(f"Page {page_num + 1}: Found {len(text_instances)} blocks")

        # Loop through text blocks
        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        x, y = span["bbox"][:2]  # Get top-left corner (x, y)
                        font_size = span["size"]  # Font size
                        content = span["text"].strip()   # Text content

                        # Skip empty text spans
                        if not content:
                            continue

                        # Log the text being processed
                        print(f"Text: '{content}' at position ({x}, {y}) with font size {font_size}")

                        # Create a div for each text span with absolute positioning
                        html_content += f'<div style="left: {x}px; top: {y}px; font-size: {font_size}px;">{content}</div>\n'
                        total_text_instances += 1

    # Log: Total number of text instances found
    print(f"Total text instances found: {total_text_instances}")

    if total_text_instances == 0:
        print("No text found in the PDF. It may be an image-based PDF.")

    # HTML footer
    html_content += '</body></html>'

    # Save the HTML content to a file
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file has been saved to {output_html}")


# Example usage
pdf_path = "input.pdf"  # Your PDF file path
output_html = "output.html"  # Output HTML file
pdf_to_html_with_positions(pdf_path, output_html)
