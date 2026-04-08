from docx import Document

files = [
    '/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main/capstonefinal.docx',
    '/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main/finalcapstone.docx'
]

for f in files:
    try:
        doc = Document(f)
        print(f"Successfully opened {f}")
    except Exception as e:
        print(f"Error opening {f}: {e}")
