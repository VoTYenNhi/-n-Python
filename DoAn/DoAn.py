import os
import json
import random
import tkinter as tk
from tkinter import messagebox

# Đường dẫn thư mục và tên file
DIRECTORY = "tu_vung_data"
FILE_NAME = "tu_vung.json"
FILE_PATH = os.path.join(DIRECTORY, FILE_NAME)

# Hàm đảm bảo thư mục và file tồn tại
def ensure_file_exists():
    # Kiểm tra xem thư mục có tồn tại không, nếu không thì tạo
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    
    # Kiểm tra xem file có tồn tại không, nếu không thì tạo file mới
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump({}, file, ensure_ascii=False, indent=4)

# Hàm lưu từ vào file JSON
def luu_tu(tu, nghia):
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            tu_vung = json.load(file)
    except json.JSONDecodeError:
        # Nếu file bị lỗi, tạo lại từ vựng mới
        tu_vung = {}

    # Kiểm tra nếu từ đã tồn tại
    if tu in tu_vung:
        messagebox.showinfo("Thông báo", f"Từ '{tu}' đã tồn tại với nghĩa: '{tu_vung[tu]}'")
        return

    tu_vung[tu] = nghia

    # Lưu lại từ vựng vào file JSON
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(tu_vung, file, ensure_ascii=False, indent=4)

    messagebox.showinfo("Thông báo", f"Đã thêm từ: {tu} - {nghia}")

# Hàm hiển thị một từ ngẫu nhiên
def hien_tu_ngau_nhien():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            tu_vung = json.load(file)
    except FileNotFoundError:
        tu_vung = {}

    if not tu_vung:
        messagebox.showinfo("Thông báo", "Chưa có từ vựng nào!")
        return

    tu = random.choice(list(tu_vung.keys()))
    nghia = tu_vung[tu]
    messagebox.showinfo("Từ ngẫu nhiên", f"Từ: {tu}\nNghĩa: {nghia}")

# Hàm hiển thị tất cả từ vựng
def hien_tat_ca_tu():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            tu_vung = json.load(file)
    except FileNotFoundError:
        tu_vung = {}

    if not tu_vung:
        messagebox.showinfo("Thông báo", "Chưa có từ vựng nào!")
        return

    danh_sach = "\n".join([f"{tu}: {nghia}" for tu, nghia in tu_vung.items()])
    messagebox.showinfo("Danh sách từ vựng", danh_sach)

# Hàm xử lý thêm từ
def xu_ly_them_tu():
    tu = entry_tu.get().strip().lower()
    nghia = entry_nghia.get().strip()
    if not tu or not nghia:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ từ và nghĩa!")
        return
    tu = tu.capitalize()
    luu_tu(tu, nghia)
    entry_tu.delete(0, tk.END)
    entry_nghia.delete(0, tk.END)
# Hàm tạo cửa sổ thông báo tùy chỉnh (Toplevel)
def custom_messagebox(title, message):
    msg_box = tk.Toplevel()
    msg_box.title(title)
    msg_box.geometry("600x200")  # Điều chỉnh kích thước cửa sổ
    msg_box.resizable(False, False)  # Ngăn người dùng thay đổi kích thước cửa sổ

    label = tk.Label(msg_box, text=message, font=("Arial", 12), wraplength=350)
    label.pack(pady=20, padx=20)

    btn_ok = tk.Button(msg_box, text="OK", font=("Arial", 12), command=msg_box.destroy)
    btn_ok.pack(pady=10)

def kiem_tra_tu_vung():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            tu_vung = json.load(file)
    except json.JSONDecodeError:
        # Nếu file bị lỗi, tạo lại từ vựng mới
        tu_vung = {}

    if not tu_vung:
        messagebox.showinfo("Thông báo", "Chưa có từ vựng nào để kiểm tra!")
        return

    # Chọn một từ ngẫu nhiên
    tu = random.choice(list(tu_vung.keys()))
    nghia_dung = tu_vung[tu]

    # Tạo cửa sổ để người dùng nhập nghĩa
    def kiem_tra_dap_an():
        dap_an = entry_nghia_kiem_tra.get().strip()
        if dap_an.lower() == nghia_dung.lower():
            messagebox.showinfo("Kết quả", " Bạn đã trả lời chính xác.")
        else:
            messagebox.showinfo("Kết quả", f"Sai rồi! Nghĩa đúng là: {nghia_dung}")

        entry_nghia_kiem_tra.delete(0, tk.END)
        entry_nghia_kiem_tra.config(state=tk.DISABLED)  # Khóa ô nhập sau khi kiểm tra

    # Tạo giao diện nhập nghĩa từ
    kiem_tra_window = tk.Toplevel(root)
    kiem_tra_window.title("Kiểm tra từ vựng")
    kiem_tra_window.geometry("400x200")

    label_kiem_tra = tk.Label(kiem_tra_window, text=f"Từ: {tu}", font=("Arial", 14))
    label_kiem_tra.pack(pady=20)

    entry_nghia_kiem_tra = tk.Entry(kiem_tra_window, font=("Arial", 14), width=30)
    entry_nghia_kiem_tra.pack(pady=10)

    btn_kiem_tra = tk.Button(kiem_tra_window, text="Kiểm tra", font=("Arial", 14), command=kiem_tra_dap_an)
    btn_kiem_tra.pack(pady=20)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng học từ vựng tiếng Anh")

# Tăng kích thước cửa sổ
root.geometry("800x400")

# Giao diện: Nhập từ và nghĩa
frame_nhap = tk.Frame(root)
frame_nhap.pack(pady=20)

tk.Label(frame_nhap, text="Từ tiếng Anh:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_tu = tk.Entry(frame_nhap, width=40, font=("Arial", 14))
entry_tu.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_nhap, text="Nghĩa tiếng Việt:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_nghia = tk.Entry(frame_nhap, width=40, font=("Arial", 14))
entry_nghia.grid(row=1, column=1, padx=10, pady=10)

btn_them = tk.Button(frame_nhap, text="Thêm từ", font=("Arial", 14), command=xu_ly_them_tu)
btn_them.grid(row=2, columnspan=2, pady=20)

# Giao diện: Các chức năng khác
frame_chuc_nang = tk.Frame(root)
frame_chuc_nang.pack(pady=20)

btn_tu_ngau_nhien = tk.Button(frame_chuc_nang, text="Hiển thị từ ngẫu nhiên", font=("Arial", 14), command=hien_tu_ngau_nhien)
btn_tu_ngau_nhien.pack(fill=tk.X, padx=20, pady=5)

btn_xem_tat_ca = tk.Button(frame_chuc_nang, text="Xem tất cả từ đã lưu", font=("Arial", 14), command=hien_tat_ca_tu)
btn_xem_tat_ca.pack(fill=tk.X, padx=20, pady=5)

btn_kiem_tra = tk.Button(frame_chuc_nang, text="Kiểm tra từ vựng", font=("Arial", 14), command=kiem_tra_tu_vung)
btn_kiem_tra.pack(fill=tk.X, padx=20, pady=5)

btn_thoat = tk.Button(frame_chuc_nang, text="Thoát", font=("Arial", 14), command=root.quit)
btn_thoat.pack(fill=tk.X, padx=20, pady=5)

# Đảm bảo file và thư mục tồn tại
ensure_file_exists()

# Chạy ứng dụng
root.mainloop()

