import tkinter
from tkinter import ttk
import random
from tkinter import messagebox

# Từ điển ánh xạ màu tiếng Anh sang tiếng Việt và mã màu hex
mau_tieng_anh = {
    'red': ('Đỏ', '#FF0000'), 'blue': ('Xanh Dương', '#0000FF'), 'green': ('Xanh Lá', '#008000'),
    'pink': ('Hồng', '#FFC0CB'), 'black': ('Đen', '#000000'), 'yellow': ('Vàng', '#FFFF00'),
    'orange': ('Cam', '#FFA500'), 'white': ('Trắng', '#FFFFFF'), 'purple': ('Tím', '#800080'),
    'brown': ('Nâu', '#A52A2A')
}

# Danh sách màu sắc tiếng Việt (dùng để hiển thị nội dung nhãn)
mau_sac = [value[0] for value in mau_tieng_anh.values()]
diem = 0
diem_cao = 0
thoi_gian_con_lai = 60
dem_tg_dang_chay = False  # Biến kiểm tra trạng thái đếm ngược
che_do = "thuong"  # Mặc định chế độ là thường
tro_choi_ket_thuc = False


# Hàm bắt đầu trò chơi
def bat_dau_tro_choi(event=None):
    global thoi_gian_con_lai, dem_tg_dang_chay, che_do, tro_choi_ket_thuc

    # Ngăn việc bắt đầu nhiều bộ đếm cùng lúc
    if dem_tg_dang_chay:
        return

    tro_choi_ket_thuc = False  # Reset trạng thái trò chơi

    # Nếu chế độ "thường"
    if che_do == "thuong":
        do_kho = combo.get()
        if do_kho == "Dễ (60s)":
            thoi_gian_con_lai = 60
        elif do_kho == "Trung bình(45s)":
            thoi_gian_con_lai = 45
        elif do_kho == "Khó(30s)":
            thoi_gian_con_lai = 30

        thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))
        dem_tg_dang_chay = True
        dem_nguoc()
        mau_tiep_theo()
    else:  # Chế độ sinh tồn
        thoi_gian_con_lai = 15  # Thời gian ban đầu cho chế độ Sinh Tồn
        diem = 0
        diem_nhan.config(text="Điểm: " + str(diem))
        mau_tiep_theo()  # Hiển thị màu tiếp theo
        hien_thi_sinh_ton()  # Hiển thị giao diện chế độ Sinh Tồn
        thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))  # Hiển thị thời gian ban đầu
        dem_tg_dang_chay = True
        dem_nguoc()  # Gọi hàm đếm ngược khi bắt đầu chế độ Sinh Tồn

# Hàm hiển thị giao diện chế độ sinh tồn
def hien_thi_sinh_ton():
    if che_do == "sinh_ton":
        # Vô hiệu hóa ComboBox và cập nhật hướng dẫn
        combo.config(state="disabled")  # Vô hiệu hóa để không thể chọn
        thoi_gian_nhan.pack_forget()  # Ẩn nhãn thời gian
        huong_dan.config(text="Chế độ Sinh Tồn: gõ màu sắc của chữ (không phải nội dung chữ)!")
        diem_nhan.config(text=f"Điểm: {diem} | Điểm cao nhất: {diem_cao}")  # Hiển thị điểm
        nut_choi_lai.pack_forget()  # Đảm bảo ẩn nút chơi lại khi bắt đầu
    else:
        # Nếu quay lại chế độ thường, đảm bảo các phần tử hiển thị lại
        combo.config(state="readonly")  # Kích hoạt lại ComboBox
        thoi_gian_nhan.pack()  # Hiển thị nhãn thời gian
        huong_dan.config(text="Chọn độ khó, gõ màu sắc của chữ (không phải nội dung chữ)!")
        diem_nhan.pack()
        nut_choi_lai.pack_forget()

