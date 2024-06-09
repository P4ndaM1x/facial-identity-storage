import pytesseract
import cv2
import re
import os

def search_word(text, words):
    text = text.lower()
    
    for word in words:
        if word in text:
            return word
    return None      

def recognize_card_type(image_path):
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
    found_word = search_word(data, words)
    print(found_word, '\n')
    
    print(data)
    
    # Scan the image accordingly to the document type
    if found_word == "bicycle":
        name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b' #nie dziala
        id_number_pattern = r'ID number:\s*(\d+)'
        place_of_birth_pattern = r'Place of birth:\s*([A-Za-z\s,]+)'
        date_of_birth_pattern = r'Date of birth:\s*([\d/]+)'
        card_number_pattern = r'Card no\.\s*(\d+)'
        
        # Initialize variables
        name = None
        id_number = None
        place_of_birth = None
        date_of_birth = None
        card_number = None

        # Search for patterns line by line
        for line in data.split('\n'):
            line = line.strip()
            if not name and re.match(name_pattern, line):
                name = line
            if not id_number and re.search(id_number_pattern, line):
                id_number = re.search(id_number_pattern, line).group(1)
            if not place_of_birth and re.search(place_of_birth_pattern, line):
                place_of_birth = re.search(place_of_birth_pattern, line).group(1)
            if not date_of_birth and re.search(date_of_birth_pattern, line):
                date_of_birth = re.search(date_of_birth_pattern, line).group(1)
            if not card_number and re.search(card_number_pattern, line):
                card_number = re.search(card_number_pattern, line).group(1)

        # Print the extracted values
        print(f"Name: {name}")
        print(f"ID Number: {id_number}")
        print(f"Place of Birth: {place_of_birth}")
        print(f"Date of Birth: {date_of_birth}")
        print(f"Card Number: {card_number}")
            
    elif found_word == 'library':
        name_pattern = r'Name\s+([A-Z][a-z]+\s[A-Z][a-z]+)' # przekazuje ze slowem "Name"
        id_number_pattern = r'ID number\s*(\d+)'
        expiration_date_pattern = r'Expirationdate\s*([\d/]+)' # nie dziala
        phone_number_pattern = r'Phone\s*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})' # nie dziala
        
        # Initialize variables
        name = None
        id_number = None
        expiration_date = None
        phone_number = None

        # Search for patterns line by line
        for line in data.split('\n'):
            line = line.strip()
            if not name and re.match(name_pattern, line):
                name = line
            if not id_number and re.search(id_number_pattern, line):
                id_number = re.search(id_number_pattern, line).group(1)
            if not expiration_date_pattern and re.search(expiration_date_pattern, line):
                expiration_date_pattern = re.search(expiration_date_pattern, line).group(1)
            if not phone_number_pattern and re.search(phone_number_pattern, line):
                phone_number_pattern = re.search(phone_number_pattern, line).group(1)

        # Print the extracted values
        print(f"Name: {name}")
        print(f"ID Number: {id_number}")
        print(f"Expiration Date: {expiration_date}")
        print(f"Phone Number: {phone_number}")
        
    else:
        print("Unsupported type of file.")
        
    
    
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
recognize_card_type("photos/person2/person2_library_card.png")

# C:\Program Files\Tesseract-OCR\tesseract.exe