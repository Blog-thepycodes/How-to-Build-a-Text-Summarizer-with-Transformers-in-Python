import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from transformers import pipeline
import threading
from collections import Counter
import string


summarizer = pipeline("summarization")




def summarize_text(text, max_length, min_length):
   summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
   return summary[0]['summary_text']




def open_file():
   file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
   if file_path:
       with open(file_path, 'r', encoding='utf-8') as file:
           text = file.read()
       text_area.delete("1.0", tk.END)
       text_area.insert(tk.END, text)
       display_text_info(text)




def save_summary():
   summary = summary_area.get("1.0", tk.END).strip()
   if summary:
       file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
       if file_path:
           with open(file_path, 'w', encoding='utf-8') as file:
               file.write(summary)
           messagebox.showinfo("Success", "Summary saved successfully!")
   else:
       messagebox.showwarning("Warning", "Summary is empty!")




def perform_summarization():
   text = text_area.get("1.0", tk.END).strip()
   if text:
       try:
           max_length = int(max_length_entry.get())
           min_length = int(min_length_entry.get())
           if min_length > max_length:
               messagebox.showwarning("Warning", "Min Length cannot be greater than Max Length!")
               return
           threading.Thread(target=run_summarization, args=(text, max_length, min_length)).start()
       except ValueError:
           messagebox.showwarning("Warning", "Please enter valid numbers for Max Length and Min Length!")
   else:
       messagebox.showwarning("Warning", "Input text is empty!")




def run_summarization(text, max_length, min_length):
   progress_bar.start()
   summary = summarize_text(text, max_length, min_length)
   summary_area.delete("1.0", tk.END)
   summary_area.insert(tk.END, summary)
   progress_bar.stop()




def display_text_info(text):
   word_count = len(text.split())
   char_count = len(text)
   most_common_words = Counter(text.lower().translate(str.maketrans('', '', string.punctuation)).split()).most_common(
       5)
   info = f"Word Count: {word_count}\nCharacter Count: {char_count}\nMost Common Words: {most_common_words}"
   info_label.config(text=info)




def create_gui():
   global text_area, summary_area, max_length_entry, min_length_entry, info_label, progress_bar


   root = tk.Tk()
   root.title("Text Summarizer - The Pycodes")
   root.geometry("900x700")


   title_label = tk.Label(root, text="Text Summarizer", font=("Helvetica", 16))
   title_label.pack(pady=10)


   text_frame = tk.Frame(root)
   text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


   text_label = tk.Label(text_frame, text="Input Text:")
   text_label.pack(anchor=tk.W)


   text_area_scrollbar = tk.Scrollbar(text_frame)
   text_area_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


   text_area = tk.Text(text_frame, wrap=tk.WORD, height=10, yscrollcommand=text_area_scrollbar.set)
   text_area.pack(fill=tk.BOTH, expand=True)
   text_area_scrollbar.config(command=text_area.yview)


   controls_frame = tk.Frame(root)
   controls_frame.pack(fill=tk.X, padx=10, pady=5)


   open_button = tk.Button(controls_frame, text="Open Text File", command=open_file)
   open_button.pack(side=tk.LEFT, padx=5)


   tk.Label(controls_frame, text="Max Length:").pack(side=tk.LEFT)
   max_length_entry = tk.Entry(controls_frame, width=5)
   max_length_entry.insert(0, "150")
   max_length_entry.pack(side=tk.LEFT, padx=5)


   tk.Label(controls_frame, text="Min Length:").pack(side=tk.LEFT)
   min_length_entry = tk.Entry(controls_frame, width=5)
   min_length_entry.insert(0, "30")
   min_length_entry.pack(side=tk.LEFT, padx=5)


   summarize_button = tk.Button(controls_frame, text="Summarize Text", command=perform_summarization)
   summarize_button.pack(side=tk.LEFT, padx=5)


   save_button = tk.Button(controls_frame, text="Save Summary", command=save_summary)
   save_button.pack(side=tk.LEFT, padx=5)


   summary_frame = tk.Frame(root)
   summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


   summary_label = tk.Label(summary_frame, text="Summary:")
   summary_label.pack(anchor=tk.W)


   summary_area_scrollbar = tk.Scrollbar(summary_frame)
   summary_area_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


   summary_area = tk.Text(summary_frame, wrap=tk.WORD, height=10, yscrollcommand=summary_area_scrollbar.set)
   summary_area.pack(fill=tk.BOTH, expand=True)
   summary_area_scrollbar.config(command=summary_area.yview)


   info_label = tk.Label(root, text="", font=("Helvetica", 10), justify=tk.LEFT)
   info_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


   progress_bar = ttk.Progressbar(root, mode="indeterminate", length=400)
   progress_bar.place(x=200, y=620)


   root.mainloop()




if __name__ == "__main__":
   create_gui()
