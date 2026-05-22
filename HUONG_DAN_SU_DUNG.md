# HƯỚNG DẪN SỬ DỤNG CHI TIẾT – Python Converter v2.3.0

**Mục đích:** Chuyển đổi Java Resource Pack sang Bedrock Edition, hỗ trợ ItemsAdder (contents + storage), tự động kiểm tra và sửa lỗi pack.

---

## 1. CÀI ĐẶT

### 1.1. Cài Python

- Tải Python 3.8+ từ [python.org](https://python.org)
- **Quan trọng:** Trong quá trình cài, chọn **"Add Python to PATH"**

### 1.2. Cài thư viện

Mở **Command Prompt** hoặc **PowerShell** và chạy:

```bash
python -m pip install pyyaml pillow
```

Hoặc:

```bash
pip install pyyaml pillow
```

### 1.3. Kiểm tra cài đặt

```bash
python -c "import yaml, PIL; print('✅ Thành công')"
```

Nếu không có lỗi, bạn đã sẵn sàng.

---

## 2. CHUẨN BỊ DỮ LIỆU

### 2.1. Java Resource Pack thông thường

Thư mục pack cần có cấu trúc tối thiểu:

```
MyPack/
├── pack.mcmeta
├── pack.png              (không bắt buộc)
└── assets/
    └── minecraft/
        ├── models/item/          # file .json (overrides)
        ├── textures/item/        # texture .png
        ├── textures/models/armor/ # armor layer
        └── sounds.json           # nếu có
```

### 2.2. Tích hợp ItemsAdder (nếu dùng)

Bạn cần có thư mục `contents` của ItemsAdder (thường nằm trong `plugins/ItemsAdder/contents`). Cấu trúc bên trong:

```
contents/
└── ten_namespace/                # ví dụ: "my_items"
    ├── configs/                  # file .yml (items, blocks, fonts, cosmetics)
    │   ├── items.yml
    │   ├── blocks.yml
    │   └── fonts.yml
    └── resourcepack/
        └── assets/
            └── ten_namespace/    # cùng tên namespace
                ├── textures/items/
                ├── textures/blocks/
                ├── textures/font/
                └── models/
```

> **Lưu ý:** Nếu có thư mục `storage` (chứa font images bổ sung), bạn cũng có thể cung cấp đường dẫn.

---

## 3. CHẠY CONVERTER

### 3.1. Chế độ tương tác (khuyến nghị)

```bash
python converter.py
```

Lần lượt nhập:

1. **Đường dẫn Java Resource Pack**
   Ví dụ: `C:\Users\Admin\Desktop\MyPack` hoặc `./MyPack`

2. **Đường dẫn output**
   Mặc định: `./bedrock_packs_v2` – nơi tạo thư mục pack Bedrock.

3. **Tên pack**
   Không dấu cách, ví dụ: `my_awesome_pack`

4. **Đường dẫn đến thư mục `contents` của ItemsAdder**
   - Nếu có: nhập đường dẫn tuyệt đối (ví dụ `C:\server\plugins\ItemsAdder\contents`). Script sẽ kiểm tra cấu trúc và yêu cầu nhập lại nếu sai.
   - Nếu không: nhấn **Enter** để bỏ qua.

5. **Đường dẫn đến thư mục `storage`** (tùy chọn)
   Nhập hoặc để trống.

Sau đó, bạn sẽ được hỏi các tùy chọn nâng cao (mapping V3/V4, animation, cosmetics, log chi tiết). Trả lời bằng số hoặc `Y/N`.

### 3.2. Chế độ dòng lệnh (batch)

```bash
python converter.py "D:\MyPack" "./bedrock_output" "pack_name"
```

Ba tham số đầu tiên, các tham số còn lại (`contents`, `storage`) sẽ không được hỏi – bạn phải sửa trực tiếp trong script hoặc dùng chế độ tương tác.

---

## 4. GIẢI THÍCH CÁC TÙY CHỌN

| Tùy chọn | Giá trị | Ý nghĩa |
|---|---|---|
| GeyserMC Mappings | V3 / V4 | V3 ổn định; V4 thử nghiệm, hỗ trợ components, NBT. |
| Animation frames | Y / N | Bật/tạo `flipbook_textures.json` từ file `.png.mcmeta`. |
| Cosmetics | Y / N | Chuyển mũ, wings, particle từ ItemsAdder sang attachables. |
| Log chi tiết | Y / N | In thông tin từng file, mỗi bước nhỏ. |

---

## 5. KẾT QUẢ ĐẦU RA

Sau khi chạy thành công, thư mục output sẽ có cấu trúc:

```
bedrock_packs_v2/
└── my_awesome_pack/
    ├── manifest.json              # Bedrock pack metadata
    ├── custom_mappings.json       # GeyserMC mappings (V3 hoặc V4)
    ├── blocks.json                # Định nghĩa block custom
    ├── sound_definitions.json     # Âm thanh
    ├── attachables/               # File .json cho armor, weapons, cosmetics
    ├── textures/
    │   ├── items/                 # Textures item
    │   ├── blocks/                # Textures block
    │   └── font/                  # Font/emoji PNG
    ├── sounds/                    # Các file .ogg
    ├── font/                      # Định nghĩa font Bedrock
    └── CONVERSION_REPORT.txt      # Báo cáo tóm tắt
```

---

## 6. KIỂM TRA VÀ SỬA LỖI TỰ ĐỘNG

Trong quá trình chạy, `PackValidator` sẽ tự động:

- Tạo thư mục `assets/minecraft` nếu thiếu.
- Tạo `pack.mcmeta` mặc định với `pack_format: 15` (phù hợp Java 1.21).
- Sửa đường dẫn texture trong các file `.json` – thêm đuôi `.png` nếu quên.
- Xóa các thư mục rỗng.
- Phát hiện file JSON lỗi cú pháp → tạo bản sao `.bak` và báo lỗi.

Tất cả các thay đổi đều được ghi lại trong log.

---

## 7. TRIỂN KHAI LÊN GEYSERMC

1. Copy toàn bộ thư mục pack (ví dụ `my_awesome_pack`) vào thư mục `plugins/Geyser-Spigot/packs/` trên máy chủ Minecraft.

2. Reload Geyser bằng lệnh trong console server:
   ```
   /geyser reload
   ```

3. Kết nối từ Bedrock client (phone, PC Windows 10/11, console). Pack sẽ tự động tải về lần đầu kết nối.

4. Kiểm tra log Geyser để chắc chắn không có lỗi:
   ```
   [Geyser] Loading custom resource pack: my_awesome_pack
   [Geyser] Loaded 45 custom mappings.
   ```

---

## 8. XỬ LÝ SỰ CỐ

### `pip` không được nhận diện

**Nguyên nhân:** Python chưa được thêm vào PATH.

**Khắc phục:** Dùng `python -m pip install ...` hoặc cài lại Python, chọn "Add to PATH".

### `KeyError: 'items'` hoặc `KeyError: 'blocks'`

**Nguyên nhân:** Phiên bản script cũ (trước 2.3.0) không xử lý dict ItemsAdder đúng.

**Khắc phục:** Tải lại script phiên bản 2.3.0 từ repository.

### Không tìm thấy contents hợp lệ

**Nguyên nhân:** Đường dẫn đến `contents` không tồn tại hoặc thiếu thư mục `resourcepack/assets` bên trong namespace.

**Khắc phục:** Kiểm tra lại đường dẫn. Ví dụ đúng: `C:\server\plugins\ItemsAdder\contents` – bên trong phải có thư mục con chứa `resourcepack`.

### Pack Bedrock không load trong Geyser

**Nguyên nhân:** `manifest.json` lỗi (thiếu UUID, sai format), hoặc thư mục pack không được đặt đúng chỗ.

**Khắc phục:** Xóa thư mục pack cũ trong `packs/`, chạy lại converter. Nếu vẫn lỗi, mở `manifest.json` kiểm tra cú pháp JSON.

### Font bị lệch, icon không hiển thị

**Nguyên nhân:** Không có cấu hình glyph chính xác (do thiếu file font config từ ItemsAdder hoặc Pillow không hoạt động).

**Khắc phục:** Cài Pillow (`pip install pillow`) và chạy lại – script sẽ tự động quét glyph. Nếu vẫn lỗi, chỉnh sửa thủ công file `font/*.json` trong Bedrock pack.

### Lỗi YAML khi parse ItemsAdder

**Nguyên nhân:** File `.yml` trong `configs/` bị sai cú pháp (thiếu dấu cách, sai indent).

**Khắc phục:** Mở file bằng editor hỗ trợ YAML (VS Code, Notepad++) và sửa lỗi.

---

## 9. CÂU HỎI THƯỜNG GẶP

**Hỏi: Tôi có cần ItemsAdder không?**

Không. Script vẫn hoạt động với Java pack thuần túy. ItemsAdder chỉ là tính năng bổ sung.

**Hỏi: Tại sao pack output lại có thư mục `font/` và `textures/font/`?**

Bedrock cần cả font texture (`.png`) và định nghĩa glyph (`.json`). `textures/font/` chứa ảnh, `font/` chứa file cấu hình.

**Hỏi: Làm sao để chạy nhiều pack cùng lúc?**

Viết script batch (`.bat` hoặc `.sh`) lặp lại lệnh `python converter.py` với các tham số khác nhau. Hoặc dùng chế độ dòng lệnh.

**Hỏi: Có hỗ trợ 3D model từ ModelEngine không?**

Phiên bản Python 2.3.0 hỗ trợ cơ bản (parse entity, tạo geometry/animations). Để đầy đủ, cần mở rộng thêm.

---

## 10. LIÊN HỆ & HỖ TRỢ

- **GitHub Issues:** https://github.com/your-repo/mc-converter-python/issues
- **Email:** support@example.com
- **Wiki ItemsAdder:** http://thunder.pikamc.vn:25164/wiki/#itemsadder
