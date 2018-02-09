import PyPDF2
import appJar
import os
import pathlib


def split_pdf(infile, output_directory, outfile, page_range):
    reader = PyPDF2.PdfFileReader(open(infile, 'rb'))
    writer = PyPDF2.PdfFileWriter()
    outfile = open(output_directory + '/' + outfile + '.pdf', 'wb')

    pages = (x.split('-') for x in page_range.split(','))
    range_list = [i for r in pages for i in range(int(r[0]), int(r[-1]) + 1)]

    for j in range_list:
        try:
            writer.addPage(reader.getPage(j - 1))
        except IndexError:
            app.infoBox('Info', 'Please select a different page range /nFile will be saved')
            break

    writer.write(outfile)

    if app.questionBox('File Saved', 'Quit?'):
        app.stop()


def press(button):
    if button == 'Process':
        src_file = app.getEntry('input_file')
        dest_direct = app.getEntry('output_directory')
        file_name = app.getEntry('output_name')
        page_range = app.getEntry('page_range')
        errors, error_msgs = validate_input(src_file, dest_direct, file_name, page_range)
        if errors:
            app.errorBox('Error', '/n'.join(error_msgs), parent=None)
        else:
            split_pdf(src_file, dest_direct, file_name, page_range)
    elif button == 'Quit':
        app.stop()


def validate_input(src_file, dest_direct, file_name, page_range):
    errors = False
    error_msgs = []

    if pathlib.Path(src_file).suffix.upper() != '.PDF':
        errors = True
        error_msgs.append('Please target a .PDF file')

    if not os.path.isdir(dest_direct):
        errors = True
        error_msgs.append('Please target a directory for the output pdf')

    if len(page_range) < 1:
        errors = True
        error_msgs.append('Please add at least one page to split')

    if len(file_name) < 1:
        errors = True
        error_msgs.append('Please input a valid file name')

    return errors, error_msgs


if __name__ == '__main__':
    app = appJar.gui('PDF Splitter', useTtk=True)
    app.setTtkTheme('vista')
    app.setSize(500, 200)

    app.addLabel('Choose Source PDF File')
    app.addFileEntry('input_file')

    app.addLabel('Choose Destination Folder')
    app.addDirectoryEntry('output_directory')

    app.addLabel('Output File Name')
    app.addEntry('output_name')

    app.addLabel('Page Ranges: 1,3,4-10')
    app.addEntry('page_range')

    app.addButtons(['Process', 'Quit'], press)

    app.go()
