import fitz
from PIL import Image

# Uses page and bounding box information from tables_info object returned by Textract
# To extract images of tables from original pdf

class image_handler_cls():
    def __init__(self, file_path, tables_info):
        self.pdf_document = fitz.open(file_path)
        self.tables_info = tables_info
        self.images = []
    
    def populate_images(self, page, bounding_box, target_dpi=900):
        width = page.rect.width
        height = page.rect.height

        # Calculate the absolute coordinates for the bounding box
        left = bounding_box['Left'] * width
        top = bounding_box['Top'] * height
        right = (bounding_box['Left'] + bounding_box['Width']) * width
        bottom = (bounding_box['Top'] + bounding_box['Height']) * height

        # Determine matrix for target DPI
        source_dpi = 72  # Default for PDFs
        scale = target_dpi / source_dpi
        mat = fitz.Matrix(scale, scale)

        # Get the pixmap using the matrix
        pix = page.get_pixmap(matrix=mat, clip=fitz.Rect(left, top, right, bottom))
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        self.images.append(img)
    
    def get_images(self):
        for table_info in self.tables_info:
            page_number = table_info['Page'] - 1  # 0-indexed
            bounding_box = table_info['BoundingBox']
            page = self.pdf_document[page_number]
            self.populate_images(page, bounding_box)
            
    def save_images(self):
        for i, table_image in enumerate(self.images):  # Just saving first 3 for demonstration
            output_path = f"table_{i + 1}.png"
            table_image.save(output_path)