# Hàm quay lại chế độ Thường
def quay_lai_che_do_thuong():
    global che_do, diem
    che_do = "thuong"  # Đặt chế độ về "Thường"
    diem = 0  # Đặt lại điểm về 0
    combo.config(state="readonly")  # Kích hoạt lại ComboBox
    thoi_gian_nhan.pack()  # Hiển thị nhãn thời gian
    huong_dan.config(text="Chọn độ khó, gõ màu sắc của chữ (không phải nội dung chữ)!")
    nhan.pack()  # Hiển thị lại nhãn màu
    diem_nhan.config(text=f"Điểm: {diem}")  # Cập nhật điểm về 0
    o_nhap.pack()  # Hiển thị hộp nhập liệu
    nut_choi_lai.pack_forget()  # Ẩn nút chơi lại

# Hàm chọn và hiển thị màu tiếp theo
def mau_tiep_theo():
    global diem, thoi_gian_con_lai
    if tro_choi_ket_thuc:  # Nếu trò chơi đã kết thúc, không cho nhập tiếp
        return
    if che_do == "thuong" and thoi_gian_con_lai > 0:  # Chế độ thường
        o_nhap.focus_set()  # Đảm bảo hộp nhập liệu có thể nhập tiếp
        nhap_vao = o_nhap.get().lower()
        mau_hien_tai = mau_sac[1]
        ten_tieng_anh = [key for key, value in mau_tieng_anh.items() if value[0] == mau_hien_tai][0]
        if nhap_vao == mau_hien_tai.lower() or nhap_vao == ten_tieng_anh:
            diem += 1
        o_nhap.delete(0, tkinter.END)
        random.shuffle(mau_sac)
        ma_mau_hex = [value[1] for key, value in mau_tieng_anh.items() if value[0] == mau_sac[1]][0]
        nhan.config(fg=ma_mau_hex, text=mau_sac[0], font=('Helvetica', 40))
        diem_nhan.config(text="Điểm: " + str(diem))
    elif che_do == "sinh_ton":  # Chế độ sinh tồn
        o_nhap.focus_set()  # Đảm bảo hộp nhập liệu có thể nhập tiếp
        nhap_vao = o_nhap.get().lower()
        mau_hien_tai = mau_sac[1]
        ten_tieng_anh = [key for key, value in mau_tieng_anh.items() if value[0] == mau_hien_tai][0]
        if nhap_vao == mau_hien_tai.lower() or nhap_vao == ten_tieng_anh:
            diem += 1
            thoi_gian_con_lai += 3  # Cộng thêm 3 giây mỗi lần nhập đúng
        o_nhap.delete(0, tkinter.END)
        random.shuffle(mau_sac)
        ma_mau_hex = [value[1] for key, value in mau_tieng_anh.items() if value[0] == mau_sac[1]][0]
        nhan.config(fg=ma_mau_hex, text=mau_sac[0], font=('Helvetica', 40))
        diem_nhan.config(text="Điểm: " + str(diem))
        thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))  # Cập nhật lại thời gian


# Hàm đếm ngược thời gian
def dem_nguoc():
    global thoi_gian_con_lai, dem_tg_dang_chay, diem_cao

    if thoi_gian_con_lai > 0:  # Nếu thời gian còn lại lớn hơn 0
        thoi_gian_con_lai -= 1  # Giảm thời gian mỗi giây
        thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))  # Cập nhật nhãn thời gian
        thoi_gian_nhan.after(1000, dem_nguoc)  # Đếm ngược mỗi giây
    else:
        dem_tg_dang_chay = False  # Dừng đếm ngược khi hết thời gian
        if diem > diem_cao:
            diem_cao = diem
        ket_thuc_tro_choi()  # Kết thúc trò chơi khi hết thời gian

def choi_lai():
    global diem, thoi_gian_con_lai, dem_tg_dang_chay, tro_choi_ket_thuc, che_do
    tro_choi_ket_thuc = False  # Reset trạng thái trò chơi
    diem = 0  # Đặt lại điểm hiện tại
    thoi_gian_con_lai = 15  # Đặt lại thời gian
    dem_tg_dang_chay = False  # Đặt lại trạng thái đếm ngược
    diem_nhan.config(text=f"Điểm: {diem} | Điểm cao nhất: {diem_cao}")  # Hiển thị điểm hiện tại và điểm cao nhất
    thoi_gian_nhan.config(text="Thời gian còn lại: " + str(thoi_gian_con_lai))
    nut_choi_lai.pack_forget()  # Ẩn nút chơi lại
    o_nhap.delete(0, tkinter.END)  # Xóa nội dung trong hộp nhập liệu
    if che_do == "thuong":
        mau_tiep_theo()  # Hiển thị một màu mới ngay lập tức
    else:
        hien_thi_sinh_ton()  # Hiển thị lại giao diện chế độ Sinh Tồn


