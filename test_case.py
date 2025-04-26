from mini_aes import encrypt, str_to_nibbles, nibbles_to_str

def run_test_cases():
    test_cases = [
        # Format: [plaintext, key, expected_ciphertext]
        ["1234", "5678", "910A"],  # Test case 1
        ["0000", "FFFF", "02FD"],  # Test case 2
        ["ABCD", "0123", "AB97"]   # Test case 3
    ]
    
    print("Mini-AES Test Cases")
    print("===================")
    
    for i, (pt, key, expected) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Plaintext: {pt}")
        print(f"Key: {key}")
        
        pt_nibbles = str_to_nibbles(pt)
        key_nibbles = str_to_nibbles(key)
        
        ciphertext = encrypt(pt_nibbles, key_nibbles)
        ct_str = nibbles_to_str(ciphertext)
        
        print(f"Generated Ciphertext: {ct_str}")
        
        if expected:
            if ct_str == expected:
                print("✓ Test passed!")
            else:
                print(f"✗ Test failed! Expected: {expected}")
        else:
            # For the first run, we'll just record the output
            print("(No expected ciphertext specified)")
    
    # Now update the expected values based on the first run
    # After running once, you can fill in the expected values
    
    # Additional example of showing the encryption process
    print("\nDetailed Encryption Process Example:")
    pt = "1234"
    key = "5678"
    print(f"Plaintext: {pt}")
    print(f"Key: {key}")
    
    pt_nibbles = str_to_nibbles(pt)
    key_nibbles = str_to_nibbles(key)
    
    # Run detailed process
    show_encryption_process(pt_nibbles, key_nibbles)

def show_encryption_process(plaintext, key):
    """Show the detailed encryption process"""
    from mini_aes import key_expansion, sub_nibbles, shift_rows, mix_columns, add_round_key
    
    # Generate round keys
    round_keys = key_expansion(key)
    
    print("\nRound Keys:")
    for i, rk in enumerate(round_keys):
        print(f"Round {i}: {nibbles_to_str(rk)}")
    
    # Initial state
    state = plaintext.copy()
    print(f"\nInitial state: {nibbles_to_str(state)}")
    
    # Initial AddRoundKey
    state = add_round_key(state, round_keys[0])
    print(f"After Initial AddRoundKey: {nibbles_to_str(state)}")
    
    # Round 1
    print("\nRound 1:")
    state = sub_nibbles(state)
    print(f"After SubNibbles: {nibbles_to_str(state)}")
    state = shift_rows(state)
    print(f"After ShiftRows: {nibbles_to_str(state)}")
    state = mix_columns(state)
    print(f"After MixColumns: {nibbles_to_str(state)}")
    state = add_round_key(state, round_keys[1])
    print(f"After AddRoundKey: {nibbles_to_str(state)}")
    
    # Round 2 (Final)
    print("\nRound 2 (Final):")
    state = sub_nibbles(state)
    print(f"After SubNibbles: {nibbles_to_str(state)}")
    state = shift_rows(state)
    print(f"After ShiftRows: {nibbles_to_str(state)}")
    state = add_round_key(state, round_keys[2])
    print(f"After AddRoundKey (Final): {nibbles_to_str(state)}")
    
    print(f"\nFinal Ciphertext: {nibbles_to_str(state)}")

if __name__ == "__main__":
    run_test_cases()
