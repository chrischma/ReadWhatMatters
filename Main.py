import os
import re
import PyPDF2
from pdfrw import PdfWriter, PdfReader
from tkinter import filedialog, messagebox
from tkinter import *

INCLUDE_CONTEXT = False         # if set to true, final pdf will include the previous page before the page
                                # that includes the search term.

def input_file_dialog():
    global input_file, file_path
    file_path = filedialog.askopenfilename(filetypes=[('pdf file', '*.pdf')])
    input_file = PyPDF2.PdfFileReader(file_path)


def short_pdf():
    page_count = input_file.getNumPages()
    search_term = search_term_input_field.get()
    input_file_name = re.search('(?!.*\/)(.*?)(?=.pdf)', file_path).group()
    output_file_name = str(input_file_name + '_reduced.pdf')

    output_pdf = PdfWriter()
    input_file_data = PdfReader(file_path)
    output_file_page_count = 0

    for i in range(0, page_count):

        page_content = input_file.getPage(i).extractText()
        result = re.findall(search_term, page_content)

        if len(result) > 0:

            if INCLUDE_CONTEXT is True and i >= 0:
                output_pdf.addPage(input_file_data.pages[i - 1])
                output_file_page_count += 1

            output_pdf.addPage(input_file_data.pages[i])
            output_file_page_count += 1

        print(f'page {i + 1}: {len(result)} results.')

        i += 1

    output_pdf.write(output_file_name)
    os.system(f'open .')
    messagebox.showinfo('Done!', f'Your pdf  \n'
                                 f'{output_file_name}\n'
                                 f'was created sucessfully!\n'
                                 f'The new pdf includes {output_file_page_count} of {page_count} pages.')


root = Tk()
root.title("Read What Matters 0.1")
root.geometry("330x250")
icon = PhotoImage(file='icon.gif')
root.iconphoto(False, icon)

input_file_dialog_button = Button(root, text="Chose file", command=input_file_dialog)
start_processing_button = Button(root, text="Go", command=short_pdf)

search_term_label = Label(root, text="Enter any search-term: ")
file_dialog_label = Label(root, text="Chose any pdf-file:")

logo = PhotoImage(file="logo.gif")
logo_panel = Label(root, image=logo)

search_term_input_field = Entry(root)
search_term_input_field.insert(0, "Literatur")

logo_panel.grid(row=0, column=2, sticky="w", pady="30")
search_term_label.grid(row=1, column=1)
file_dialog_label.grid(row=2, column=1)
search_term_input_field.grid(row=1, column=2)
input_file_dialog_button.grid(row=2, column=2, sticky="W")
start_processing_button.grid(row=3, column=2, sticky="w")

mainloop()