def ket_thuc_tro_choi():
    global diem, tro_choi_ket_thuc
    tro_choi_ket_thuc = True  # Đánh dấu trạng thái trò chơi kết thúc
    messagebox.showinfo("Hết thời gian", f"Trò chơi kết thúc!\nĐiểm của bạn: {diem}\nĐiểm cao nhất: {diem_cao}")
    diem_nhan.config(text=f"Kết thúc! Điểm của bạn: {diem} | Điểm cao nhất: {diem_cao}")
    nut_choi_lai.pack()  # Hiển thị nút chơi lại

# Hàm chọn chế độ chơi từ menu
def chon_che_do(che_do_chon):
    global che_do, diem
    che_do = che_do_chon
    diem = 0  # Đặt lại điểm về 0 khi chuyển chế độ
    if che_do == "thuong":
        messagebox.showinfo("Chế độ chơi", "Chế độ Thường đã được chọn!")
        quay_lai_che_do_thuong()
    elif che_do == "sinh_ton":
        messagebox.showinfo("Chế độ chơi", "Chế độ Sinh Tồn đã được chọn!")
        hien_thi_sinh_ton()

# Code chính

# Tạo cửa sổ giao diện
root = tkinter.Tk()
root.title("TRÒ CHƠI ĐOÁN MÀU")
root.geometry("600x400")

# Thêm nhãn hướng dẫn
huong_dan = tkinter.Label(root, text="Chọn độ khó, gõ màu sắc của chữ (không phải nội dung chữ)!",
                          font=('Helvetica', 12))
huong_dan.pack()

# Thêm ComboBox để chọn độ khó
combo = ttk.Combobox(root, values=["Dễ (60s)", "Trung bình(45s)", "Khó(30s)"], state="readonly", font=('Helvetica', 10))
combo.set("Dễ (60s)")  # Đặt độ khó mặc định
combo.pack()

# Thêm menu chọn chế độ chơi
menu = tkinter.Menu(root)
root.config(menu=menu)

che_do_menu = tkinter.Menu(menu)
menu.add_cascade(label="Chế độ chơi", menu=che_do_menu)
che_do_menu.add_command(label="Chế độ Thường", command=lambda: chon_che_do("thuong"))
che_do_menu.add_command(label="Chế độ Sinh Tồn", command=lambda: chon_che_do("sinh_ton"))

# Thêm nhãn điểm
diem_nhan = tkinter.Label(root, text="Nhấn Enter để bắt đầu", font=('Helvetica', 12))
diem_nhan.pack()

# Thêm nhãn thời gian còn lại
thoi_gian_nhan = tkinter.Label(root, text="Thời gian còn lại: " + str(thoi_gian_con_lai),
                               font=('Helvetica', 12))
thoi_gian_nhan.pack()

# Thêm nhãn hiển thị màu sắc
nhan = tkinter.Label(root, font=('Helvetica', 60))
nhan.pack()

# Thêm hộp nhập liệu để gõ màu
o_nhap = tkinter.Entry(root, font=('Helvetica', 20), width=10)

# Thêm nút chơi lại
nut_choi_lai = tkinter.Button(root, text="Chơi lại", font=('Helvetica', 12), command=choi_lai)
nut_choi_lai.pack_forget()

# Chạy hàm 'bat_dau_tro_choi' khi nhấn phím Enter
root.bind('<Return>', lambda event: (mau_tiep_theo() if dem_tg_dang_chay and not tro_choi_ket_thuc else bat_dau_tro_choi()))
o_nhap.pack()

# Đặt con trỏ vào hộp nhập liệu
o_nhap.focus_set()

# Bắt đầu giao diện
root.mainloop()
