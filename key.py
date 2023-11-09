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


# Function to permute the bits according to the given table
def permute(bits, table):
    return "".join(bits[i - 1] for i in table)


# Function to perform left circular shift
def shift_left(bits, shifts):
    return bits[shifts:] + bits[:shifts]


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

key = "AABB09182736CCDD"

# Key generation
round_keys_bin, round_keys_hex = generate_round_keys(key)

print('Keys:')
for item in round_keys_hex:
    print(item)