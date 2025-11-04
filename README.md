# 🗜️ Huffman Compression & Decompression Tool  
### Built using Python | Streamlit | Data Compression Algorithm

---

## 📖 Project Overview
This project implements **Huffman Encoding and Decoding** — a lossless data compression algorithm.  
It allows users to upload a text file, compress it efficiently using **Static or Adaptive Huffman Coding**, and then decompress it back to its original form.

It also includes a modern **Streamlit Web Interface** for easy interaction, visualization, and report generation.

---

## 🎯 Objectives
- To design and implement a **lossless compression algorithm** using Huffman Coding.  
- To visualize **compression ratios** and compare original vs. compressed sizes.  
- To provide a simple, user-friendly **web UI** using Streamlit.  
- To implement an **Adaptive Huffman** version for real-time compression simulation.  
- To demonstrate algorithmic concepts like **Greedy technique**, **Divide & Conquer**, and **Complexity Analysis**.

---

## ⚙️ System Architecture
The system follows a modular design:
User Interface (Streamlit)
↓
Input & Preprocessing
↓
Huffman Encoder / Adaptive Encoder
↓
Compressed File (.huff) + Code Mapping (codes.txt)
↓
Huffman Decoder
↓
Decompressed Output + Reports

🖼️ *Refer to the architecture diagram in the repository.*

---

## 💻 Features
- 📦 **Text Compression:** Upload `.txt` files and compress them into `.huff` format.  
- 🪶 **Decompression:** Reconstruct original text using generated `codes.txt`.  
- ⚡ **Dual Modes:**  
  - **Static Huffman Encoding**  
  - **Adaptive Huffman Encoding (Real-time)**  
- 📊 **Visualization:** Compare file sizes with bar charts.  
- 📄 **Auto Summary Report:** Generates compression statistics automatically.  
- 🌐 **Web-based Interface:** Built with Streamlit — no installation hassles.

---

## 🧠 Algorithm Concepts Used
- **Design and Analysis Concepts:**  
  - Greedy Algorithm (Huffman Coding)  
  - Complexity Analysis (O(n log n))  
  - Divide and Conquer (Tree Construction)  
  - Empirical Complexity via Profiling  

- **Complexity Overview:**  
  - Building Frequency Table → O(n)  
  - Building Huffman Tree → O(k log k)  
  - Encoding → O(n)  
  - Decoding → O(n)

---

## 🚀 How to Run the Project

### 🧩 1. Clone the Repository
```bash
git clone https://github.com/gunjansoni04/Huffman-Compression-Tool.git
cd Huffman-Compression-Tool

3. Run the Streamlit App
streamlit run app.py


Then open the local URL shown in the terminal.

📊 Sample Output
Metric	Example Result
Original Size	3800 bits
Compressed Size	849 bits
Compression Ratio	77.66%
Encoding Time	0.0003 sec
🧩 Files & Structure
📂 HuffmanProject
 ┣ 📄 app.py                → Streamlit interface
 ┣ 📄 huffman.py            → Huffman encoding/decoding logic
 ┣ 📄 adaptive_demo.py      → Adaptive Huffman simulation
 ┣ 📂 data/                 → Sample text files (English, Hindi, Marathi, Tamil)
 ┣ 📄 codes.txt             → Code mapping for decoding
 ┣ 📄 compressed_output.huff→ Compressed file output
 ┗ 📄 README.md             → Project documentation

🧾 Report Highlights

Algorithm Used: Huffman Coding (Greedy Approach)

Programming Language: Python

Tools: Streamlit, Matplotlib

Dataset: Custom multilingual text samples

Extension: Adaptive Huffman Algorithm (Dynamic frequency update)

👩‍💻 Author

Gunjan Soni
Department of Artificial Intelligence & Data Science
Vishwakarma Institute of Information Technology, Pune

📚 References

Huffman, D. A. “A Method for the Construction of Minimum-Redundancy Codes.” Proceedings of the IRE, 1952.

Streamlit Documentation: https://docs.streamlit.io

GeeksforGeeks: Huffman Coding Algorithm

