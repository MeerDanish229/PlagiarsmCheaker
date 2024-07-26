import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import filedialog, Text

nltk.download('punkt')

nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    words = nltk.word_tokenize(text.lower())
    doc = nlp(' '.join(words))
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return ' '.join(tokens)

def detect_plagiarism(text1, text2):
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])
    
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0]

def open_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    entry.delete(1.0, tk.END)
    entry.insert(tk.END, content)

def compare_texts():
    text1 = text1_entry.get("1.0", tk.END).strip()
    text2 = text2_entry.get("1.0", tk.END).strip()
    if text1 and text2:
        score = detect_plagiarism(text1, text2)
        result_label.config(text=f"Similarity Score: {score:.2f}")
    else:
        result_label.config(text="Please provide text in both fields.")

root = tk.Tk()
root.title("Plagiarism Detection Tool")

text1_entry = Text(root, height=10, width=50)
text1_entry.grid(row=0, column=0, padx=10, pady=10)
text2_entry = Text(root, height=10, width=50)
text2_entry.grid(row=0, column=1, padx=10, pady=10)

open_file_btn1 = tk.Button(root, text="Open File 1", command=lambda: open_file(text1_entry))
open_file_btn1.grid(row=1, column=0, padx=10, pady=10)
open_file_btn2 = tk.Button(root, text="Open File 2", command=lambda: open_file(text2_entry))
open_file_btn2.grid(row=1, column=1, padx=10, pady=10)
compare_btn = tk.Button(root, text="Compare Texts", command=compare_texts)
compare_btn.grid(row=2, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Similarity Score: N/A")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
