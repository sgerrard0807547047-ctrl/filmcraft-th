# FilmCraft TH สำหรับ Windows 11 / 10 (x64)

โฟลเดอร์นี้บรรจุแพ็กเกจติดตั้ง สคริปต์สร้างแพ็กเกจ และสคริปต์ทดสอบของ **FilmCraft TH รุ่น 0.17.0-th.1** สำหรับระบบปฏิบัติการ **Windows 11 / 10 (64-bit)**

---

## ไฟล์แพ็กเกจพร้อมใช้งาน

| ไฟล์ | ประเภท | ขนาด | SHA-256 |
|---|---|---|---|
| [FilmCraft-TH-0.17.0-th.1-windows-x64.msi](FilmCraft-TH-0.17.0-th.1-windows-x64.msi) | Windows Installer (`.msi`) | ~34.5 MB | `45e9df8fa92a6418c978f0e3b56354ee3084ab51069aa535b1126abd04ef9afd` |
| [FilmCraft-TH-0.17.0-th.1-windows-x64-portable.zip](FilmCraft-TH-0.17.0-th.1-windows-x64-portable.zip) | Portable (`.zip`) ไม่ต้องติดตั้ง | ~43.6 MB | `c6dcb2aeae38513890e9463996fc85ae3e82525f8b8bfeda818fd76337c879b3` |
| [SHA256SUMS.txt](SHA256SUMS.txt) | ไฟล์ตรวจสอบค่า Hash SHA-256 | - | - |

---

## วิธีติดตั้งและเริ่มต้นใช้งานบน Windows 11

### วิธีที่ 1: แบบติดตั้งมาตรฐาน (`.msi`)
1. ดาวน์โหลดและดับเบิลคลิกไฟล์ `FilmCraft-TH-0.17.0-th.1-windows-x64.msi`
2. ทำตามขั้นตอนตัวติดตั้ง (ค่าเริ่มต้นติดตั้งที่ `%LOCALAPPDATA%\Programs\ArtCraft\FilmCraft` หรือเลือกติดตั้งสำหรับผู้ใช้ทุกคน)
3. เปิดโปรแกรม **FilmCraft** จากเมนู Start
4. เลือกเมนู **Edit → Language → ไทย** (หรือ **แก้ไข → ภาษา → ไทย**) หรือตั้งค่าใน **Settings → General**

### วิธีที่ 2: แบบพกพา ไม่ต้องติดตั้ง (`Portable .zip`)
1. แตกไฟล์ `FilmCraft-TH-0.17.0-th.1-windows-x64-portable.zip` ไปยังโฟลเดอร์ที่ต้องการ
2. ดับเบิลคลิกเปิดไฟล์ `filmcraft.exe` ได้ทันที
3. ข้อมูลการตั้งค่า (`preferences.json`) และบันทึกการทำงานจะถูกเก็บแยกไว้ในโฟลเดอร์ `data/` ข้างไฟล์ `filmcraft.exe` (เนื่องจากมีไฟล์ `portable.txt` กำกับไว้)

---

## ตรวจสอบความถูกต้องของไฟล์ (SHA-256)

เปิด PowerShell ในโฟลเดอร์ `windows/` แล้วรันคำสั่ง:

```powershell
Get-FileHash .\FilmCraft-TH-0.17.0-th.1-windows-x64.msi, .\FilmCraft-TH-0.17.0-th.1-windows-x64-portable.zip -Algorithm SHA256
```

เปรียบเทียบค่าที่ได้กับไฟล์ [SHA256SUMS.txt](SHA256SUMS.txt)

---

## การรองรับบน Windows 11 ที่ตรวจสอบแล้ว

- **ฟอนต์ภาษาไทย**: ตรวจพบและใช้งานฟอนต์ระบบของ Windows 11 (`Leelawadee UI`, `Leelawadee`, `Tahoma`) อัตโนมัติครบทุกชุดตัวอักษรและวรรณยุกต์
- **กราฟิกและการถอดรหัสฮาร์ดแวร์**:
  - รองรับ **Vulkan** และ **DirectX 12** (ทดสอบบน NVIDIA GeForce RTX 5060 Laptop GPU และ AMD Radeon Graphics)
  - รองรับการถอดรหัสวิดีโอด้วยฮาร์ดแวร์ผ่าน **Windows Media Foundation**
- **ชุดคำแปลภาษาไทย**: แค็ตตาล็อกภาษาไทยครบ **3,763 รายการ** (`th.tsv`)

---

## สคริปต์สำหรับนักพัฒนาบน Windows

หากต้องการคอมไพล์และสร้างแพ็กเกจใหม่จากซอร์สโค้ดบน Windows 11:

```powershell
# 1. ตรวจสอบความสมบูรณ์ของแค็ตตาล็อกคำแปลภาษาไทย
python tools/thai/validate_catalog.py

# 2. รันชุดทดสอบระบบภาษาไทยและฟอนต์บน Windows
cargo test --release --locked -p filmcraft-ui-egui --lib i18n::tests

# 3. สร้างแพ็กเกจ .zip Portable และ .msi Installer
powershell -ExecutionPolicy Bypass -File windows/package_windows.ps1

# 4. รันการทดสอบเปิดแอปและจับภาพหน้าจออัตโนมัติ (Smoke Test)
python windows/smoke_windows.py
```
