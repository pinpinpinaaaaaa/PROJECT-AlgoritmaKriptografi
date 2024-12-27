import math

# Cara mencari d
def find_private_key(e, m):
    k = 1
    while True:
        d = (1 + k * m) / e
        if d.is_integer():
            return int(d)
        k += 1

# Cara enkripsi per digit
def process_ascii_value(ascii_value, e, n):
    digits = [int(d) for d in str(ascii_value)]  # Pisahkan digit nilai ASCII
    encrypted_digits = [(digit ** e) % n for digit in digits]  # Enkripsi setiap digit
    encrypted_value = ".".join(map(str, encrypted_digits))  # Gabungkan hasil dengan '.'
    return encrypted_value

# Cara dekripsi per digit
def reverse_ascii_process(encrypted_value, d, n):
    encrypted_digits = list(map(int, encrypted_value.split(".")))  # Pisahkan hasil enkripsi
    decrypted_digits = [(digit ** d) % n for digit in encrypted_digits]  # Dekripsi setiap digit
    decrypted_value = int("".join(map(str, decrypted_digits)))  # Gabungkan kembali menjadi angka ASCII
    return decrypted_value

def rsa_encrypt_decrypt(p, q, plaintext):
    # Step 1: Menghitung n dan m
    n = p * q
    m = (p - 1) * (q - 1)

    # Step 2: Menentukan e
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    e = 2
    while e < m and gcd(e, m) != 1:
        e += 1

    # Step 3: Mencari d
    d = find_private_key(e, m)

    # Step 4: Mengubah ke ASCII dan mengenkripsi
    ascii_values = [ord(char) for char in plaintext]
    encrypted = [process_ascii_value(ascii, e, n) for ascii in ascii_values]

    # Step 5: Mendekripsi nilai terenkripsi
    decrypted_ascii = [reverse_ascii_process(enc, d, n) for enc in encrypted]
    try:
        decrypted_text = ''.join(chr(decrypted) for decrypted in decrypted_ascii)
    except ValueError:
        raise ValueError("Dekripsi menghasilkan karakter yang tidak valid.")

    # Output
    return {
        "n": n,
        "m": m,
        "e": e,
        "d": d,
        "encrypted": encrypted,
        "decrypted_text": decrypted_text
    }

# Input
try:
    p = int(input("Masukkan nilai p (bilangan prima): "))
    q = int(input("Masukkan nilai q (bilangan prima): "))
    plaintext = input("Masukkan plaintext: ")

    # Process
    result = rsa_encrypt_decrypt(p, q, plaintext)

    # Output
    print("\nHasil RSA:")
    print(f"n: {result['n']}")
    print(f"m: {result['m']}")
    print(f"e: {result['e']}")
    print(f"d: {result['d']}")
    print(f"Public Key: {result['e']},{result['n']}")
    print(f"Private Key: {result['d']},{result['n']}")
    print(f"Hasil Enkripsi: {result['encrypted']}")
    print(f"Hasil Dekripsi: {result['decrypted_text']}")
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
