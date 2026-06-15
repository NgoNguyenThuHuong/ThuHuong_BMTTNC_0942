# BÁO CÁO KẾT QUẢ THỰC HÀNH - TUẦN 6
## CÂU 1: GIAO DIỆN MÃ HÓA VÀ GIẢI MÃ RAIL FENCE CIPHER

### 1. Thông tin kết quả chạy thử nghiệm (từ hình ảnh chụp màn hình):
*   **Thuật toán sử dụng**: Rail Fence Cipher (Mã hóa đường sắt - một dạng mã hóa hoán vị cổ điển).
*   **Thông điệp đầu vào (Plain Text)**: `hutech`
*   **Khóa mã hóa (Key - Rails)**: `3` (Số đường ray bằng 3)
*   **Thông điệp mã hóa đầu ra (Cipher Text)**: `hcueht`

---

### 2. Phân tích chi tiết quá trình mã hóa bằng lý thuyết:
Với bản rõ là `hutech` (độ dài 6 ký tự) và số đường ray (khóa) \(K = 3\), quá trình phân bổ các ký tự theo hình răng cưa (đường ray) diễn ra như sau:

1. **Bước 1: Thiết lập ma trận đường ray**
   * Ký tự 1 (`h`): Đặt vào Đường ray 1
   * Ký tự 2 (`u`): Đặt vào Đường ray 2
   * Ký tự 3 (`t`): Đặt vào Đường ray 3
   * Ký tự 4 (`e`): Đặt vào Đường ray 2 (đổi hướng đi lên)
   * Ký tự 5 (`c`): Đặt vào Đường ray 1 (đổi hướng đi lên)
   * Ký tự 6 (`h`): Đặt vào Đường ray 2 (đổi hướng đi xuống)

2. **Bước 2: Biểu diễn sơ đồ đường ray**
   ```text
   Đường ray 1:  h   .   .   .   c   .
   Đường ray 2:  .   u   .   e   .   h
   Đường ray 3:  .   .   t   .   .   .
   ```

3. **Bước 3: Đọc kết quả theo từng dòng (từ trên xuống dưới)**
   * Dòng 1 (Đường ray 1): `hc`
   * Dòng 2 (Đường ray 2): `ueh`
   * Dòng 3 (Đường ray 3): `t`
   
   Ghép các dòng lại với nhau ta được Bản mã (Cipher Text): **`hcueht`**

---

### 3. Đánh giá kết quả chương trình:
*   Kết quả chạy thực tế trên giao diện **PyQt5** (đầu ra là `hcueht`) khớp hoàn toàn 100% với tính toán lý thuyết.
*   Giao diện hoạt động ổn định, các chức năng **Mã hóa (Encrypt)**, **Giải mã (Decrypt)** và **Xóa (Clear)** thực hiện chính xác các yêu cầu nghiệp vụ.
