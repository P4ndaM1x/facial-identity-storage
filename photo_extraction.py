import cv2

def get_box(img, top_correction=0.1):
    cc = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    box = cc.detectMultiScale(gray_img, 1.02, 2, minSize=(200,200))[0]
    height = box[3]
    box[1] -= height*top_correction
    box[3] += height*top_correction

    return box

def get_photo(img):
    x,y, w,h = get_box(img)

    return img[y:y+h, x:x+w]

if __name__ == '__main__':
    img = cv2.imread('images/person_3/bicycle_card.png')

    cv2.imshow("Cut photo", get_photo(img))

    rect = get_box(img)
    cv2.rectangle(img, rect, (0,255,0), 5)
    cv2.imshow("Bounding box", img)

    cv2.waitKey(100_000)
    cv2.destroyAllWindows()