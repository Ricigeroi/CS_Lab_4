
# Function to convert hexadecimal to binary
def hex_to_bin(hex_value):
    hex_bin_map = {'0': "0000",
                   '1': "0001",
                   '2': "0010",
                   '3': "0011",
                   '4': "0100",
                   '5': "0101",
                   '6': "0110",
                   '7': "0111",
                   '8': "1000",
                   '9': "1001",
                   'A': "1010",
                   'B': "1011",
                   'C': "1100",
                   'D': "1101",
                   'E': "1110",
                   'F': "1111"}
    binary = "".join(hex_bin_map[hex_digit] for hex_digit in hex_value)
    return binary

# Function to convert binary to hexadecimal
def bin_to_hex(bin_value):
    bin_hex_map = {"0000": '0',
                   "0001": '1',
                   "0010": '2',
                   "0011": '3',
                   "0100": '4',
                   "0101": '5',
                   "0110": '6',
                   "0111": '7',
                   "1000": '8',
                   "1001": '9',
                   "1010": 'A',
                   "1011": 'B',
                   "1100": 'C',
                   "1101": 'D',
                   "1110": 'E',
                   "1111": 'F'}
    hex_value = "".join(bin_hex_map[bin_value[i:i+4]] for i in range(0, len(bin_value), 4))
    return hex_value

# Function to convert binary to decimal
def bin_to_dec(binary):
    decimal = int(binary, 2)
    return decimal

# Function to convert decimal to binary
def dec_to_bin(number):
    binary = bin(number).replace("0b", "")
    while len(binary) % 4 != 0:
        binary = '0' + binary
    return binary

# Function to permute the bits according to the given table
def permute(bits, table):
    return "".join(bits[i - 1] for i in table)

# Function to perform left circular shift
def shift_left(bits, shifts):
    return bits[shifts:] + bits[:shifts]

# Function to perform XOR operation between two bit strings
def xor_bits(bit_string1, bit_string2):
    return "".join('0' if bit == bit_string2[i] else '1' for i, bit in enumerate(bit_string1))

# Function to perform DES encryption/decryption
def des_process(input_hex, round_keys_bin):
    input_bin = hex_to_bin(input_hex)

    # Initial Permutation
    permuted_input = permute(input_bin, initial_permutation_table)
    print("\nAfter initial permutation:", bin_to_hex(permuted_input))
    print()

    # Splitting
    left, right = permuted_input[:32], permuted_input[32:]

    # 16 rounds of processing
    for i in range(16):
        # Expansion D-box: Expanding the 32 bits data into 48 bits
        right_expanded = permute(right, expansion_table)

        # XOR RoundKey[i] and right_expanded
        xor_result = xor_bits(right_expanded, round_keys_bin[i])

        # S-boxes: substituting the value from s-box table by calculating row and column
        sbox_result = ""
        for j in range(8):
            row = bin_to_dec(xor_result[j * 6] + xor_result[j * 6 + 5])
            col = bin_to_dec(xor_result[j * 6 + 1:j * 6 + 5])
            sbox_value = sbox[j][row][col]
            sbox_result += dec_to_bin(sbox_value)

        # Straight D-box: Rearranging the bits
        sbox_permuted = permute(sbox_result, straight_permutation_table)

        # XOR left and sbox_permuted
        left = xor_bits(left, sbox_permuted)

        # Swapping left and right for the next round
        if i != 15:
            left, right = right, left

        print(f"Round {i + 1}:\t LPT = {bin_to_hex(left)}, RPT = {bin_to_hex(right)}, KEY = {round_keys_hex[i]}")

    # Combination
    combined_result = left + right

    # Final permutation to get the cipher text
    cipher_text_bin = permute(combined_result, final_permutation_table)
    return cipher_text_bin

# Function to generate round keys from the given key
def generate_round_keys(key_hex):
    key_bin = hex_to_bin(key_hex)

    # Permutation using the parity bit drop table
    key_permuted = permute(key_bin, parity_bit_drop_table)

    # Splitting the key into two halves
    left, right = key_permuted[:28], key_permuted[28:]

    round_keys_bin = []
    round_keys_hex = []
    for shift_amount in shift_table:
        # Shifting the bits by the specified amount
        left, right = shift_left(left, shift_amount), shift_left(right, shift_amount)

        # Combining left and right halves
        combined_key = left + right

        # Compressing the key from 56 to 48 bits
        round_key_bin = permute(combined_key, key_compression_table)

        round_keys_bin.append(round_key_bin)
        round_keys_hex.append(bin_to_hex(round_key_bin))

    return round_keys_bin, round_keys_hex


# Tables used in the DES algorithm
initial_permutation_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]
expansion_table = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

straight_permutation_table = [
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

final_permutation_table = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Parity bit drop table (Key Permutation Table 1)
parity_bit_drop_table = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Shift table defines the number of left shifts of the key schedule
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Key Compression Table (Key Permutation Table 2)
key_compression_table = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Setup
plaintext = "123456ABCD132536"
key = "AABB09182736CCDD"

# Key generation
round_keys_bin, round_keys_hex = generate_round_keys(key)

print("\n\nENCRYPTION")
cipher_text = bin_to_hex(des_process(plaintext, round_keys_bin))
print("Cipher Text : ", cipher_text)

print("=" * 70)
print("\nDECRYPTION")
round_keys_bin_rev = round_keys_bin[::-1]
round_keys_hex_rev = round_keys_hex[::-1]
decrypted_text = bin_to_hex(des_process(cipher_text, round_keys_bin_rev))
print("Plain Text : ", decrypted_text)