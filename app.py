import streamlit as st
import time
import heapq
from collections import Counter
import matplotlib.pyplot as plt


# HUFFMAN IMPLEMENTATION

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_map):
    heap = [Node(ch, f) for ch, f in freq_map.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1, n2 = heapq.heappop(heap), heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left, merged.right = n1, n2
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def build_codes(node, prefix="", code_map={}):
    if node is None:
        return
    if node.char is not None:
        code_map[node.char] = prefix
    build_codes(node.left, prefix + "0", code_map)
    build_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(text):
    freq_map = Counter(text)
    root = build_huffman_tree(freq_map)
    codes = build_codes(root)
    encoded_text = ''.join(codes[ch] for ch in text)
    return encoded_text, codes, root

def huffman_decode(encoded_text, root):
    decoded = []
    node = root
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            decoded.append(node.char)
            node = root
    return ''.join(decoded)


# ADAPTIVE VERSION (Simulated)

def adaptive_huffman_demo(text):
    freq = {}
    encoded_stream = ""
    evolution = []

    for i, ch in enumerate(text, 1):
        freq[ch] = freq.get(ch, 0) + 1
        root = build_huffman_tree(freq)
        codes = build_codes(root, "", {})
        encoded_stream += codes[ch]
        evolution.append((i, dict(freq)))
    return encoded_stream, evolution



# STREAMLIT UI


st.set_page_config(page_title="Huffman Compressor", page_icon="🔠", layout="centered")

st.title("🔠 Huffman Text Compressor & Decompressor")
st.write("Upload a text file to **compress** it or select a `.huff` file to **decompress** it.")

# Mode selector
mode = st.radio("Select Encoding Mode:", ["Static Huffman", "Adaptive Huffman"], horizontal=True)

tab1, tab2 = st.tabs(["📦 Compress", "🪶 Decompress"])

# -----------------
# COMPRESSION TAB
# -----------------
with tab1:
    st.subheader("📂 Compression Mode")
    uploaded_file = st.file_uploader("Upload a text file for compression", type=["txt"], key="compress")

    if st.button("🧹 Clear All", key="clear_compress"):
        st.session_state.clear()
        st.rerun()

    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")

        if mode == "Static Huffman":
            start_time = time.time()
            encoded_text, codes, root = huffman_encode(text)
            end_time = time.time()
        else:
            start_time = time.time()
            encoded_text, evolution = adaptive_huffman_demo(text)
            end_time = time.time()
            st.info("Adaptive Huffman updates frequencies dynamically (no pre-pass).")

        original_size = len(text) * 8
        compressed_size = len(encoded_text)
        ratio = 100 * (1 - compressed_size / original_size)

        st.success("✅ Compression Completed!")
        st.write(f"**Original Size:** {original_size} bits ({len(text)/1024:.2f} KB)")
        st.write(f"**Compressed Size:** {compressed_size} bits ({compressed_size/8/1024:.2f} KB)")
        st.write(f"**Compression Ratio:** {ratio:.2f}%")
        st.write(f"**Encoding Time:** {end_time - start_time:.4f} sec")

        # ----- Compression Chart -----
        fig, ax = plt.subplots()
        ax.bar(["Original", "Compressed"], [original_size/8, compressed_size/8], color=["#FF4B4B", "#4BB543"])
        ax.set_ylabel("File Size (Bytes)")
        ax.set_title("Compression Comparison")
        st.pyplot(fig)

        if mode == "Static Huffman":
            st.subheader("🔤 Huffman Code Table")
            st.dataframe(
                [{"Character": k, "Frequency": text.count(k), "Code": v} for k, v in codes.items()],
                use_container_width=True
            )

                        # ✅ Save compressed binary file
        with open("compressed_output.huff", "w", encoding="utf-8") as f:
            f.write(encoded_text)

        # 📦 Download button for compressed file (always visible)
        with open("compressed_output.huff", "rb") as f:
            st.download_button(
                label="📦 Download Compressed File (.huff)",
                data=f,
                file_name="compressed_output.huff",
                mime="application/octet-stream"
            )

        # ✅ Save Huffman Codes for Decompression (only for Static Huffman)
        if mode == "Static Huffman" and 'codes' in locals():
            codes_path = "codes.txt"
            with open(codes_path, "w", encoding="utf-8") as f:
                for k, v in codes.items():
                    if k == '\n':
                        f.write("\\n:" + v + "\n")
                    elif k == ' ':
                        f.write("SPACE:" + v + "\n")
                    else:
                        f.write(f"{k}:{v}\n")

            st.success("✅ Generated 'codes.txt' for decompression.")

            # 📘 Download button for Huffman codes
            with open(codes_path, "r", encoding="utf-8") as f:
                st.download_button(
                    label="📘 Download Huffman Codes (codes.txt)",
                    data=f.read(),
                    file_name="codes.txt",
                    mime="text/plain"
                )


        # ----- Summary Report -----
        summary = f"""Huffman Compression Summary
---------------------------------
Mode: {mode}
Original Size: {original_size} bits
Compressed Size: {compressed_size} bits
Compression Ratio: {ratio:.2f}%
Encoding Time: {end_time - start_time:.4f} sec
"""
        st.download_button(
            label="📄 Download Summary Report",
            data=summary.encode("utf-8"),
            file_name="compression_summary.txt",
            mime="text/plain"
        )

        if mode == "Adaptive Huffman":
            st.subheader("📈 Frequency Evolution (Adaptive Mode)")
            for step, freq_map in evolution[:10]:
                st.text(f"After {step} chars → {freq_map}")


# -----------------
# DECOMPRESSION TAB
# -----------------
with tab2:
    st.subheader("📤 Decompression Mode")
    uploaded_huff = st.file_uploader("Upload a .huff file to decompress", type=["huff"], key="decompress")
    codes_file = st.file_uploader("Upload codes.txt (Huffman Code Mapping)", type=["txt"], key="codes")

    if st.button("🧹 Clear All", key="clear_decompress"):
        st.session_state.clear()
        st.rerun()

    if uploaded_huff and codes_file:
        encoded_text = uploaded_huff.read().decode("utf-8")
        code_map = {}

        for line in codes_file:
            line = line.decode("utf-8").strip()
            if ':' in line:
                char, code = line.split(':', 1)
                code_map[char] = code

        # Rebuild Huffman Tree
        root = Node(None, 0)
        for char, code in code_map.items():
            node = root
            for bit in code:
                if bit == '0':
                    if not node.left:
                        node.left = Node(None, 0)
                    node = node.left
                else:
                    if not node.right:
                        node.right = Node(None, 0)
                    node = node.right
            node.char = char

        start = time.time()
        decoded_text = huffman_decode(encoded_text, root)
        end = time.time()

        st.success("✅ Decompression Completed!")
        st.write(f"**Decoding Time:** {end - start:.4f} sec")
        st.text_area("📄 Decoded Text:", decoded_text, height=200)

        st.download_button(
            label="⬇️ Download Decoded Text",
            data=decoded_text.encode("utf-8"),
            file_name="decompressed_output.txt",
            mime="text/plain"
        )


