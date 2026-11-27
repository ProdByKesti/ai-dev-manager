use tauri::{webview::NewWindowResponse, WebviewUrl, WebviewWindowBuilder};

#[tauri::command]
fn get_foundation_status() -> &'static str {
    "Desktop foundation bridge is available."
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_foundation_status])
        .setup(|app| {
            WebviewWindowBuilder::new(app, "main", WebviewUrl::App("index.html".into()))
                .title("AI Dev Manager")
                .inner_size(880.0, 600.0)
                .min_inner_size(480.0, 360.0)
                .on_navigation(|url| {
                    let local_origin = if cfg!(windows) {
                        url.scheme() == "http" && url.host_str() == Some("tauri.localhost")
                    } else {
                        url.scheme() == "tauri" && url.host_str() == Some("localhost")
                    };
                    local_origin
                        && url.port().is_none()
                        && url.username().is_empty()
                        && url.password().is_none()
                })
                .on_new_window(|_, _| NewWindowResponse::Deny)
                .build()?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("failed to run desktop application");
}
