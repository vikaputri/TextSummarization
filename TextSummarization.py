from PIL import ImageTk
import PIL.Image
from tkinter import *
import tkinter as tk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

windo = Tk()
windo.configure(background='white')
windo.title("Summarization App")
windo.geometry('1150x700')
windo.resizable(0,0)

def clear():
    Input.delete(1.0, END)
    Result.destroy()
    Judul2.destroy()

def destroy_widget(widget):
    widget.destroy()

def hasil():
    global Judul2, Result, result
    query = Input.get(1.0, END)

    def _create_frequency_table(text_string):
        stopWords = set(stopwords.words("indonesian"))
        words = word_tokenize(text_string)
        ps = PorterStemmer()

        freqTable = dict()
        for word in words:
            word = ps.stem(word)
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        return freqTable


    def _score_sentences(sentences, freqTable):
        sentenceValue = dict()

        for sentence in sentences:
            word_count_in_sentence = (len(word_tokenize(sentence)))
            word_count_in_sentence_except_stop_words = 0
            for wordValue in freqTable:
                if wordValue in sentence.lower():
                    word_count_in_sentence_except_stop_words += 1
                    if sentence[:10] in sentenceValue:
                        sentenceValue[sentence[:10]] += freqTable[wordValue]
                    else:
                        sentenceValue[sentence[:10]] = freqTable[wordValue]

            if sentence[:10] in sentenceValue:
                sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words

        return sentenceValue


    def _find_average_score(sentenceValue):
        sumValues = 0
        for entry in sentenceValue:
            sumValues += sentenceValue[entry]

        average = (sumValues / len(sentenceValue))

        return average


    def _generate_summary(sentences, sentenceValue, threshold):
        sentence_count = 0
        summary = ''

        for sentence in sentences:
            if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
                summary += " " + sentence
                sentence_count += 1

        return summary


    def run_summarization(text):
        freq_table = _create_frequency_table(text)
        sentences = sent_tokenize(text)
        sentence_scores = _score_sentences(sentences, freq_table)
        threshold = _find_average_score(sentence_scores)
        summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)
        return summary

    result = run_summarization(query)

    Judul2 = tk.Label(windo, text="Result : ", width=10, height=1, fg="white",bg="blue",
                font=('times', 16, ' bold '))
    Judul2.place(x=600, y=100)

    Result = tk.Text(windo,borderwidth = 7, width=45, heigh=20, bg="white", fg="black", font=('times', 16))
    Result.place(x=600, y=135)
    Result.configure(state='normal')
    Result.insert(tk.END, result)
    Result.configure(state='disabled')

Judul = tk.Label(windo, text="Automatic Text Summarization App", width=40, height=2, fg="white",bg="black",
                font=('times', 20, ' bold '))
Judul.place(x=274, y=10)

Judul1 = tk.Label(windo, text="Input Text : ", width=13, height=1, fg="white",bg="blue",
                font=('times', 16, ' bold '))
Judul1.place(x=35, y=100)

Input = tk.Text(windo,borderwidth = 7, width=45, heigh=20, bg="white", fg="black", font=('times', 16))
Input.place(x=35, y=135)

Clear = Button(windo,borderwidth=0, text='CLEAR', command = clear, fg="white", bg="red", font=('times', 15, ' bold '))
Clear.pack()
Clear.place(x=450, y=650)

Hasil = Button(windo,borderwidth=0, text='SUMMARIZE', command = hasil, fg="white", bg="red", font=('times', 15, ' bold '))
Hasil.pack()
Hasil.place(x=600, y=650)

windo.mainloop()
