import pytesseract
import cv2
import re
import os

class DocumentScanner:
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'

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
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Light blur
        blurred = cv2.GaussianBlur(gray, (3,3), 0)

        # Preprocessed image to text using pytesseract
        options = "--psm 6"
        data = pytesseract.image_to_string(blurred, lang='eng', config=options)
        
        # Delete created JPG file
        try:
            if image_path.lower().endswith('.png'):
                os.remove(new_path)
        except FileNotFoundError:
            print(f"File {new_path} not found for deletion.")
        except PermissionError:
            print(f"Permission denied: cannot delete {new_path}.")
        except Exception as e:
            print(f"Error deleting file {new_path}: {e}")
        
        # Check what type of document has been passed
        words = ['bicycle', 'library']
        found_word = self.search_word(data, words)
        print(found_word, '\n')
        
        # Scan the image accordingly to the document type
        if found_word == "bicycle":
            name_pattern = r'^.*?\b([A-Z][a-z]+)\s([A-Z][a-z]+)\b'
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
                if not name:
                    name_match = re.search(name_pattern, line)
                    if name_match:
                        # Use groups to extract first name and last name
                        first_name = name_match.group(1)
                        last_name = name_match.group(2)
                        name = f"{first_name} {last_name}"
                if not id_number and re.search(id_number_pattern, line):
                    id_number = re.search(id_number_pattern, line).group(1)
                if not phone_number and re.search(phone_number_pattern, line):
                    phone_number = re.search(phone_number_pattern, line).group(1)
                if not address and re.search(address_pattern, line):
                    address = re.search(address_pattern, line).group(1)

            # Print the extracted values and return them
            # print(f"Name: {name}")
            # print(f"ID Number: {id_number}")
            # print(f"Place of Birth: {phone_number}")
            # print(f"Date of Birth: {address}")
            return (found_word, name, id_number, phone_number, address)
                
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

            # Print the extracted values and return them
            # print(f"Name: {name}")
            # print(f"ID Number: {id_number}")
            # print(f"Class: {class_type}")
            # print(f"Phone Number: {phone_number}")
            # print(f"Address: {address}")
            return (found_word, name, id_number, class_type, phone_number, address)
            
        else:
            print("Unsupported type of file.")