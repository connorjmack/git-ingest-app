import customtkinter as ctk
import gitingest
import asyncio
import threading
import multiprocessing  # <- ADDED THIS
import os
import sys
from datetime import datetime

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class IngestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GitIngest Pro")
        self.geometry("600x600") # Increased height for new UI elements
        self.resizable(False, False)

        # --- PATH SETUP ---
        # Determine the base path (handle both script and PyInstaller .app execution)
        if getattr(sys, 'frozen', False):
            # If running as a compiled app, default to Documents to avoid permission issues
            base_path = os.path.join(os.path.expanduser("~"), "Documents", "GitIngest_Output")
        else:
            # If running as a script, default to 'txt_files' inside the repo folder
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "txt_files")

        self.output_dir = base_path
        self.ensure_directory_exists(self.output_dir)

        # --- UI LAYOUT ---
        
        # 1. Header
        self.title_label = ctk.CTkLabel(self, text="GitIngest", font=("SF Pro Display", 28, "bold"))
        self.title_label.pack(pady=(25, 5))
        
        self.subtitle_label = ctk.CTkLabel(self, text="Turn GitHub repos into prompt-ready text files", font=("SF Pro Display", 14), text_color="gray70")
        self.subtitle_label.pack(pady=(0, 20))

        # 2. Input Section
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=40)
        
        self.url_label = ctk.CTkLabel(self.input_frame, text="Repository URL:", font=("Arial", 12, "bold"), anchor="w")
        self.url_label.pack(fill="x", pady=(0, 5))

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="https://github.com/user/repo", height=40, font=("Arial", 13))
        self.url_entry.pack(fill="x")

        # 3. Output Directory Selector (NEW)
        self.dir_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dir_frame.pack(fill="x", padx=40, pady=(15, 0))

        self.dir_label_title = ctk.CTkLabel(self.dir_frame, text="Save Location:", font=("Arial", 12, "bold"), anchor="w")
        self.dir_label_title.pack(fill="x", pady=(0, 5))

        self.dir_selector_layout = ctk.CTkFrame(self.dir_frame, fg_color="transparent")
        self.dir_selector_layout.pack(fill="x")

        self.dir_entry = ctk.CTkEntry(self.dir_selector_layout, placeholder_text=self.output_dir, height=35, font=("Arial", 11))
        self.dir_entry.insert(0, self.output_dir)
        self.dir_entry.configure(state="readonly") # User must use the button to change it
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.change_dir_btn = ctk.CTkButton(self.dir_selector_layout, text="Change Folder", width=100, height=35, command=self.change_directory)
        self.change_dir_btn.pack(side="right")

        # 4. Action Button
        self.ingest_button = ctk.CTkButton(self, text="Ingest Repository", font=("Arial", 14, "bold"), height=45, corner_radius=8, command=self.start_ingest_thread)
        self.ingest_button.pack(pady=25, padx=40, fill="x")

        # 5. Status & Output
        self.status_label = ctk.CTkLabel(self, text="Ready", font=("Arial", 12), text_color="gray60")
        self.status_label.pack(pady=(0, 5))

        self.path_result_entry = ctk.CTkEntry(self, placeholder_text="Output path will appear here...", state="readonly", font=("Courier", 12))
        self.path_result_entry.pack(pady=(0, 15), padx=40, fill="x")
        
        # 6. Button Row
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(0, 20), padx=40, fill="x")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.copy_path_btn = ctk.CTkButton(
            self.button_frame, text="Copy File Path", state="disabled", 
            fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), 
            command=self.copy_path_to_clipboard
        )
        self.copy_path_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.copy_content_btn = ctk.CTkButton(
            self.button_frame, text="Copy File Content", state="disabled", 
            fg_color="#2CC985", hover_color="#25A970", text_color="white",
            command=self.copy_content_to_clipboard
        )
        self.copy_content_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def ensure_directory_exists(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                self.log_status(f"Error creating directory: {e}", "red")

    def change_directory(self):
        new_dir = ctk.filedialog.askdirectory(initialdir=self.output_dir, title="Select Output Folder")
        if new_dir:
            self.output_dir = new_dir
            self.dir_entry.configure(state="normal")
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, self.output_dir)
            self.dir_entry.configure(state="readonly")

    def log_status(self, message, color="white"):
        if color == "green": color = "#2CC985"
        if color == "red": color = "#FF5555"
        if color == "yellow": color = "#F1C40F"
        self.status_label.configure(text=message, text_color=color)

    def success_ui(self, full_path):
        self.path_result_entry.configure(state="normal")
        self.path_result_entry.delete(0, "end")
        self.path_result_entry.insert(0, full_path)
        self.path_result_entry.configure(state="readonly")
        
        self.copy_path_btn.configure(state="normal")
        self.copy_content_btn.configure(state="normal")
        self.log_status("Success!", "green")
        self.ingest_button.configure(state="normal")
        self.change_dir_btn.configure(state="normal")

    def copy_path_to_clipboard(self):
        path = self.path_result_entry.get()
        if path:
            self.clipboard_clear()
            self.clipboard_append(path)
            self.update_idletasks()
            self.log_status("File path copied!", "green")

    def copy_content_to_clipboard(self):
        path = self.path_result_entry.get()
        if path and os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.clipboard_clear()
                self.clipboard_append(content)
                self.update_idletasks()
                self.log_status("File content copied to clipboard!", "green")
            except Exception as e:
                self.log_status(f"Error copying content: {e}", "red")

    def start_ingest_thread(self):
        repo_url = self.url_entry.get().strip()
        if not repo_url:
            self.log_status("Please enter a valid URL.", "red")
            return

        self.ingest_button.configure(state="disabled")
        self.copy_path_btn.configure(state="disabled")
        self.copy_content_btn.configure(state="disabled")
        self.change_dir_btn.configure(state="disabled")
        self.log_status("Cloning and processing... this may take a moment.", "yellow")
        
        thread = threading.Thread(target=self.run_async_ingest, args=(repo_url,))
        thread.start()

    def run_async_ingest(self, repo_url):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.perform_ingest(repo_url))
        finally:
            loop.close()

    async def perform_ingest(self, repo_url):
        try:
            # Check directory existence before starting (in case user deleted it manually)
            self.ensure_directory_exists(self.output_dir)

            summary, tree, content = await gitingest.ingest_async(source=repo_url)
            
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{repo_name}_{timestamp}.txt"
            full_path = os.path.join(self.output_dir, filename)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(f"SUMMARY:\n{summary}\n\nDIRECTORY TREE:\n{tree}\n\nFULL CONTENT:\n{content}")

            self.after(0, lambda: self.success_ui(full_path))
            
        except Exception as e:
            self.after(0, lambda: self.log_status(f"Error: {str(e)}", "red"))
            self.after(0, lambda: self.ingest_button.configure(state="normal"))
            self.after(0, lambda: self.change_dir_btn.configure(state="normal"))

if __name__ == "__main__":
    multiprocessing.freeze_support()  # <- ADDED THIS
    app = IngestApp()
    app.mainloop()