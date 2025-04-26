import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mini_aes import str_to_nibbles, nibbles_to_str, encrypt

def flip_bit(hex_str, position):
    # Konversi hex string ke bit string
    bit_string = ""
    for c in hex_str:
        # Konversi setiap karakter hex ke 4 bit
        bits = bin(int(c, 16))[2:].zfill(4)
        bit_string += bits
    
    # Flip bit pada posisi yang ditentukan
    bit_list = list(bit_string)
    bit_list[position] = '1' if bit_list[position] == '0' else '0'
    new_bit_string = ''.join(bit_list)
    
    # Konversi kembali ke hex string
    new_hex = ""
    for i in range(0, len(new_bit_string), 4):
        nibble = new_bit_string[i:i+4]
        hex_char = hex(int(nibble, 2))[2:]
        new_hex += hex_char
    
    return new_hex.upper()

def count_bit_differences(str1, str2):
    # Konversi ke bit string
    bits1 = ''.join([bin(int(c, 16))[2:].zfill(4) for c in str1])
    bits2 = ''.join([bin(int(c, 16))[2:].zfill(4) for c in str2])
    
    # Hitung perbedaan
    differences = sum(b1 != b2 for b1, b2 in zip(bits1, bits2))
    return differences, len(bits1)

def analyze_plaintext_avalanche(plaintext, key):
    results = []
    pt_nibbles = str_to_nibbles(plaintext)
    key_nibbles = str_to_nibbles(key)
    
    # Enkripsi plaintext asli
    original_ciphertext = nibbles_to_str(encrypt(pt_nibbles, key_nibbles))
    
    for bit_pos in range(16):  # 16 bit dalam 4 hex digit
        # Flip satu bit pada plaintext
        modified_pt = flip_bit(plaintext, bit_pos)
        mod_pt_nibbles = str_to_nibbles(modified_pt)
        
        # Enkripsi plaintext yang dimodifikasi
        modified_ciphertext = nibbles_to_str(encrypt(mod_pt_nibbles, key_nibbles))
        
        # Hitung perbedaan bit
        diff, total_bits = count_bit_differences(original_ciphertext, modified_ciphertext)
        
        results.append((bit_pos, diff, diff/total_bits * 100))
    
    return results, original_ciphertext

def analyze_key_avalanche(plaintext, key):
    results = []
    pt_nibbles = str_to_nibbles(plaintext)
    key_nibbles = str_to_nibbles(key)
    
    # Enkripsi dengan key asli
    original_ciphertext = nibbles_to_str(encrypt(pt_nibbles, key_nibbles))
    
    for bit_pos in range(16):  # 16 bit dalam 4 hex digit
        # Flip satu bit pada key
        modified_key = flip_bit(key, bit_pos)
        mod_key_nibbles = str_to_nibbles(modified_key)
        
        # Enkripsi dengan key yang dimodifikasi
        modified_ciphertext = nibbles_to_str(encrypt(pt_nibbles, mod_key_nibbles))
        
        # Hitung perbedaan bit
        diff, total_bits = count_bit_differences(original_ciphertext, modified_ciphertext)
        
        results.append((bit_pos, diff, diff/total_bits * 100))
    
    return results, original_ciphertext

class AvalancheAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-AES Avalanche Effect Analyzer")
        self.root.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Plaintext input
        ttk.Label(input_frame, text="Plaintext (4 hex digits):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.plaintext_var = tk.StringVar(value="1234")
        plaintext_entry = ttk.Entry(input_frame, textvariable=self.plaintext_var, width=20)
        plaintext_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Key input
        ttk.Label(input_frame, text="Key (4 hex digits):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.key_var = tk.StringVar(value="5678")
        key_entry = ttk.Entry(input_frame, textvariable=self.key_var, width=20)
        key_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Analysis type
        ttk.Label(input_frame, text="Analyze:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.analysis_type = tk.StringVar(value="plaintext")
        plaintext_radio = ttk.Radiobutton(input_frame, text="Plaintext Changes", variable=self.analysis_type, value="plaintext")
        plaintext_radio.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        key_radio = ttk.Radiobutton(input_frame, text="Key Changes", variable=self.analysis_type, value="key")
        key_radio.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Analyze button
        analyze_btn = ttk.Button(input_frame, text="Analyze Avalanche Effect", command=self.perform_analysis)
        analyze_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Results section - Notebook with tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab for text results
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="Text Results")
        
        # Result text area
        self.result_text = scrolledtext.ScrolledText(text_frame, width=70, height=15, font=("Courier", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab for graph
        graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(graph_frame, text="Graph")
        
        # Matplotlib figure for graph
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def perform_analysis(self):
        try:
            # Dapatkan input
            plaintext = self.plaintext_var.get().upper()
            key = self.key_var.get().upper()
            
            # Validasi input
            if not (len(plaintext) == 4 and len(key) == 4):
                self.status_var.set("Error: Plaintext dan Key harus tepat 4 digit hex")
                return
            
            if not (all(c in "0123456789ABCDEF" for c in plaintext) and 
                    all(c in "0123456789ABCDEF" for c in key)):
                self.status_var.set("Error: Input hex tidak valid")
                return
            
            # Hapus hasil sebelumnya
            self.result_text.delete(1.0, tk.END)
            self.ax.clear()
            
            # Jalankan analisis
            if self.analysis_type.get() == "plaintext":
                results, original_ct = analyze_plaintext_avalanche(plaintext, key)
                target = "plaintext"
            else:
                results, original_ct = analyze_key_avalanche(plaintext, key)
                target = "key"
            
            # Tampilkan header
            self.result_text.insert(tk.END, f"Analisis Avalanche Effect pada {target.capitalize()}\n")
            self.result_text.insert(tk.END, f"{'='*50}\n\n")
            self.result_text.insert(tk.END, f"Plaintext: {plaintext}\n")
            self.result_text.insert(tk.END, f"Key: {key}\n")
            self.result_text.insert(tk.END, f"Ciphertext Awal: {original_ct}\n\n")
            
            # Tampilkan hasil dalam tabel
            self.result_text.insert(tk.END, f"{'Bit Position':<15}{'Bit yang Berubah':<20}{'Persentase':<15}\n")
            self.result_text.insert(tk.END, f"{'-'*50}\n")
            
            bit_positions = []
            bit_differences = []
            percentages = []
            
            for bit_pos, diff, percentage in results:
                self.result_text.insert(tk.END, f"{bit_pos:<15}{diff:<20}{percentage:.2f}%\n")
                bit_positions.append(bit_pos)
                bit_differences.append(diff)
                percentages.append(percentage)
            
            # Hitung rata-rata
            avg_diff = sum(bit_differences) / len(bit_differences)
            avg_percentage = sum(percentages) / len(percentages)
            
            self.result_text.insert(tk.END, f"\nRata-rata bit yang berubah: {avg_diff:.2f}\n")
            self.result_text.insert(tk.END, f"Rata-rata persentase perubahan: {avg_percentage:.2f}%\n")
            
            # Plot data
            self.ax.bar(bit_positions, percentages)
            self.ax.set_xlabel('Posisi Bit')
            self.ax.set_ylabel('Persentase Bit yang Berubah (%)')
            self.ax.set_title(f'Avalanche Effect - Perubahan pada {target.capitalize()}')
            self.ax.axhline(y=avg_percentage, color='r', linestyle='-', label=f'Rata-rata: {avg_percentage:.2f}%')
            self.ax.legend()
            
            # Tampilkan plot
            self.canvas.draw()
            
            # Switch to graph tab
            self.notebook.select(1)
            
            self.status_var.set(f"Analisis avalanche effect selesai. Rata-rata perubahan: {avg_percentage:.2f}%")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Terjadi error: {str(e)}\n\nSilakan periksa input Anda.")

def main():
    root = tk.Tk()
    app = AvalancheAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 