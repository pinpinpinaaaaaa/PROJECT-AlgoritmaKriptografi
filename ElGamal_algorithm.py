import random

def gen_key(q):
    """Langkah 3: Menghasilkan kunci privat acak x, dengan syarat 1 < x < p-2."""
    key = random.randint(2, q - 2)
    while gcd(q, key) != 1:
        key = random.randint(2, q - 2)
    return key

def power(a, b, c):
    """Langkah 4 & 6: Melakukan perpangkatan modular, digunakan untuk menghitung g^k mod p dan y^k mod p."""
    x = 1
    y = a % c
    while b > 0:
        if b % 2 == 1:
            x = (x * y) % c
        y = (y * y) % c
        b = b // 2
    return x

def mod_inverse(a, p):
    """Langkah 7: Menghitung invers modular, digunakan saat proses dekripsi untuk membagi b dengan a^x mod p."""
    return power(a, p - 2, p)

def encrypt(msg, p, g, y):
    """Langkah 5: Mengenkripsi pesan dengan bilangan acak k, dan menghasilkan pasangan cipherteks (a, b)."""
    en_msg = []
    details = []

    for i, char in enumerate(msg):
        m = ord(char)  # Mengonversi karakter ke ASCII (plaintext -> m)
        k = random.randint(1, p - 2)  # Kunci rahasia acak k
        a = power(g, k, p)  # Hitung a = g^k mod p
        b = (power(y, k, p) * m) % p  # Hitung b = (y^k * m) mod p
        en_msg.append((a, b))
        details.append((i + 1, m, k, a, b))

    return en_msg, details

def decrypt(en_msg, p, x):
    """Langkah 8: Mendekripsi pesan terenkripsi dengan menghitung m = (b / a^x) mod p."""
    dr_msg = ""

    for a, b in en_msg:
        s = power(a, x, p)  # Hitung s = a^x mod p
        m = (b * mod_inverse(s, p)) % p  # Hitung m = (b / s) mod p
        dr_msg += chr(int(m))

    return dr_msg

def main():
    """Langkah 1-2: Inisialisasi bilangan prima p dan akar primitif g."""
    msg = input("Masukkan pesan plaintext: ")
    p = int(input("Masukkan bilangan prima (p): "))

    # Langkah 2: Menentukan akar primitif (g)
    g = random.randint(2, p - 1)
    while gcd(p, g) != 1:
        g = random.randint(2, p - 1)

    x = gen_key(p)  # Langkah 3: Kunci privat penerima
    y = power(g, x, p)  # Langkah 4: Komponen kunci publik y = g^x mod p

    print("\nKunci Publik: (y, g, p) =", (y, g, p))
    print("Kunci Privat: (x, p) =", (x, p))
    print("\nTabel Perhitungan:")
    print("| n | m(n) | k(n) | a(n) | b(n) |")
    print("|---|------|------|------|------|")

    en_msg, details = encrypt(msg, p, g, y)
    for n, m, k, a, b in details:
        print(f"| {n} | {m} | {k} | {a} | {b} |")

    print("\nPasangan Cipherteks (a(n), b(n)):", en_msg)

    dr_msg = decrypt(en_msg, p, x)
    print("\nPesan Setelah Dekripsi:", dr_msg)

if __name__ == '__main__':
    main()
