# KMA Schedule Parser

**Ngôn ngữ:** [🇺🇸 English](README.md) | [🇻🇳 Tiếng Việt](README_vi.md)

Công cụ Python để phân tích thời khóa biểu từ định dạng HTML của KMA (Học viện Kỹ thuật Mật mã) và chuyển đổi sang định dạng ICS tương thích với Google Calendar.

## Tính năng

- Phân tích file HTML thời khóa biểu từ cổng thông tin sinh viên KMA
- Chuyển đổi định dạng thời khóa biểu tiếng Việt phức tạp sang định dạng lịch ICS
- Xử lý nhiều khoảng thời gian và phạm vi ngày tháng
- Hỗ trợ cả buổi học lý thuyết (LT) và thực hành (TH)
- Bao gồm chi tiết môn học, giảng viên và địa điểm
- Xử lý múi giờ chính xác cho Việt Nam (Asia/Ho_Chi_Minh)

## Yêu cầu

- Python 3.9+
- beautifulsoup4
- icalendar

## Cài đặt

Vì dự án bao gồm file `pyproject.toml` với tất cả dependencies được liệt kê, việc cài đặt rất đơn giản:

### Sử dụng pip (khuyên dùng)
```bash
pip install .
```

### Sử dụng uv (nhanh hơn)
Nếu bạn đã cài [uv](https://github.com/astral-sh/uv):
```bash
uv pip install .
```

### Cài đặt dependencies thủ công
Nếu bạn muốn cài dependencies thủ công:
```bash
pip install beautifulsoup4 icalendar
```

Hoặc với uv:
```bash
uv pip install beautifulsoup4 icalendar
```

## Hướng dẫn sử dụng

### Bước 1: Lấy mã HTML thời khóa biểu từ Cổng thông tin KMA

1. **Truy cập cổng thông tin sinh viên KMA**:
   - Đi tới: http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Reports/Form/StudentTimeTable.aspx
   - Đăng nhập bằng tài khoản sinh viên của bạn

2. **Điều hướng đến thời khóa biểu của bạn**:
   - Trang sẽ hiển thị "Xem kết quả ĐKH" (Xem Kết quả Đăng ký Học)
   - Đảm bảo học kỳ và đợt học được chọn đúng
   - Bảng thời khóa biểu của bạn sẽ hiển thị trên trang

3. **Lấy mã nguồn HTML**:
   - Nhấn `Ctrl + U` (hoặc `Cmd + U` trên Mac) để xem mã nguồn trang
   - Điều này sẽ mở tab/cửa sổ mới với mã HTML thô
   - Nhấn `Ctrl + A` (hoặc `Cmd + A` trên Mac) để chọn tất cả nội dung HTML
   - Nhấn `Ctrl + C` (hoặc `Cmd + C` trên Mac) để sao chép HTML

4. **Lưu vào file**:
   - Tạo file text mới (ví dụ: `my_schedule.html`)
   - Dán nội dung HTML đã sao chép vào file
   - Lưu file với phần mở rộng `.html` hoặc `.txt`

> **📝 Lưu ý quan trọng:**
> - Đảm bảo bạn đã đăng nhập và có thể xem thời khóa biểu thực tế trước khi lấy mã nguồn
> - Link cổng thông tin: http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Reports/Form/StudentTimeTable.aspx
> - Nếu bạn thấy trang trống hoặc trang đăng nhập, hãy đảm bảo đăng nhập trước và điều hướng đến thời khóa biểu
> - Mã nguồn HTML phải chứa dữ liệu bảng với thông tin môn học của bạn
> - Nếu trang hiển thị "không có dữ liệu" hoặc thời khóa biểu trống, hãy kiểm tra lựa chọn học kỳ/đợt học

### Bước 2: Chạy trình phân tích

```bash
python main.py -i <file_đầu_vào> -o <file_đầu_ra>
```

Ví dụ:
```bash
python main.py -i my_schedule.html -o my_calendar.ics
```

### Bước 3: Import vào Google Calendar

- Mở Google Calendar
- Nhấp vào dấu "+" bên cạnh "Other calendars"
- Chọn "Import"
- Tải lên file ICS đã tạo

## Tùy chọn dòng lệnh

- `-i, --input`: Đường dẫn file HTML chứa thời khóa biểu KMA (bắt buộc)
- `-o, --output`: Đường dẫn file ICS đầu ra cho lịch được tạo (bắt buộc)
- `-h, --help`: Hiển thị thông báo trợ giúp và thoát

## Ví dụ

```bash
# Sử dụng cơ bản
python main.py -i schedule.html -o calendar.ics

# Sử dụng đường dẫn đầy đủ
python main.py -i /path/to/schedule.html -o /path/to/output/calendar.ics

# Hiển thị trợ giúp
python main.py --help
```

## Cách hoạt động

Trình phân tích:

1. **Trích xuất dữ liệu thời khóa biểu** từ bảng HTML sử dụng BeautifulSoup
2. **Phân tích định dạng thời gian phức tạp** như "Từ 27/10/2025 đến 16/11/2025: (1) Thứ 2 tiết 1,2,3 (LT)"
3. **Chuyển đổi tên ngày tiếng Việt** (Thứ 2 = Thứ Hai, v.v.) sang ngày trong tuần tiêu chuẩn
4. **Ánh xạ khoảng thời gian** (tiết 1,2,3) sang giờ thực tế (07:00-09:25)
5. **Tạo sự kiện lặp lại** cho mỗi tuần trong phạm vi ngày được chỉ định
6. **Tạo định dạng ICS** tương thích với Google Calendar và các ứng dụng lịch khác

## Ánh xạ khung giờ

Trình phân tích sử dụng khung giờ học tiêu chuẩn:

- Tiết 1: 07:00-07:45
- Tiết 2: 07:50-08:35
- Tiết 3: 08:40-09:25
- Tiết 4: 09:35-10:20
- Tiết 5: 10:25-11:10
- Tiết 6: 11:15-12:00
- Tiết 7: 13:00-13:45
- Tiết 8: 13:50-14:35
- Tiết 9: 14:40-15:25
- Tiết 10: 15:35-16:20
- Tiết 11: 16:25-17:10
- Tiết 12: 17:15-18:00

## Ví dụ đầu ra

File ICS được tạo chứa các sự kiện như:

```
BEGIN:VEVENT
SUMMARY:Lập trình hướng đối tượng-1-25 (A21C908)
DTSTART;TZID=Asia/Ho_Chi_Minh:20250811T093500
DTEND;TZID=Asia/Ho_Chi_Minh:20250811T120000
DESCRIPTION:Course: CLC1ATCTKM5\nType: LT\nInstructor: Bùi Thị Như (GVM), Trịnh Anh Tuấn (GVM)\nPeriods: 4, 5, 6
LOCATION:201-TA1 TA1- 8T
UID:CLC1ATCTKM5-2025-08-11-09:35@kma.schedule
END:VEVENT
```

## Khắc phục sự cố

### Các vấn đề thường gặp

1. **"Could not find schedule table in HTML file" (Không thể tìm thấy bảng thời khóa biểu trong file HTML)**
   - Đảm bảo bạn đã sao chép HTML từ trang đúng (sau khi đăng nhập)
   - Xác minh rằng thời khóa biểu của bạn hiển thị trên trang web trước khi sao chép mã nguồn
   - Kiểm tra rằng bạn đã chọn học kỳ và đợt học đúng

2. **"No events generated" (Không tạo được sự kiện) hoặc lịch trống**
   - Đảm bảo file HTML của bạn chứa dữ liệu thời khóa biểu thực tế
   - Xác minh ngày tháng học kỳ hiện tại và không phải từ kỳ trước
   - Kiểm tra xem việc đăng ký môn học đã hoàn thành chưa

3. **Vấn đề truy cập cổng thông tin**
   - URL cổng thông tin KMA: http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Reports/Form/StudentTimeTable.aspx
   - Đảm bảo bạn có thông tin đăng nhập sinh viên KMA hợp lệ
   - Thử truy cập cổng thông tin từ mạng của trường nếu truy cập từ bên ngoài bị hạn chế

4. **Vấn đề mã hóa**
   - Lưu file HTML của bạn với mã hóa UTF-8 để bảo toàn ký tự tiếng Việt
   - Nếu bạn thấy text bị lỗi, hãy thử sao chép mã nguồn lại

### Nhận trợ giúp

Nếu bạn gặp vấn đề:
1. Kiểm tra file HTML của bạn có chứa dữ liệu bảng với thông tin môn học
2. Xác minh kích thước file hợp lý (nên có vài KB, không chỉ vài byte)
3. Thử trình phân tích với file ví dụ được cung cấp trước để đảm bảo nó hoạt động

## Tùy chỉnh

Để thích ứng với các trường khác hoặc định dạng khác:

1. Cập nhật `day_mapping` cho tên ngày khác
2. Sửa đổi `time_slots` cho khoảng thời gian khác
3. Điều chỉnh logic phân tích HTML trong `parse_html_file()` cho cấu trúc bảng khác
4. Cập nhật mẫu regex trong `parse_time_info()` cho định dạng ngày/giờ khác

## Giấy phép

[LICENSE](LICENSE)
