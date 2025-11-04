import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import huffman
import adaptive_demo as adaptive
import os

# global variables
current_encoded = None
current_root = None
current_file = None

def open_file():
    global current_file
    file_path = filedialog.askopenfilename(
        title="Select Text File",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if not file_path:
        return
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)
    file_label.config(text=f"Loaded File: {os.path.basename(file_path)}")
    current_file = file_path

def compress_text():
    global current_encoded, current_root
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please load or enter text first!")
        return

    output_box.delete("1.0", tk.END)

    if adaptive_var.get() == 1:
        # run adaptive demo
        encoded, duration, steps = adaptive.adaptive_encode(text)
        output_box.insert(tk.END, "🔄 Adaptive Huffman Mode Enabled\n\n")
        output_box.insert(tk.END, f"Encoded Bits: {encoded}\n")
        output_box.insert(tk.END, f"Encoding Time: {round(duration,4)} sec\n\n")
        output_box.insert(tk.END, "Frequency & Code Evolution:\n")
        for i, freq, codes in steps[-5:]:   # show last 5 updates
            output_box.insert(tk.END, f"After {i} chars → {freq}\nCodes: {codes}\n---\n")
        messagebox.showinfo("Adaptive Mode", "Adaptive encoding demonstration completed!")
    else:
        # run normal static Huffman
        try:
            result = huffman.compress_text(text)
            current_encoded = result["encoded_text"]
            current_root = result["root"]

            output_box.insert(tk.END, f"✅ Static Compression Successful!\n\n")
            output_box.insert(tk.END, f"Original Size: {result['original_size']} bits\n")
            output_box.insert(tk.END, f"Compressed Size: {result['compressed_size']} bits\n")
            output_box.insert(tk.END, f"Compression Ratio: {result['ratio']}%\n")
            output_box.insert(tk.END, f"Encoding Time: {result['time']} sec\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

def save_compressed():
    global current_encoded, current_root
    if not current_encoded or not current_root:
        messagebox.showinfo("Info", "Please compress in Static Mode first!")
        return
    save_path = filedialog.asksaveasfilename(
        defaultextension=".huff",
        filetypes=(("Huffman Files", "*.huff"),)
    )
    if save_path:
        huffman.save_compressed(save_path, current_encoded, current_root)
        messagebox.showinfo("Success", f"File saved as {save_path}")

def decompress_file():
    file_path = filedialog.askopenfilename(
        title="Select Compressed File (.huff)",
        filetypes=(("Huffman Files", "*.huff"),)
    )
    if not file_path:
        return
    try:
        decoded = huffman.load_and_decompress(file_path)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, decoded)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "✅ Decompression Successful!\n")
        file_label.config(text=f"Decompressed: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decompress:\n{e}")

def clear_text():
    text_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    file_label.config(text="No file loaded.")

# ---------------- GUI Layout ----------------
root = tk.Tk()
root.title("Unicode Huffman Encoding - GUI")
root.geometry("880x700")
root.config(bg="#fce8e8")

title_label = tk.Label(root, text="🔤 Huffman Encoding for Indian Languages",
                       font=("Arial", 18, "bold"), bg="#fce8e8", fg="#800000")
title_label.pack(pady=10)

file_label = tk.Label(root, text="No file loaded.", bg="#fce8e8", fg="#333")
file_label.pack()

# checkbox for adaptive mode
adaptive_var = tk.IntVar()
adaptive_check = tk.Checkbutton(root, text="Enable Real-Time Adaptive Mode",
                                variable=adaptive_var, bg="#fce8e8", fg="#000",
                                font=("Arial", 10, "italic"))
adaptive_check.pack()

btn_frame = tk.Frame(root, bg="#fce8e8")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="📂 Open File", command=open_file, bg="#ffcccc", width=15).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="⚙️ Compress", command=compress_text, bg="#d4edda", width=15).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="💾 Save (Static)", command=save_compressed, bg="#cce5ff", width=15).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="📤 Decompress", command=decompress_file, bg="#ffeeba", width=15).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="🧹 Clear", command=clear_text, bg="#f8d7da", width=15).grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="❌ Exit", command=root.quit, bg="#e2e3e5", width=15).grid(row=0, column=5, padx=5)

tk.Label(root, text="Input / Decompressed Text:", bg="#fce8e8", fg="#000").pack(anchor="w", padx=15)
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=12)
text_box.pack(padx=15, pady=5)

tk.Label(root, text="Output:", bg="#fce8e8", fg="#000").pack(anchor="w", padx=15)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=12, fg="#004085")
output_box.pack(padx=15, pady=5)

root.mainloop()
