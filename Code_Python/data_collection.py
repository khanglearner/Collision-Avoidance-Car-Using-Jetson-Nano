import cv2
import os

# Thư mục lưu ảnh
output_folder_free = 'free'
output_folder_blocked = 'blocked'

os.makedirs(output_folder_free, exist_ok=True)
os.makedirs(output_folder_blocked, exist_ok=True)

# Mở webcam
cap = cv2.VideoCapture(0)

# Đếm số ảnh
count_free = 0
count_blocked = 0

print("Nhấn phím “f” để chụp ảnh không vật cản, nhấn phím “b” để chụp ảnh có vật cản 'q' để thoát.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc từ webcam")
        break

    cv2.imshow('Webcam', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('f'):
        # Resize về 224x224
        resized = cv2.resize(frame, (224, 224))

        # Tạo tên file
        filename = f'image_{count_free}.jpeg'
        filepath = os.path.join(output_folder_free, filename)

        # Lưu ảnh dưới dạng JPEG
        cv2.imwrite(filepath, resized)

        print(f'Đã lưu {filepath}')
        count_free += 1


    if key == ord('b'):
        # Resize về 224x224
        resized = cv2.resize(frame, (224, 224))

        # Tạo tên file
        filename = f'image_{count_blocked}.jpeg'
        filepath = os.path.join(output_folder_blocked, filename)

        # Lưu ảnh dưới dạng JPEG
        cv2.imwrite(filepath, resized)

        print(f'Đã lưu {filepath}')
        count_blocked += 1

    elif key == ord('q'):
        break

# Giải phóng
cap.release()
cv2.destroyAllWindows()

