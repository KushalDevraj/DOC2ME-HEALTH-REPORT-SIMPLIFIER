import sys
from docx import Document
from docxcompose.composer import Composer

def merge_documents(master_path, sub_path, output_path):
    try:
        # Load the master document
        master_doc = Document(master_path)
        # Load the document to append
        sub_doc = Document(sub_path)
        
        # Initialize the Composer with the master document
        composer = Composer(master_doc)
        
        # Append the sub document
        # Add a page break if needed, but the requirements just say "without changing the format"
        # composer.append will simply append it
        composer.append(sub_doc)
        
        # Save the result
        composer.save(output_path)
        print(f"Successfully merged documents into {output_path}")
    except Exception as e:
        print(f"Error merging documents: {e}")
        sys.exit(1)

if __name__ == '__main__':
    master = '/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main/capstonefinal.docx'
    sub = '/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main/finalcapstone.docx'
    out = '/Users/kushaldevraj/Downloads/Medical_Jargon_Simplification-main/merged_capstone.docx'
    
    merge_documents(master, sub, out)
