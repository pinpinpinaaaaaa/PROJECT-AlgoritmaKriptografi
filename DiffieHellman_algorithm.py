import random
from sympy import isprime, primerange

def generate_large_prime(start=10**5, end=10**6):
    """
    Generate a large random prime number within the specified range.
    """
    primes = list(primerange(start, end))
    return random.choice(primes)

def diffie_hellman(p=None):
    """
    Implements the Diffie-Hellman key exchange algorithm.
    :param p: A prime number (optional, if not provided, will be generated).
    """
    # Step 1: Generate or accept user input for p (prime number)
    if not p:
        p = generate_large_prime()
        print(f"Generated prime number (p): {p}")
    else:
        if not isprime(p):
            raise ValueError("p must be a prime number.")

    # Step 2: Use default g (primitive root modulo p)
    g = 2
    print(f"Using primitive root (g): {g}")

    # Step 3: Alice inputs her private key (a) and computes her public key (A)
    a = int(input("Enter Alice's private key (a): "))  # Private key for Alice
    A = pow(g, a, p)             # Public key for Alice
    print(f"Alice's public key (A): {A}")

    # Step 4: Bob inputs his private key (b) and computes his public key (B)
    b = int(input("Enter Bob's private key (b): "))  # Private key for Bob
    B = pow(g, b, p)             # Public key for Bob
    print(f"Bob's public key (B): {B}")

    # Step 5: Compute the shared secret key
    K_alice = pow(B, a, p)  # Alice computes the shared key
    K_bob = pow(A, b, p)    # Bob computes the shared key

    print(f"Shared secret key computed by Alice: {K_alice}")
    print(f"Shared secret key computed by Bob: {K_bob}")

    # Verify that both keys are equal
    if K_alice == K_bob:
        print(f"Key exchange successful! Shared secret key (K): {K_alice}")
    else:
        print("Key exchange failed. Keys do not match.")

    return K_alice

# Example usage
if __name__ == "__main__":
    try:
        user_p = input("Enter a prime number (or press Enter to generate one): ")
        p = int(user_p) if user_p else None

        shared_key = diffie_hellman(p)
    except ValueError as e:
        print(f"Error: {e}")
