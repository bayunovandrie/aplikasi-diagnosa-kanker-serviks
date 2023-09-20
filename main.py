import cv2
import os

# Inisialisasi kamera dengan ID 0 (kamera utama)
cap = cv2.VideoCapture(0)

while True:
    # Membaca frame dari kamera
    ret, frame = cap.read()

    # Menampilkan frame dalam jendela
    cv2.imshow('Camera', frame)

    # Menunggu tombol ditekan
    key = cv2.waitKey(1)

    # Jika tombol spasi ditekan, simpan gambar
    if key == ord(' '):
        image_filename = "captured_image.jpg"

        path = os.path.join("img", image_filename)
        cv2.imwrite(path, frame)
        print("Gambar telah diambil dan disimpan sebagai", image_filename)
        break  # Keluar dari loop jika gambar sudah diambil

    # Jika tombol Esc ditekan, keluar dari loop
    if key == 27:
        break

# Menutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()
