import pdfplumber
with pdfplumber.open("project report-updated (1).pdf") as pdf:
    for i in range(2):
        print(f"Page {i} images:")
        for img in pdf.pages[i].images:
            x0 = img.get('x0', 'N/A')
            x1 = img.get('x1', 'N/A')
            top = img.get('top', 'N/A')
            bottom = img.get('bottom', 'N/A')
            print(f"  Img: ({x0}, {top}, {x1}, {bottom})")
            
        print(f"Page {i} rects:")
        for rect in pdf.pages[i].rects:
            print(f"  Rect: ({rect.get('x0')}, {rect.get('top')}, {rect.get('x1')}, {rect.get('bottom')})")
