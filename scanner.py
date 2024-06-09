import pytesseract
import cv2
import re
import os

class DocumentScanner:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def search_word(self, text, words):
        text = text.lower()
        
        for word in words:
            if word in text:
                return word
        return None      

    def recognize_card_type(self, image_path):
        img = cv2.imread(image_path)
        
        # Convert image to JPG format if it's PNG (pytesseract works only with JPG)
        if image_path.lower().endswith('.png'):
            new_path = os.path.splitext(image_path)[0] + '.jpg'
            cv2.imwrite(new_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        
        # Image to text using pytesseract
        options = "--psm 6"
        data = pytesseract.image_to_string(img, lang='eng', config=options)
        
        # Delete created JPG file
        if image_path.lower().endswith('.png'):
            os.remove(new_path)
        
        # Check what type of document has been passed
        words = ['bicycle', 'library']
        found_word = self.search_word(data, words)
        print(found_word, '\n')
        
        print(data)
        
        # Scan the image accordingly to the document type
        if found_word == "bicycle":
            name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
            id_number_pattern = r'ID Number:\s*(\d+)'
            phone_number_pattern = r'Phone Number:\s*(.*)'
            address_pattern = r'Address:\s*(.*)'
            
            # Initialize variables
            name = None
            id_number = None
            phone_number = None
            address = None

            # Search for patterns line by line
            for line in data.split('\n'):
                line = line.strip()
                if not name and re.match(name_pattern, line):
                    name = line
                if not id_number and re.search(id_number_pattern, line):
                    id_number = re.search(id_number_pattern, line).group(1)
                if not phone_number and re.search(phone_number_pattern, line):
                    phone_number = re.search(phone_number_pattern, line).group(1)
                if not address and re.search(address_pattern, line):
                    address = re.search(address_pattern, line).group(1)

            # Print the extracted values
            print(f"Name: {name}")
            print(f"ID Number: {id_number}")
            print(f"Place of Birth: {phone_number}")
            print(f"Date of Birth: {address}")
                
        elif found_word == 'library':
            name_pattern = r'Name\s+([A-Z][a-z]+\s[A-Z][a-z]+)'
            id_number_pattern = r'Student\s*ID\s*(\d+)'
            class_pattern = r'Class\s*(.*)'
            phone_number_pattern = r'Phone\s*(.*)'
            address_pattern = r'Address\s*(.*)'        
            
            # Initialize variables
            name = None
            id_number = None
            class_type = None
            phone_number = None
            address = None

            # Search for patterns line by line
            for line in data.split('\n'):
                line = line.strip()
                if not name and re.search(name_pattern, line):
                    name = re.search(name_pattern, line).group(1)
                if not id_number and re.search(id_number_pattern, line):
                    id_number = re.search(id_number_pattern, line).group(1)
                if not class_type and re.search(class_pattern, line):
                    class_type = re.search(class_pattern, line).group(1)
                if not phone_number and re.search(phone_number_pattern, line):
                    phone_number = re.search(phone_number_pattern, line).group(1)
                if not address and re.search(address_pattern, line):
                    address = re.search(address_pattern, line).group(1)

            # Print the extracted values
            print(f"Name: {name}")
            print(f"ID Number: {id_number}")
            print(f"Class: {class_type}")
            print(f"Phone Number: {phone_number}")
            print(f"Address: {address}")
            
        else:
            print("Unsupported type of file.")

DocumentScanner().recognize_card_type("images/person_9/bicycle_card.png")
