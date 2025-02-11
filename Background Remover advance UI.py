import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from rembg import remove
import multiprocessing
import queue
import threading

class BackgroundRemoverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Background Remover")
        self.master.geometry("600x700")
        self.master.configure(bg='#f0f0f0')

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Create tabs
        self.batch_frame = ttk.Frame(self.notebook)
        self.single_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.batch_frame, text='Batch Processing')
        self.notebook.add(self.single_frame, text='Single Image')

        # Initialize both interfaces
        self.setup_batch_interface()
        self.setup_single_interface()

        # Queue and Threading Setup
        self.log_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        # Start log processing thread
        self.log_thread = threading.Thread(target=self.process_log_queue, daemon=True)
        self.log_thread.start()

    def setup_single_interface(self):
        # Input File Section
        input_label = tk.Label(self.single_frame, text="Input Image:")
        input_label.pack(anchor='w', pady=(10,0))
        
        self.input_file_var = tk.StringVar()
        input_entry = tk.Entry(self.single_frame, textvariable=self.input_file_var, width=70)
        input_entry.pack(fill=tk.X, pady=5)
        
        input_browse_btn = tk.Button(self.single_frame, text="Browse", command=self.select_input_file)
        input_browse_btn.pack(anchor='w', pady=5)

        # Output File Section
        output_label = tk.Label(self.single_frame, text="Output Image:")
        output_label.pack(anchor='w', pady=(10,0))
        
        self.output_file_var = tk.StringVar()
        output_entry = tk.Entry(self.single_frame, textvariable=self.output_file_var, width=70)
        output_entry.pack(fill=tk.X, pady=5)
        
        output_browse_btn = tk.Button(self.single_frame, text="Browse", command=self.select_output_file)
        output_browse_btn.pack(anchor='w', pady=5)

        # Process Button
        process_btn = tk.Button(self.single_frame, text="Remove Background", command=self.process_single_image)
        process_btn.pack(pady=20)

        # Preview Labels
        self.input_preview_label = tk.Label(self.single_frame, text="Input Preview")
        self.input_preview_label.pack()
        self.output_preview_label = tk.Label(self.single_frame, text="Output Preview")
        self.output_preview_label.pack()

    def setup_batch_interface(self):
        # Input Directory Section
        input_label = tk.Label(self.batch_frame, text="Input Directory:")
        input_label.pack(anchor='w', pady=(10,0))
        
        self.input_dir_var = tk.StringVar()
        input_entry = tk.Entry(self.batch_frame, textvariable=self.input_dir_var, width=70)
        input_entry.pack(fill=tk.X, pady=5)
        
        input_browse_btn = tk.Button(self.batch_frame, text="Browse", command=self.select_input_directory)
        input_browse_btn.pack(anchor='w', pady=5)

        # Output Directory Section
        output_label = tk.Label(self.batch_frame, text="Output Directory:")
        output_label.pack(anchor='w', pady=(10,0))
        
        self.output_dir_var = tk.StringVar()
        output_entry = tk.Entry(self.batch_frame, textvariable=self.output_dir_var, width=70)
        output_entry.pack(fill=tk.X, pady=5)
        
        output_browse_btn = tk.Button(self.batch_frame, text="Browse", command=self.select_output_directory)
        output_browse_btn.pack(anchor='w', pady=5)

        # Progress Section
        self.progress_label = tk.Label(self.batch_frame, text="")
        self.progress_label.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(self.batch_frame, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Process Button
        process_btn = tk.Button(self.batch_frame, text="Remove Backgrounds", command=self.start_batch_processing)
        process_btn.pack(pady=20)

        # Log Section
        log_label = tk.Label(self.batch_frame, text="Processing Log:")
        log_label.pack(anchor='w')
        
        self.log_text = tk.Text(self.batch_frame, height=10, width=70)
        self.log_text.pack(pady=10)

    def select_input_file(self):
        """Select single input file"""
        filetypes = (
            ('Image files', '*.jpg *.jpeg *.png *.webp'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_file_var.set(filename)

    def select_output_file(self):
        """Select single output file"""
        filetypes = (
            ('PNG files', '*.png'),
            ('All files', '*.*')
        )
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
        if filename:
            self.output_file_var.set(filename)

    def process_single_image(self):
        """Process a single image"""
        input_path = self.input_file_var.get()
        output_path = self.output_file_var.get()

        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select input and output files")
            return

        try:
            # Process the image
            input_image = Image.open(input_path)
            output_image = remove(input_image)
            output_image.save(output_path)
            
            messagebox.showinfo("Success", "Background removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")

    def process_log_queue(self):
        """Process log messages from the queue"""
        while not self.stop_event.is_set():
            try:
                message = self.log_queue.get(timeout=0.1)
                self.master.after(0, self.update_log, message)
            except queue.Empty:
                continue

    def update_log(self, message):
        """Update log text widget (called from main thread)"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def select_input_directory(self):
        """Select input directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir_var.set(directory)

    def select_output_directory(self):
        """Select output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)

    @staticmethod
    def remove_background_single(input_path, output_path):
        """Static method for background removal to avoid pickling issues"""
        try:
            input_image = Image.open(input_path)
            output_image = remove(input_image)
            output_image.save(output_path)
            return True
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return False

    def start_batch_processing(self):
        """Start batch background removal process"""
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()

        # Validate directories
        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select input and output directories")
            return

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Find image files
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]

        if not image_files:
            messagebox.showinfo("Info", "No images found in the input directory")
            return

        # Reset progress
        self.progress_bar["maximum"] = len(image_files)
        self.progress_bar["value"] = 0
        self.progress_label.config(text=f"Processing {len(image_files)} images...")
        self.log_text.delete(1.0, tk.END)

        # Process images
        successful = 0
        failed = 0

        for index, filename in enumerate(image_files):
            try:
                input_path = os.path.join(input_dir, filename)
                output_filename = os.path.splitext(filename)[0] + "_processed.png"
                output_path = os.path.join(output_dir, output_filename)

                if self.remove_background_single(input_path, output_path):
                    successful += 1
                    self.log_queue.put(f"Processed: {filename}")
                else:
                    failed += 1
                    self.log_queue.put(f"Failed: {filename}")

                # Update progress
                self.master.after(0, self.update_progress, index + 1)
            except Exception as e:
                self.log_queue.put(f"Error processing {filename}: {str(e)}")
                failed += 1

        # Show completion message
        messagebox.showinfo("Complete", 
                          f"Processing complete.\nSuccessful: {successful}\nFailed: {failed}")
        
        self.progress_label.config(text="Processing Complete")

    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar["value"] = value

def main():
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
