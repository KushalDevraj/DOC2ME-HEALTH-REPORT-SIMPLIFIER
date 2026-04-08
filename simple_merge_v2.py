import os
from docx import Document
from docxcompose.composer import Composer

def simple_merge():
    base = '/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main'
    front_path = os.path.join(base, 'capstonefinal.docx') # Use original as fixed is corrupted
    chapter_path = os.path.join(base, 'finalcapstone.docx')
    output_path = os.path.join(base, 'Merged_Project_Report_Original.docx')
    
    print(f"Opening front matter: {front_path}")
    master = Document(front_path)
    composer = Composer(master)
    
    print(f"Appending chapters: {chapter_path}")
    chapters = Document(chapter_path)
    composer.append(chapters)
    
    print(f"Saving merged document: {output_path}")
    composer.save(output_path)
    print("Merge complete!")
    return output_path

if __name__ == '__main__':
    simple_merge()
