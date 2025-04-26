import tkinter as tk
from tkinter import ttk, scrolledtext
from mini_aes import str_to_nibbles, nibbles_to_str, encrypt, key_expansion

class MiniAESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-AES Encryption")
        self.root.geometry("650x550")
        
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
        
        # Encrypt button
        encrypt_btn = ttk.Button(input_frame, text="Encrypt", command=self.perform_encryption)
        encrypt_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Encryption Process", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Result output
        self.result_text = scrolledtext.ScrolledText(output_frame, width=70, height=20, font=("Courier", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def nibbles_to_hex_string(self, nibbles):
        return ''.join(f"{n:X}" for n in nibbles)
    
    def display_state(self, label, state):
        return f"{label}: {self.nibbles_to_hex_string(state)}"
    
    def perform_encryption(self):
        try:
            # Parse input
            plaintext_hex = self.plaintext_var.get().upper()
            key_hex = self.key_var.get().upper()
            
            # Validate input
            if not (len(plaintext_hex) == 4 and len(key_hex) == 4):
                self.status_var.set("Error: Plaintext and Key must be exactly 4 hex digits")
                return
            
            if not (all(c in "0123456789ABCDEF" for c in plaintext_hex) and 
                    all(c in "0123456789ABCDEF" for c in key_hex)):
                self.status_var.set("Error: Invalid hexadecimal input")
                return
            
            # Convert to nibbles
            pt_nibbles = str_to_nibbles(plaintext_hex)
            key_nibbles = str_to_nibbles(key_hex)
            
            # Generate round keys
            round_keys = key_expansion(key_nibbles)
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            
            # Display initial state
            self.result_text.insert(tk.END, f"Initial Plaintext: {plaintext_hex}\n")
            self.result_text.insert(tk.END, f"Initial Key: {key_hex}\n\n")
            
            # Display round keys
            self.result_text.insert(tk.END, "Round Keys:\n")
            for i, rk in enumerate(round_keys):
                self.result_text.insert(tk.END, f"Round {i}: {self.nibbles_to_hex_string(rk)}\n")
            self.result_text.insert(tk.END, "\n")
            
            # Encryption process
            self.result_text.insert(tk.END, "Encryption Process:\n")
            
            # Initial round - just AddRoundKey
            state = pt_nibbles.copy()
            self.result_text.insert(tk.END, f"Initial state: {self.nibbles_to_hex_string(state)}\n")
            
            state = [s ^ k for s, k in zip(state, round_keys[0])]
            self.result_text.insert(tk.END, f"After Initial AddRoundKey: {self.nibbles_to_hex_string(state)}\n\n")
            
            # Round 1
            self.result_text.insert(tk.END, "Round 1:\n")
            
            # SubNibbles
            state = [SBOX[n] for n in state]
            self.result_text.insert(tk.END, self.display_state("After SubNibbles", state) + "\n")
            
            # ShiftRows
            state = [state[0], state[3], state[2], state[1]]
            self.result_text.insert(tk.END, self.display_state("After ShiftRows", state) + "\n")
            
            # MixColumns
            state = [
                gf_mul(0x3, state[0]) ^ gf_mul(0x2, state[1]),
                gf_mul(0x2, state[0]) ^ gf_mul(0x3, state[1]),
                gf_mul(0x3, state[2]) ^ gf_mul(0x2, state[3]),
                gf_mul(0x2, state[2]) ^ gf_mul(0x3, state[3])
            ]
            self.result_text.insert(tk.END, self.display_state("After MixColumns", state) + "\n")
            
            # AddRoundKey
            state = [s ^ k for s, k in zip(state, round_keys[1])]
            self.result_text.insert(tk.END, self.display_state("After AddRoundKey", state) + "\n\n")
            
            # Round 2 (Final)
            self.result_text.insert(tk.END, "Round 2 (Final):\n")
            
            # SubNibbles
            state = [SBOX[n] for n in state]
            self.result_text.insert(tk.END, self.display_state("After SubNibbles", state) + "\n")
            
            # ShiftRows
            state = [state[0], state[3], state[2], state[1]]
            self.result_text.insert(tk.END, self.display_state("After ShiftRows", state) + "\n")
            
            # AddRoundKey (Final)
            state = [s ^ k for s, k in zip(state, round_keys[2])]
            self.result_text.insert(tk.END, self.display_state("After AddRoundKey (Final)", state) + "\n\n")
            
            # Final ciphertext
            ciphertext = self.nibbles_to_hex_string(state)
            self.result_text.insert(tk.END, f"Final Ciphertext: {ciphertext}")
            
            self.status_var.set(f"Encryption successful! {plaintext_hex} encrypted to {ciphertext}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"An error occurred: {str(e)}\n\nPlease check your input.")

# Import needed functions from mini_aes.py
from mini_aes import SBOX, gf_mul

def main():
    root = tk.Tk()
    app = MiniAESApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
