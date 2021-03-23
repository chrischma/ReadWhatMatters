import PyPDF2
import re
from pdfrw import PdfWriter, PdfReader
from tkinter import filedialog, messagebox
from tkinter import *


INCLUDE_CONTEXT = False


def input_file_dialog():
    print('check')
    global input_file, file_path
    input_file = None
    while input_file is None:
        try:
            file_path = '/Users/Chris/Downloads/10.1515_zrs-2016-0021.pdf'
            input_file = PyPDF2.PdfFileReader(file_path)
            file_path = filedialog.askopenfilename(filetypes=[('pdf file', '*.pdf')])

            input_file = PyPDF2.PdfFileReader(file_path)

        except FileNotFoundError:
            print('File not found. Please try again.')

        except PyPDF2.utils.PdfReadError:
            print('Please use a valid .pdf-file!')


def short_pdf():
    page_count = input_file.getNumPages()
    search_term = search_term_input_field.get()
    input_file_name = re.search('(?!.*\/)(.*?)(?=.pdf)', file_path).group()
    output_file_name = str('pages_of_' + input_file_name + '_including_' + search_term + '.pdf')

    output_pdf = PdfWriter()
    input_file_data = PdfReader(file_path)

    i = 0
    for i in range(0, page_count):
        page_content = input_file.getPage(i).extractText()
        result = re.findall(search_term, page_content)

        if len(result) > 0:

            if INCLUDE_CONTEXT is True and i >= 0:
                output_pdf.addPage(input_file_data.pages[i - 1])

            print(i)
            output_pdf.addPage(input_file_data.pages[i])

        print(f'page {i + 1}: {len(result)} results.')

        i += 1

    output_pdf.write(output_file_name)
    messagebox.showinfo('Done!', 'Your pdf was created sucessfully!')


root = Tk()
root.geometry("250x250")
root.title("Read What Matters 0.1")
input_file_dialog_button = Button(root, text="Chose file", command=input_file_dialog)
start_processing_button = Button(root, text="Go", command=short_pdf)
welcome_text = Label(root, text="Enter your search-term here:")
search_term_input_field = Entry(root)
search_term_input_field.insert(0, "Literatur")

welcome_text.pack()
search_term_input_field.pack()
input_file_dialog_button.pack()
start_processing_button.pack()

mainloop()
