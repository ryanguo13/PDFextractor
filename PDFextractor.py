from PyPDF2 import PdfReader
import os

def extract_pdf_contents(pdf_path, save_directory):

    pdf = PdfReader(pdf_path)
    images = []
    links = []
    for page_num, page in enumerate(pdf.pages):

        page_resources = page['/Resources']
        if '/XObject' in page_resources:
            xObject = page_resources['/XObject'].get_object()
            for obj_name in xObject:
                obj = xObject[obj_name].get_object()
                if obj['/Subtype'] == '/Image':
                    images.append(obj.get_data())


                    obj_name_cleaned = obj_name.strip('/').replace('/', '_')
                    
                    image_filename = f'image_{page_num+1}_{obj_name_cleaned}.jpg'
                    image_path = os.path.join(save_directory, image_filename)

        
                    os.makedirs(os.path.dirname(image_path), exist_ok=True)

                    with open(image_path, 'wb') as img_file:
                        img_file.write(obj.get_data())
                    print(f'Saved image to {image_path}')
                    

        if '/Annots' in page:
            for annot in page['/Annots']:
                annot_obj = annot.get_object()
                if annot_obj['/Subtype'] == '/Link' and '/A' in annot_obj:
                    action = annot_obj['/A']
                    if action['/S'] == '/URI':
                        links.append(action['/URI'])

    for link in links:
        print("Found link:" ,link)
        print("---------------------------------") 
        
    return images, links

