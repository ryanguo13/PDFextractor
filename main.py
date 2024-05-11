from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
from PyPDF2 import PdfReader
import sys, os
import PDFextractor

class PdfExtractorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.files = []
        self.save_path = ""
        self.init_ui()

    def init_ui(self):
            self.layout = QVBoxLayout()

            self.status_label = QLabel('Select PDF files from which to extract images & links.')
            self.layout.addWidget(self.status_label) 

            self.open_btn = QPushButton('Open file(s)')
            self.open_btn.clicked.connect(self.open_files) 
            self.layout.addWidget(self.open_btn) 

            self.save_btn = QPushButton('Save image(s) to')
            self.save_btn.clicked.connect(self.save_images)  
            self.layout.addWidget(self.save_btn)  

            self.run_btn = QPushButton('Run extraction')
            self.run_btn.clicked.connect(self.run_extraction)  
            self.layout.addWidget(self.run_btn)  

            self.output = QTextEdit()
            self.layout.addWidget(self.output)  

            self.setLayout(self.layout)

            self.setWindowTitle('PDF Extractor')  
            self.setGeometry(300, 300, 600, 400)  
        
    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Open PDF File(s)', '', 'PDF Files (*.pdf)')
        if files:
            self.files = files
            self.status_label.setText(f'Selected {len(files)} file(s).')   
    
    def save_images(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
          
            self.save_path = directory
            self.status_label.setText(f'Selected save location: {directory}')
    
    
    def run_extraction(self):
            if not self.files or not self.save_path:
                self.status_label.setText('Please select files and save location first.')
                return
            
            for file_path in self.files:
                try:
                    images, links = PDFextractor.extract_pdf_contents(file_path, self.save_path)

                    self.output.append(f"Processed {file_path}:")
                    for link in links:
                        self.output.append(f"Found link: {link}")
                except Exception as e:
                    self.output.append(f"Error processing {file_path}: {e}")
                

            link_filename = "links.txt"
            link_path = self.save_path
            
            filename = 'links.txt'
            file_path = os.path.join(self.save_path, filename)

            with open(file_path, 'w') as file:
                for link in links:
                    file.write(link + '\n')

            print('Links are wrote in the file: links.txt', file_path)
                
            
            self.status_label.setText('Extraction completed!')
    

def main():
    app = QApplication(sys.argv)
    ex = PdfExtractorApp()
    ex.show()
    sys.exit(app.exec_())
            
if __name__ == '__main__':
    main()