import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from pathlib import Path

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Master Image Converter")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Premium dark purple theme colors
        self.bg_dark = "#0a0a0f"
        self.bg_card = "#1a1a2e"
        self.purple_main = "#a855f7"
        self.purple_light = "#c084fc"
        self.purple_dark = "#7e22ce"
        self.purple_glow = "#e9d5ff"
        self.text_primary = "#f8fafc"
        self.text_secondary = "#94a3b8"
        self.accent = "#06b6d4"
        
        # Configure root
        self.root.configure(bg=self.bg_dark)
        
        # Supported formats
        self.formats = ['PNG', 'JPG', 'JPEG', 'BMP', 'GIF', 'TIFF', 'WEBP', 'ICO']
        
        # Create main frame with glow effect
        glow_frame = tk.Frame(root, bg=self.purple_main, padx=2, pady=2)
        glow_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        main_frame = tk.Frame(glow_frame, bg=self.bg_card, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(main_frame, bg=self.bg_card)
        title_frame.pack(pady=(0, 30))
        
        title_label = tk.Label(title_frame, text="MASTER IMAGE CONVERTER", 
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.bg_card, fg=self.purple_light)
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Premium Edition", 
                                 font=('Segoe UI', 10),
                                 bg=self.bg_card, fg=self.text_secondary)
        subtitle_label.pack()
        
        # Mode selection
        mode_frame = tk.Frame(main_frame, bg=self.bg_dark, padx=20, pady=15)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        mode_label = tk.Label(mode_frame, text="CONVERSION MODE", 
                             font=('Segoe UI', 9, 'bold'),
                             bg=self.bg_dark, fg=self.text_secondary)
        mode_label.pack(pady=(0, 10))
        
        radio_frame = tk.Frame(mode_frame, bg=self.bg_dark)
        radio_frame.pack()
        
        self.mode_var = tk.StringVar(value="single")
        
        single_radio = tk.Radiobutton(radio_frame, text="Single File", 
                                     variable=self.mode_var, value="single",
                                     command=self.update_mode,
                                     font=('Segoe UI', 11),
                                     bg=self.bg_dark, fg=self.text_primary,
                                     selectcolor=self.purple_dark,
                                     activebackground=self.bg_dark,
                                     activeforeground=self.purple_light,
                                     bd=0, highlightthickness=0)
        single_radio.pack(side=tk.LEFT, padx=20)
        
        batch_radio = tk.Radiobutton(radio_frame, text="Batch Mode", 
                                    variable=self.mode_var, value="batch",
                                    command=self.update_mode,
                                    font=('Segoe UI', 11),
                                    bg=self.bg_dark, fg=self.text_primary,
                                    selectcolor=self.purple_dark,
                                    activebackground=self.bg_dark,
                                    activeforeground=self.purple_light,
                                    bd=0, highlightthickness=0)
        batch_radio.pack(side=tk.LEFT, padx=20)
        
        # File selection area
        file_container = tk.Frame(main_frame, bg=self.bg_dark, padx=20, pady=20)
        file_container.pack(fill=tk.X, pady=(0, 20))
        
        self.file_label = tk.Label(file_container, text="No file selected", 
                                   font=('Segoe UI', 10),
                                   bg=self.bg_dark, fg=self.text_secondary,
                                   anchor='w')
        self.file_label.pack(fill=tk.X, pady=(0, 15))
        
        self.select_btn = tk.Button(file_container, text="📁 Select File", 
                                   command=self.select_file,
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.purple_dark, fg=self.text_primary,
                                   activebackground=self.purple_main,
                                   activeforeground=self.text_primary,
                                   bd=0, padx=20, pady=12,
                                   cursor='hand2',
                                   relief=tk.FLAT)
        self.select_btn.pack()
        self.select_btn.bind('<Enter>', lambda e: self.select_btn.config(bg=self.purple_main))
        self.select_btn.bind('<Leave>', lambda e: self.select_btn.config(bg=self.purple_dark))
        
        # Output format selection
        format_container = tk.Frame(main_frame, bg=self.bg_card, padx=20, pady=20)
        format_container.pack(fill=tk.X, pady=(0, 20))

        format_label = tk.Label(format_container, text="OUTPUT FORMAT",
                               font=('Segoe UI', 9, 'bold'),
                               bg=self.bg_card, fg=self.text_secondary)
        format_label.pack(pady=(0, 15))

        self.format_var = tk.StringVar(value='PNG')

        # Create format buttons grid
        format_buttons_frame = tk.Frame(format_container, bg=self.bg_card)
        format_buttons_frame.pack(pady=10)

        self.format_buttons = {}
        formats_layout = [
            ['PNG', 'JPG', 'JPEG', 'BMP'],
            ['GIF', 'TIFF', 'WEBP', 'ICO']
        ]

        for row_idx, row_formats in enumerate(formats_layout):
            for col_idx, fmt in enumerate(row_formats):
                btn = tk.Button(format_buttons_frame, text=fmt,
                              command=lambda f=fmt: self.select_format(f),
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.purple_dark, fg=self.text_primary,
                              activebackground=self.purple_main,
                              activeforeground=self.text_primary,
                              bd=0, padx=18, pady=10,
                              cursor='hand2',
                              relief=tk.RAISED,
                              width=6)
                btn.grid(row=row_idx, column=col_idx, padx=4, pady=4)
                self.format_buttons[fmt] = btn

                # Hover effects
                btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.purple_main))
                btn.bind('<Leave>', lambda e, b=btn, f=fmt: 
                        b.config(bg=self.purple_main if self.format_var.get() == f else self.purple_dark))

        # Highlight the default format
        self.format_buttons['PNG'].config(bg=self.purple_main, fg=self.text_primary)
        
        # Convert button with glow
        btn_glow_frame = tk.Frame(main_frame, bg=self.purple_glow, padx=2, pady=2)
        btn_glow_frame.pack(pady=(10, 15))
        
        self.convert_btn = tk.Button(btn_glow_frame, text="⚡ CONVERT NOW", 
                                    command=self.convert_images,
                                    state='disabled',
                                    font=('Segoe UI', 13, 'bold'),
                                    bg=self.bg_dark, fg=self.text_secondary,
                                    activebackground=self.purple_light,
                                    activeforeground=self.text_primary,
                                    bd=0, padx=40, pady=15,
                                    cursor='hand2',
                                    relief=tk.FLAT,
                                    disabledforeground=self.text_secondary)
        self.convert_btn.pack()
        self.convert_btn.bind('<Enter>', self.on_convert_hover)
        self.convert_btn.bind('<Leave>', self.on_convert_leave)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="", 
                                    font=('Segoe UI', 10),
                                    bg=self.bg_card, fg=self.accent)
        self.status_label.pack()
        
        # Store selected files
        self.selected_files = []
    
    def select_format(self, format_name):
        """Handle format button selection"""
        # Reset all buttons to default style
        for fmt, btn in self.format_buttons.items():
            btn.config(bg=self.purple_dark, fg=self.text_primary)
        
        # Highlight selected button
        self.format_buttons[format_name].config(bg=self.purple_main, fg=self.text_primary)
        self.format_var.set(format_name)
    
    def on_convert_hover(self, event):
        if self.convert_btn['state'] == 'normal':
            self.convert_btn.config(bg=self.purple_light)
    
    def on_convert_leave(self, event):
        if self.convert_btn['state'] == 'normal':
            self.convert_btn.config(bg=self.purple_main)
        
    def update_mode(self):
        mode = self.mode_var.get()
        if mode == "single":
            self.select_btn.config(text="📁 Select File")
        else:
            self.select_btn.config(text="📁 Select Files")
        self.file_label.config(text="No file selected", fg=self.text_secondary)
        self.selected_files = []
        self.convert_btn.config(state='disabled', bg=self.bg_dark)
        self.status_label.config(text="")
    
    def select_file(self):
        mode = self.mode_var.get()
        
        filetypes = [
            ('Image files', '*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp *.ico'),
            ('All files', '*.*')
        ]
        
        if mode == "single":
            filename = filedialog.askopenfilename(
                title="Select an image",
                filetypes=filetypes
            )
            if filename:
                self.selected_files = [filename]
                display_name = os.path.basename(filename)
                if len(display_name) > 50:
                    display_name = display_name[:47] + "..."
                self.file_label.config(text=f"✓ {display_name}", fg=self.purple_light)
                self.convert_btn.config(state='normal', bg=self.purple_main)
        else:
            filenames = filedialog.askopenfilenames(
                title="Select images",
                filetypes=filetypes
            )
            if filenames:
                self.selected_files = list(filenames)
                self.file_label.config(text=f"✓ {len(filenames)} files selected", fg=self.purple_light)
                self.convert_btn.config(state='normal', bg=self.purple_main)
    
    def convert_images(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select file(s) to convert.")
            return
        
        output_format = self.format_var.get().upper()
        mode = self.mode_var.get()
        
        # Disable button during conversion
        self.convert_btn.config(state='disabled', bg=self.bg_dark)
        self.status_label.config(text="⏳ Converting...", fg=self.purple_light)
        self.root.update()
        
        try:
            if mode == "single":
                self.convert_single_file(self.selected_files[0], output_format)
            else:
                self.convert_batch_files(self.selected_files, output_format)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="❌ Conversion failed!", fg="#ef4444")
        finally:
            self.convert_btn.config(state='normal', bg=self.purple_main)
    
    def convert_single_file(self, filepath, output_format):
        # Open image
        img = Image.open(filepath)
        
        # Convert RGBA to RGB if saving as JPEG
        if output_format in ['JPG', 'JPEG'] and img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Get output path
        file_path = Path(filepath)
        output_path = file_path.parent / f"{file_path.stem}.{output_format.lower()}"
        
        # Save image
        if output_format in ['JPG', 'JPEG']:
            img.save(output_path, 'JPEG', quality=95)
        else:
            img.save(output_path, output_format)
        
        self.status_label.config(text=f"✨ Converted successfully to {output_path.name}", 
                                fg=self.accent)
        messagebox.showinfo("Success", f"✓ Image converted successfully!\n\nSaved to:\n{output_path}")
    
    def convert_batch_files(self, filepaths, output_format):
        # Create output folder in the same directory as the first file
        first_file_dir = Path(filepaths[0]).parent
        output_folder = first_file_dir / f"converted_{output_format.lower()}"
        output_folder.mkdir(exist_ok=True)
        
        success_count = 0
        failed_files = []
        
        for i, filepath in enumerate(filepaths, 1):
            try:
                # Update status
                self.status_label.config(text=f"⏳ Converting {i}/{len(filepaths)}...", fg=self.purple_light)
                self.root.update()
                
                # Open image
                img = Image.open(filepath)
                
                # Convert RGBA to RGB if saving as JPEG
                if output_format in ['JPG', 'JPEG'] and img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Get output path
                file_path = Path(filepath)
                output_path = output_folder / f"{file_path.stem}.{output_format.lower()}"
                
                # Save image
                if output_format in ['JPG', 'JPEG']:
                    img.save(output_path, 'JPEG', quality=95)
                else:
                    img.save(output_path, output_format)
                
                success_count += 1
            except Exception as e:
                failed_files.append((os.path.basename(filepath), str(e)))
        
        # Show results
        result_msg = f"✓ Converted {success_count} out of {len(filepaths)} files.\n\n"
        result_msg += f"Output folder:\n{output_folder}"
        
        if failed_files:
            result_msg += f"\n\n❌ Failed files:\n"
            for filename, error in failed_files[:5]:  # Show first 5 errors
                result_msg += f"• {filename}: {error}\n"
        
        self.status_label.config(text=f"✨ Batch conversion complete: {success_count}/{len(filepaths)}", 
                                fg=self.accent)
        messagebox.showinfo("Batch Conversion Complete", result_msg)

def main():
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()