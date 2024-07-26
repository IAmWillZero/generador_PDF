import streamlit as st
from fpdf import FPDF

class PDF (FPDF):
    def header(self):
        # Logo
        
         if hasattr(self, "document title"): 
            self.image('logo.png', 10, 8, 33)
            self.set_font('arial','B', 12)
            self.cell(0, 10, self.document_title, 0, 1, 'C')
            self.ln(20)
            
    def footer(self) -> None:
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}' , 0 ,0, 'C')

    def chapter_title(self, title, font= 'Arial', size = 12):
        self. set_font(font, 'B', size)
        self.cell(0, 10, title, 0, 1, 'L')  
        self.ln(10)
    
    def chapter_body(self,body,font='Arial',size = 12):
        self.set_font(font,'',size)
        self.multi_cell(0,10,body)
        self.ln(10)
    
def create_pdf (filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title= document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)

    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w - 20)
        pdf.ln(120)

    for chapter in chapters:
        title,body,font,size = chapter
        pdf.chapter_title(title,font,size)
        pdf.chapter_body(body,font,size)

    pdf.output(filename)

def main():
    st.title("Generador de PDF con Python")
    st.header("Configuración del documento")
    document_title = st.text_input("Título del Documento","Título del Documento" )
    author = st.text_input("Autor","")
    uploadet_image  = st.file_uploader("Sube una imagen para el documento (opcional)", type = ["jpg", "png"])
    
    st.header("Capitulos del documento")
    chapters =[]
    chapter_count = st.number_input("Cantidad de capitulos", min_value=1, max_value=50, value=1)
     
    for i in range (chapter_count):
        st.subheader(f'Capítulo { i + 1}')
        title = st.text_input(f'Título del capítulo {i + 1}'
                              ,f'Título del capítulo {i + 1}')
        body = st.text_area(f'Contenido del capítulo {i + 1}'
                            ,f'Contenido del capítulo {i + 1}')
        font = st.selectbox(f'Fuente del capítulo {i + 1}',
                            ['Arial', 'Courier', 'Times'])
        size = st.slider(f'Tamaño de fuente del capitulo {i +1}', 8, 24, 12)
        chapters.append((title, body, font, size))
    if st.button("Generar PDF"):
        image_path = uploadet_image.name if uploadet_image else None
        if image_path:
            with open(image_path, "wb") as f:
                f.write(uploadet_image.getbuffer())
                
        create_pdf("output_fpdf.pdf", document_title,
                   author, chapters, image_path)
        with open("output_fpdf.pdf", "rb") as pdf_file:
            PDFbyte= pdf_file.read()

        st.download_button(
            label="Descargar PDF",
            data=PDFbyte,
            file_name="output_fpdf.pdf",
            mime='aplication/octet-stream'
        )
        st.success("PDF generado exitosamente")


            
                                                                                                          
    

if __name__ == '__main__':
    main()






