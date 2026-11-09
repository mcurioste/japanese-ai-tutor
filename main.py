from pathlib import Path
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

MODEL_FILENAME = "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"


def resource_path(relative):
    # PyInstaller onedir uses _internal; source runs relative to this file.
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
    return base / relative


class JapaneseTutor:
    def __init__(self, root):
        self.root = root
        root.title('Japanese Tutor — Local AI Demo')
        root.geometry('700x530')
        root.minsize(540, 430)
        self.model = None
        tk.Label(root, text='Japanese Tutor', font=('Segoe UI', 19, 'bold')).pack(pady=(16, 2))
        tk.Label(root, text='Offline • No account • No saved chat history', font=('Segoe UI', 10)).pack()
        self.status = tk.StringVar(value='Loading model...')
        tk.Label(root, textvariable=self.status, fg='#336699').pack(pady=8)
        self.answer = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=14, font=('Segoe UI', 11))
        self.answer.pack(fill='both', expand=True, padx=18, pady=(5, 10))
        self.answer.configure(state='disabled')
        tk.Label(root, text='Ask a Japanese-language question:').pack(anchor='w', padx=18)
        self.prompt = tk.Entry(root, font=('Segoe UI', 11))
        self.prompt.pack(fill='x', padx=18, pady=5)
        self.prompt.insert(0, 'Teach me how to say good morning in Japanese.')
        self.prompt.bind('<Return>', lambda _event: self.ask())
        self.ask_button = tk.Button(root, text='Ask tutor', command=self.ask, state='disabled')
        self.ask_button.pack(pady=(4, 16))
        threading.Thread(target=self.load_model, daemon=True).start()

    def show_answer(self, text):
        self.answer.configure(state='normal')
        self.answer.delete('1.0', tk.END)
        self.answer.insert(tk.END, text)
        self.answer.configure(state='disabled')

    def load_model(self):
        path = resource_path(f'models/{MODEL_FILENAME}')
        if not path.is_file():
            self.root.after(0, lambda: self.status.set('Model missing. Run download_model.py first.'))
            return
        try:
            from llama_cpp import Llama
            self.model = Llama(model_path=str(path), n_ctx=2048, n_gpu_layers=0,
                               chat_format='chatml', verbose=False)
        except Exception as exc:
            err = str(exc)
            self.root.after(0, lambda: messagebox.showerror('Model load failed', err))
            self.root.after(0, lambda: self.status.set('Could not load model'))
            return
        self.root.after(0, lambda: self.status.set('Ready — running locally on CPU'))
        self.root.after(0, lambda: self.ask_button.configure(state='normal'))

    def ask(self):
        question = self.prompt.get().strip()
        if not question or self.model is None:
            return
        self.ask_button.configure(state='disabled')
        self.status.set('Generating...')
        self.show_answer('Thinking...')
        threading.Thread(target=self.generate, args=(question,), daemon=True).start()

    def generate(self, question):
        try:
            response = self.model.create_chat_completion(
                messages=[
                    {'role': 'system', 'content': 'You are a friendly Japanese tutor for English speakers. Give concise, clear explanations. Include Japanese text, romaji, and English translations when useful. If uncertain, say so.'},
                    {'role': 'user', 'content': question},
                ],
                max_tokens=300, temperature=0.4,
            )
            text = response['choices'][0]['message']['content'] or '(No response)'
            self.root.after(0, lambda: self.show_answer(text))
        except Exception as exc:
            err = str(exc)
            self.root.after(0, lambda: self.show_answer('Error: ' + err))
        finally:
            self.root.after(0, lambda: self.status.set('Ready — running locally on CPU'))
            self.root.after(0, lambda: self.ask_button.configure(state='normal'))


if __name__ == '__main__':
    root = tk.Tk()
    JapaneseTutor(root)
    root.mainloop()
