# FilmCraft TH 0.17.1-th.1 — validation, 2026-11-05

Updated from upstream release `v0.17.1` (`2fe0d0460da86621fd8b193dcc0a61f790106200`), retaining all 3,763 Thai catalog entries. The direct upstream tree delta adds the OGG packet-list memory budget and tests, version metadata, and the Linux signing-key workflow input.

- `cargo xtask ci`: **passed** (fmt, workspace clippy, tests, doctests, layers, asset attribution, wasm for 49 crates). Test summaries report 4,695 passes, zero failures and 52 upstream ignored tests, including the localization-report invocation.
- `python3 tools/thai/validate_catalog.py`: 3,763 entries, zero missing union keys; placeholders and escapes checked.
- Release build passed. Isolated native smoke test passed for Thai menu selection, persisted preferences, demo project, and editing/settings/export screenshots; editing and export images inspected.
- Update checks point to `sgerrard0807547047-ctrl/filmcraft-th`. Prereleases should be downloaded directly from Releases.
- Native app, CLI and UI crate report `0.17.1-th.1`; engine/codec crates retain upstream `0.17.1`. Applying the Thai suffix to codec versions changed H.264 SEI length and rate-control decisions, failing the pinned-slice test in the initial run. Scoping the distribution version to the app/UI resolved this without changing codec algorithms or test expectations; the final full CI passed.
- macOS Apple Silicon package is ad-hoc signed, not Apple-notarized. This release was not manually tested on Windows/Linux.

รายงานรอบสุดท้ายผ่านครบ คำแปลไทย 3,763 รายการยังอยู่ครบ และทดสอบหน้าจอจริงด้วยโปรไฟล์แยก ไม่เปลี่ยนงานหรือการตั้งค่าของผู้ใช้

---

## Historical validation for 0.17.0-th.1

# ผลตรวจรุ่นภาษาไทย — 2026-11-04

ตรวจบน macOS Apple Silicon ด้วย commit ฐาน `c9be14245a6c9da585ff906a6e0ca9c8200652ea` และส่วนปรับแต่งภาษาไทยใน repository นี้

## ผ่าน

- สร้างแอป release และตรวจลายเซ็น ad-hoc ของแพ็กเกจ macOS
- ชุดทดสอบ i18n: 31 ผ่าน รวมการเลือก/บันทึกภาษา การค้นหา และฟอนต์ไทย
- แค็ตตาล็อกไทย: 3,763 รายการ ไม่มีคีย์จาก union ของแค็ตตาล็อกอื่นตกหล่น ตรวจ placeholders และ escape แล้ว
- `cargo fmt --check`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `cargo xtask layers`
- `cargo xtask assets`: 72 สินทรัพย์มี attribution
- `cargo xtask wasm`: 49 crates
- `cargo test --workspace --doc`
- เปิดแอปจริงด้วยข้อมูลทดสอบแยก: หน้าแก้ไข ตั้งค่า ส่งออก และตรวจว่าค่าภาษา `th` ถูกบันทึก
- ติดตั้งและเปิดแอปจริงบน Mac ที่ใช้พัฒนา เมนู native และหน้าตัดต่อแสดงภาษาไทย

## ผลชุดทดสอบเต็มและข้อจำกัด

รัน `cargo xtask ci` สองรอบ รอบแรกจบชุดทดสอบหลักด้วย 4,679 ผ่าน, 1 ไม่ผ่าน, 52 ถูกข้าม และรอบถัดมามี 4,678 ผ่าน, 1 ไม่ผ่าน, 52 ถูกข้าม โดยรายการที่ไม่ผ่านเป็นคนละรายการในโค้ดต้นฉบับที่งานนี้ไม่ได้แก้:

1. รอบแรก `avi_tests::damaged_video_index_entries_lose_no_pictures` อ่านไฟล์ fixture ไม่สำเร็จระหว่างการรันพร้อมกัน มีอีกการทดสอบใช้ชื่อไฟล์เดียวกัน เมื่อรันแยกรายการนี้ผ่าน และผ่านในรอบเต็มถัดมา
2. รอบถัดมา `hardware_encode::rate_conversion_and_cancel_then_export_again` พบจำนวนการ fallback ไป software encoder ไม่ตรงคาด (5 แทน 4) รายการนี้ผ่านในรอบแรก ตรวจชุด platform แยกโดยรันทีละรายการแล้วผ่านครบ 34 รายการ

ไม่ได้อ้างว่าคำสั่ง CI เต็มผ่านโดยไม่มีข้อผิดพลาด ผลของการตรวจแยกช่วยจำกัดความเสี่ยง แต่ไม่แทนการแก้ความไม่เสถียรในชุดทดสอบต้นฉบับ ไม่มีการเปลี่ยน codec หรือ engine เพื่อทำให้การทดสอบผ่าน

การมีคำแปลครบแค็ตตาล็อกไม่ได้หมายความว่าทดสอบทุกฟังก์ชันหรือทุกข้อความผิดพลาด คำแปลยังควรผ่านการตรวจภาษาจากผู้ใช้จริงเพิ่มเติม
