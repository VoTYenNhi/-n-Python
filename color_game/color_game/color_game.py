import tkinter
from tkinter import ttk
import random

# từ điển ánh xạ màu tiếng Anh sang tiếng Việt và mã màu hex
mau_tieng_anh = {
    'red': ('Đỏ', '#FF0000'), 'blue': ('Xanh Dương', '#0000FF'), 'green': ('Xanh Lá', '#008000'),
    'pink': ('Hồng', '#FFC0CB'), 'black': ('Đen', '#000000'), 'yellow': ('Vàng', '#FFFF00'),
    'orange': ('Cam', '#FFA500'), 'white': ('Trắng', '#FFFFFF'), 'purple': ('Tím', '#800080'),
    'brown': ('Nâu', '#A52A2A')
}

# danh sách màu sắc tiếng Việt (dùng để hiển thị nội dung nhãn)
mau_sac = [value[0] for value in mau_tieng_anh.values()]
diem = 0
diem_cao = 0
thoi_gian_con_lai = 60
dem_tg_dang_chay = False  # Biến kiểm tra trạng thái đếm ngược


# hàm bắt đầu trò chơi
def bat_dau_tro_choi(event=None):
    global thoi_gian_con_lai, dem_tg_dang_chay

    # Ngăn việc bắt đầu nhiều bộ đếm cùng lúc
    if dem_tg_dang_chay:
        return

    # Lấy độ khó từ ComboBox
    do_kho = combo.get()
    if do_kho == "Dễ (60s)":
        thoi_gian_con_lai = 60
    elif do_kho == "Trung bình(45s)":
        thoi_gian_con_lai = 45
    elif do_kho == "Khó(30s)":
        thoi_gian_con_lai = 30

    # Cập nhật thời gian và trạng thái đếm ngược
    thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))
    dem_tg_dang_chay = True

    # Bắt đầu đếm ngược và hiển thị màu đầu tiên
    dem_nguoc()
    mau_tiep_theo()


# hàm chọn và hiển thị màu tiếp theo
def mau_tiep_theo():
    global diem
    # nếu trò chơi đang diễn ra và không cho phép nhập khi đồng hồ chạy
    if thoi_gian_con_lai > 0:
        o_nhap.focus_set()  # Đảm bảo hộp nhập liệu có thể nhập tiếp
        # lấy giá trị nhập vào và chuyển về chữ thường
        nhap_vao = o_nhap.get().lower()
        # lấy màu hiện tại (tiếng Việt)
        mau_hien_tai = mau_sac[1]
        # tìm tên tiếng Anh dựa trên màu tiếng Việt
        ten_tieng_anh = [key for key, value in mau_tieng_anh.items() if value[0] == mau_hien_tai][0]
        # kiểm tra nếu đầu vào khớp với màu hiển thị (bằng tiếng Việt hoặc tiếng Anh)
        if nhap_vao == mau_hien_tai.lower() or nhap_vao == ten_tieng_anh:
            diem += 1
        # xóa nội dung trong hộp nhập liệu
        o_nhap.delete(0, tkinter.END)
        # trộn màu và chọn màu ngẫu nhiên
        random.shuffle(mau_sac)
        # lấy mã hex của màu mới
        ma_mau_hex = [value[1] for key, value in mau_tieng_anh.items() if value[0] == mau_sac[1]][0]
        # thay đổi màu chữ và nội dung hiển thị
        nhan.config(fg=ma_mau_hex, text=mau_sac[0], font=('Helvetica', 40))
        # cập nhật điểm
        diem_nhan.config(text="Điểm: " + str(diem))


# hàm đếm ngược thời gian
def dem_nguoc():
    global thoi_gian_con_lai, dem_tg_dang_chay, diem_cao

    if thoi_gian_con_lai > 0:
        thoi_gian_con_lai -= 1
        thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))
        thoi_gian_nhan.after(1000, dem_nguoc)
    else:
        dem_tg_dang_chay = False
        if diem > diem_cao:
            diem_cao = diem
        ket_thuc_tro_choi()


def choi_lai():
    global diem, thoi_gian_con_lai, dem_tg_dang_chay
    diem = 0
    thoi_gian_con_lai = 60
    dem_tg_dang_chay = False
    diem_nhan.config(text="Nhấn Enter để bắt đầu")
    thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))
    nhan.config(text="", fg="#000000", font=('Helvetica', 40))
    nut_choi_lai.pack_forget()  # Ẩn nút chơi lại
    o_nhap.delete(0, tkinter.END)  # Xóa nội dung trong hộp nhập liệu


def ket_thuc_tro_choi():
    global diem
    diem_nhan.config(text=f"Kết thúc! Điểm của bạn: {diem} | Điểm cao nhất: {diem_cao}")
    nut_choi_lai.pack()


# Code chính

# tạo cửa sổ giao diện
root = tkinter.Tk()
root.title("TRÒ CHƠI ĐOÁN MÀU")
root.geometry("500x350")

# thêm nhãn hướng dẫn
huong_dan = tkinter.Label(root, text="Chọn độ khó, gõ màu sắc của chữ (không phải nội dung chữ)!",
                          font=('Helvetica', 12))
huong_dan.pack()

# thêm ComboBox để chọn độ khó
combo = ttk.Combobox(root, values=["Dễ (60s)", "Trung bình(45s)", "Khó(30s)"], state="readonly", font=('Helvetica', 10))
combo.set("Dễ (60s)")  # Đặt độ khó mặc định
combo.pack()

# thêm nhãn điểm
diem_nhan = tkinter.Label(root, text="Nhấn Enter để bắt đầu", font=('Helvetica', 12))
diem_nhan.pack()

# thêm nhãn thời gian còn lại
thoi_gian_nhan = tkinter.Label(root, text="Thời gian còn lại: " + str(thoi_gian_con_lai),
                               font=('Helvetica', 12))
thoi_gian_nhan.pack()

# thêm nhãn hiển thị màu sắc
nhan = tkinter.Label(root, font=('Helvetica', 60))
nhan.pack()

# thêm hộp nhập liệu để gõ màu
o_nhap = tkinter.Entry(root, font=('Helvetica', 20), width=10)

# thêm nút chơi lại
nut_choi_lai = tkinter.Button(root, text="Chơi lại", font=('Helvetica', 12), command=choi_lai)
nut_choi_lai.pack_forget()

# chạy hàm 'bat_dau_tro_choi' khi nhấn phím Enter
root.bind('<Return>', bat_dau_tro_choi)
o_nhap.pack()

# đặt con trỏ vào hộp nhập liệu
o_nhap.focus_set()

# bắt đầu giao diện
root.mainloop()
