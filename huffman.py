import heapq
import time
import pickle

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, code="", mapping={}):
    if node is None:
        return
    if node.char is not None:
        mapping[node.char] = code
    generate_codes(node.left, code + "0", mapping)
    generate_codes(node.right, code + "1", mapping)
    return mapping

def huffman_encode(text, codes):
    return ''.join(codes[ch] for ch in text)

def huffman_decode(encoded_text, root):
    decoded = []
    node = root
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.char:
            decoded.append(node.char)
            node = root
    return ''.join(decoded)

def compress_text(text):
    start = time.time()
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    encoded = huffman_encode(text, codes)
    end = time.time()

    original_size = len(text.encode('utf-8')) * 8
    compressed_size = len(encoded)
    ratio = (1 - (compressed_size / original_size)) * 100

    decoded = huffman_decode(encoded, root)
    assert decoded == text, "Decompression failed!"

    return {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "ratio": round(ratio, 2),
        "time": round(end - start, 4),
        "encoded_text": encoded,
        "root": root
    }

def save_compressed(file_path, encoded_text, root):
    """Save compressed data as .huff file using pickle"""
    with open(file_path, "wb") as f:
        pickle.dump((encoded_text, root), f)

def load_and_decompress(file_path):
    """Load .huff file and decompress"""
    with open(file_path, "rb") as f:
        encoded_text, root = pickle.load(f)
    decoded_text = huffman_decode(encoded_text, root)
    return decoded_text
