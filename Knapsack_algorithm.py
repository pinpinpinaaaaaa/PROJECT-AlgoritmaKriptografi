import random
from math import gcd

def generate_superincreasing_sequence(length, start=1):
    """Generate a superincreasing sequence."""
    sequence = [start]
    for _ in range(1, length):
        sequence.append(sum(sequence) + random.randint(1, 10))
    return sequence

def generate_keys(superincreasing_sequence):
    """Generate public and private keys."""
    # Choose m (modulus) larger than the sum of all elements in the superincreasing sequence
    m = sum(superincreasing_sequence) + random.randint(10, 20)

    # Choose n (multiplier) such that gcd(n, m) = 1
    while True:
        n = random.randint(2, m - 1)
        if gcd(n, m) == 1:
            break

    # Generate public key by calculating (n * element) % m for each element in the sequence
    public_key = [(n * element) % m for element in superincreasing_sequence]

    return (public_key, (superincreasing_sequence, n, m))

def encrypt(plaintext, public_key):
    """Encrypt plaintext using the public key."""
    # Convert plaintext to binary
    binary_plaintext = ''.join(format(ord(char), '08b') for char in plaintext)

    # Split binary_plaintext into blocks of the same size as the public key
    block_size = len(public_key)
    blocks = [binary_plaintext[i:i + block_size] for i in range(0, len(binary_plaintext), block_size)]

    # Pad the last block if necessary
    if len(blocks[-1]) < block_size:
        blocks[-1] = blocks[-1].ljust(block_size, '0')

    # Encrypt each block
    ciphertext = []
    encryption_table = []  # Store table of calculations
    for block in blocks:
        encrypted_block = 0
        row_details = []  # Details for this block
        for bit, key in zip(block, public_key):
            product = int(bit) * key
            row_details.append(f"{bit} * {key} = {product}")
            encrypted_block += product
        encryption_table.append(row_details)
        ciphertext.append(encrypted_block)

    return ciphertext, blocks, encryption_table

def modular_inverse(n, m):
    """Calculate the modular inverse of n mod m using manual trial for k."""
    k = 0
    while True:
        potential_inverse = (1 + k * m) / n
        if potential_inverse.is_integer():
            print(f"k = {k}, Modular Inverse = {int(potential_inverse)}")
            return int(potential_inverse)
        k += 1

def decrypt(ciphertext, private_key):
    """Decrypt ciphertext using the private key."""
    superincreasing_sequence, n, m = private_key

    # Calculate the modular inverse of n mod m
    n_inverse = modular_inverse(n, m)

    # Decrypt each encrypted block
    binary_plaintext = ''
    decryption_steps = []  # Store decryption process details
    for encrypted_block in ciphertext:
        # Multiply encrypted_block by n_inverse mod m
        decrypted_value = (encrypted_block * n_inverse) % m

        # Solve the superincreasing knapsack problem to retrieve the original block
        block_bits = []
        step_details = []  # Details for each step
        for value in reversed(superincreasing_sequence):
            if decrypted_value >= value:
                block_bits.append('1')
                step_details.append(f"{decrypted_value} - {value} = {decrypted_value - value}")
                decrypted_value -= value
            else:
                block_bits.append('0')
                step_details.append(f"{decrypted_value} (unchanged)")
        block_bits.reverse()
        decryption_steps.append(step_details[::-1])
        binary_plaintext += ''.join(block_bits)

    # Convert binary plaintext to characters
    plaintext = ''.join(chr(int(binary_plaintext[i:i + 8], 2)) for i in range(0, len(binary_plaintext), 8))

    return plaintext, binary_plaintext, decryption_steps

# Example usage
if __name__ == "__main__":
    # Step 1: Generate keys
    superincreasing_sequence = generate_superincreasing_sequence(8)
    public_key, private_key = generate_keys(superincreasing_sequence)

    print("Superincreasing sequence (private key):", superincreasing_sequence)
    print("n (multiplier):", private_key[1])
    print("m (modulus):", private_key[2])
    print("Public key:", public_key)

    # Step 2: Encrypt plaintext
    plaintext = input("Enter plaintext: ")
    print("Plaintext:", plaintext)
    ciphertext, binary_blocks, encryption_table = encrypt(plaintext, public_key)

    print("\nBinary blocks:")
    for i, block in enumerate(binary_blocks):
        print(f"Block {i + 1}: {block}")

    print("\nEncryption table:")
    for i, row in enumerate(encryption_table):
        print(f"Block {i + 1} calculations:")
        for detail in row:
            print("  ", detail)

    print("\nCiphertext:", ciphertext)

    # Step 3: Decrypt ciphertext
    decrypted_text, decrypted_binary, decryption_steps = decrypt(ciphertext, private_key)

    print("\nDecryption steps:")
    for i, steps in enumerate(decryption_steps):
        print(f"Block {i + 1}:")
        for step in steps:
            print("  ", step)

    print("\nDecrypted binary:", decrypted_binary)
    print("Decrypted text:", decrypted_text)
