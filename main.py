from tkinter import *
from tkinter.messagebox import *
from collections import Counter
import pyperclip


# -*- coding: utf-8 -*-

def construct_form():

    def copy(event):
        pyperclip.copy(text_exit.get(1.0, END))

    def paste(event):
        text_entry.insert(1.0, pyperclip.paste())

    def clear(event):
        text_entry.delete(1.0, END)
        entry.delete(0, END)

    alphabet_table = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                      'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

    frequencies = {'а': 0.062, 'б': 0.014, 'в': 0.038, 'г': 0.013, 'д': 0.025, 'е': 0.072, 'ж': 0.07, 'з': 0.016,
                   'и': 0.062, 'й': 0.010, 'к': 0.028,
                   'л': 0.035, 'м': 0.026, 'н': 0.053, 'о': 0.09, 'п': 0.023, 'р': 0.040, 'с': 0.045, 'т': 0.053,
                   'у': 0.021, 'ф': 0.002, 'х': 0.009,
                   'ц': 0.003, 'ч': 0.012, 'ш': 0.006, 'щ': 0.003, 'ъ': 0.014, 'ы': 0.016, 'ь': 0.014, 'э': 0.003,
                   'ю': 0.006, 'я': 0.018}

    visinere_table = []
    for i in range(32):
        visinere_table.append(alphabet_table[i:] + alphabet_table[:i])


    def check_correctness(text):
        if (text == '\n' or text == ""):
            showerror(title="Ошибка", message="Необходимые поля содержат пустые значения")
            return False
        if [ch for ch in text if ch in '0123456789']:
            showerror(title="Ошибка", message="Необходимые поля содержат цифры")
            return False
        text = text.casefold()
        tab = str(alphabet_table)
        deltab = ",.!? -_)(*%№;:@#$^&[]\r\n"
        text = text.translate(str.maketrans(tab, tab, deltab))
        text = text.replace('ё', 'е')
        print(text)
        if any(ch not in alphabet_table for ch in text):
            showerror(title="Ошибка", message="Допустимы только буквы русского алфавита")
            return False
        return text

    def format_text(text):
        step = 0
        result = ""
        iter = 0
        while (iter < len(text)):
            if (step < 5):
                result += text[iter]
                step += 1
                iter += 1
            else:
                result += " "
                step = 0
        return result

    def cypher(event):

        text_exit.delete(1.0, END)

        text = text_entry.get(1.0, END)
        key = entry.get()

        text = str(check_correctness(text))
        if text == "False":
            return
        key = str(check_correctness(key))
        if key == "False":
            return

        key *= int(len(text) / len(key)) + 1
        key = key[:len(text)]

        cyphered_message = ""

        for i in range(len(text)):
            cyphered_message += visinere_table[alphabet_table.index(key[i])][alphabet_table.index(text[i])]

        text_exit.insert(1.0, format_text(cyphered_message))

    def decypher(event):

        text_exit.delete(1.0, END)

        text = text_entry.get(1.0, END)
        key = entry.get()

        text = str(check_correctness(text))
        if text == "False":
            return
        key = str(check_correctness(key))
        if key == "False":
            return

        key *= int(len(text) / len(key)) + 1
        key = key[:len(text)]

        decyphered_message = ""

        for i in range(len(text)):
            decyphered_message += alphabet_table[visinere_table[alphabet_table.index(key[i])].index(text[i])]

        text_exit.insert(1.0, format_text(decyphered_message))

    def hack(event):

        text_exit.delete(1.0, END)
        entry.delete(0, END)
        
        text = text_entry.get(1.0, END)
        text = str(check_correctness(text))
        if text == "False":
            return
        ngram_dict = {}
        for length in range(2,5):
            ngram_dict = searchNgrams(length, ngram_dict, text)
        print("Обнаруженные N-граммы и их местоположения: ",ngram_dict)
        distance_dict = convert_to_distance(ngram_dict)
        print("Дистанция между позициями: ",distance_dict)
        gcd_dict = find_gcd(distance_dict)
        print("НОД расстояний между позициями внутри одной группы N-граммы: ",gcd_dict)
        gcd_array = find_array_gcd([item[0] for item in gcd_dict.values()])
        gcd_array = [a for a in gcd_array if a!=1]
        print("НОД расстояний между группами: ",gcd_array)

        gcd_repeats = Counter(gcd_array)

        max=gcd_repeats[3]
        key_length=3
        for i in range(3,10):
            print("Количество повторений НОДа {0} = {1} ".format(i,gcd_repeats[i]))
            if gcd_repeats[i]>max:
                max = gcd_repeats[i]
                key_length = i
        print("предполагаемая длина ключа: {0}".format(key_length))

        shifts = []
        key = ""
        for i in range(key_length):
            shifts.append(text[i::key_length])
            print("Сдвиг номер {0} применим к буквам: {1}".format(i+1,shifts[-1]))

            char_repeats = Counter(shifts[-1])
            for k in char_repeats:
                char_repeats[k]=char_repeats[k]/len(alphabet_table)

            print("Частота встречаемости букв: {0}".format(char_repeats))
            minimal_shift=0
            minimal_interpolation = interpolation(shifts[-1])
            for k in range(1,len(alphabet_table)):
                new_shift = create_shift(shifts[-1],k)
                interpolation_coef = interpolation(new_shift)
                if (interpolation_coef<minimal_interpolation):
                    minimal_interpolation = interpolation_coef
                    minimal_shift=k
            fin_string = create_shift(shifts[-1],minimal_shift)
            print("Был произведен сдвиг влево на {0} позиций, новая строка: {1}".format(minimal_shift, fin_string))
            alph_character_index = alphabet_table.index(fin_string[0])
            seek_character = shifts[-1][0]
            key_character = ''
            for iter in range(len(visinere_table)):
                if (visinere_table[iter][alph_character_index]==seek_character):
                    key_character = alphabet_table[iter]
                    break;
            print("{0}-ая буква ключа: {1}".format(i+1,key_character))
            key+=key_character
        print("Найденный ключ: {0}".format(key))
        entry.insert(0, key)
        decypher(event)

    def create_shift(str, shift):
        final_string=""
        for iter in range(len(str)):
            final_string+=alphabet_table[(alphabet_table.index(str[iter])+shift)%len(alphabet_table)]
        return final_string

    def interpolation(str):
        interpolation_koef = 0
        char_repeats = Counter(str)
        for i in char_repeats:
            char_repeats[i] = char_repeats[i] / len(alphabet_table)
        for char in alphabet_table:
            try:
              interpolation_koef+=(frequencies[char]-char_repeats[char])**2
            except KeyError:
                interpolation_koef+=frequencies[char]**2

        return interpolation_koef

    def find_array_gcd(arr):
        gcd_array = []
        for i in range(len(arr)):
            for k in range(i+1, len(arr)):
                gcd_array.append(calc_gcd(arr[i],arr[k]))
        return gcd_array

    def  find_gcd(dict):
        for key in dict.keys():
            while (len(dict[key])>1):
                dict[key][0] = calc_gcd(dict[key][1], dict[key][0])
                dict[key].pop(1)
        return dict

    def calc_gcd(a,b):
        if (b==0):
            if (a==0): return -1
            else: return a
        else:
            if (a>b): return calc_gcd(b, a%b)
            else: return calc_gcd(a, b%a)

    def convert_to_distance(dict):
        for key in dict.keys():
            for iter in range(len(dict[key])):
                dict[key][iter] = max(dict[key])-dict[key][iter]
            dict[key].remove(0)
        return dict

    def searchNgrams(n, arr, text):
        for i in range(len(text) - n):
            ngram = text[i:i + n]
            temp_arr = []
            flag = True
            start_index = 0
            while (flag):
                temp_arr.append(text.find(ngram, start_index))
                if (temp_arr[-1] == -1):
                    temp_arr.pop()
                    if (len(temp_arr) > 1):
                        arr[ngram] = temp_arr
                    flag = False
                start_index += temp_arr[-1] + n

        return arr

    root = Tk()
    root.geometry('1500x500')

    root.title("Шифр Вижинера")

    frame_key = Frame(root)
    label_key = Label(frame_key, text="Введите ключ")
    entry = Entry(frame_key, width=100)
    frame_key.pack(fill=BOTH)
    label_key.pack(expand=1, side="left", fill=BOTH, padx=20, pady=10)
    entry.pack(expand=1, side="right", fill=BOTH, pady=10, padx=20)

    frame_buttons = Frame(root)
    cypher_button = Button(frame_buttons, text="Зашифровать", bg="lightgreen")
    paste_button = Button(frame_buttons, text="Вставить из буфера")
    decypher_button = Button(frame_buttons, text="Дешифровать", bg="lightblue")
    copy_button = Button(frame_buttons, text="Копировать в буфер")
    hack_button = Button(frame_buttons, text="Взломать", bg="lightyellow")
    clear_button = Button(frame_buttons, text="Очистить")
    frame_buttons.pack(fill=BOTH)
    cypher_button.pack(expand=1, side="left", padx=20, pady=10, fill=BOTH)
    paste_button.pack(expand=1, side="left", padx=20, pady=10, fill=BOTH)
    clear_button.pack(expand=1, side="left", padx=20, pady=10, fill=BOTH)
    hack_button.pack(expand=1, side="left", padx=230, pady=10, fill=BOTH)
    copy_button.pack(expand=1, side="left", padx=20, pady=10, fill=BOTH)
    decypher_button.pack(expand=1, side="left", padx=20, pady=10, fill=BOTH)

    frame_text = Frame(root)
    text_entry = Text(frame_text, bg="grey", fg="white", font={'Arial', 14})
    text_exit = Text(frame_text, bg="grey", fg="white", font={'Arial', 14}, wrap=WORD)
    text_entry.pack(side="left", padx=10, expand=1)
    scroll_entry = Scrollbar(frame_text, command=text_entry.yview)
    scroll_entry.pack(side="left")
    text_exit.pack(side="left", padx=10, expand=1)
    scroll_exit = Scrollbar(frame_text, command=text_exit.yview)
    scroll_exit.pack(side="left")
    frame_text.pack(fill=BOTH)

    hack_button.bind('<Button-1>', hack)
    decypher_button.bind('<Button-1>', decypher)
    cypher_button.bind('<Button-1>', cypher)
    copy_button.bind('<Button-1>', copy)
    paste_button.bind('<Button-1>', paste)
    clear_button.bind('<Button-1>', clear)
    root.mainloop()


construct_form()
