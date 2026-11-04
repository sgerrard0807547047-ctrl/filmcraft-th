//! Brand artwork is omitted from this locally modified build (AGENTS.md §1.8).

/// Localized builds do not embed the ArtCraft trademark artwork.
pub fn wordmark(_ctx: &egui::Context, _dark: bool) -> Option<egui::TextureHandle> {
    None
}

/// Draw the wordmark `height` points tall with its left edge at `left_center` (vertically centred).
/// Returns the drawn rect.
pub fn paint_wordmark(ui: &egui::Ui, left_center: egui::Pos2, height: f32, dark: bool) -> Option<egui::Rect> {
    let tex = wordmark(ui.ctx(), dark)?;
    let [w, h] = tex.size();
    let width = height * w as f32 / h.max(1) as f32;
    let r = egui::Rect::from_min_size(egui::pos2(left_center.x, left_center.y - height / 2.0), egui::vec2(width, height));
    ui.painter().image(tex.id(), r, egui::Rect::from_min_max(egui::pos2(0.0, 0.0), egui::pos2(1.0, 1.0)), egui::Color32::WHITE);
    Some(r)
}
