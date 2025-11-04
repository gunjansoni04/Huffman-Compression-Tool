import heapq, time
from collections import defaultdict
from huffman import Node, generate_codes

def build_tree_from_freq(freq):
    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        l = heapq.heappop(heap)
        r = heapq.heappop(heap)
        merged = Node(None, l.freq + r.freq)
        merged.left, merged.right = l, r
        heapq.heappush(heap, merged)
    return heap[0]

def adaptive_encode(text, update_interval=1):
    freq = defaultdict(int)
    encoded_stream = ""
    step_results = []

    start = time.time()
    for i, ch in enumerate(text, 1):
        freq[ch] += 1
        root = build_tree_from_freq(freq)
        codes = generate_codes(root, "")
        encoded_stream += codes[ch]
        step_results.append((i, dict(freq), codes.copy()))

    end = time.time()
    return encoded_stream, end - start, step_results

if __name__ == "__main__":
    text = "HELLOHELLO"
    encoded, duration, steps = adaptive_encode(text)
    print("Encoded bits:", encoded)
    print("Time:", round(duration,4),"sec")
    print("\nFrequency and Code evolution:")
    for i, freq, codes in steps:
        print(f"After {i} chars → {freq}")
        print(f"Codes: {codes}")
        print("-" * 40)
