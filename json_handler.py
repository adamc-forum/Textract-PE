import json

# Retrieves tables from analyzeDocResponse JSON object returned by Textract

class json_handler_cls:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tables_info = []
        self.set_text()
    
    def set_text(self):
        with open(self.file_path, "r") as file:
            self.text = json.load(file)
    
    def get_tables(self):
        for block in self.text.get("Blocks", []):
            if block.get("BlockType") == "TABLE":
                self.tables_info.append({
                    "TableId": block.get("Id"),
                    "Page": block.get("Page"),
                    "BoundingBox": block.get("Geometry", {}).get("BoundingBox", {})
            })
    
    
    