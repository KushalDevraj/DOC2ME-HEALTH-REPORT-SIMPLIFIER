import matplotlib.pyplot as plt
import os

def create_design_strategy_slide():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#ffffff')
    
    # Header
    plt.text(0.5, 0.9, "Doc 2 Me: Design Strategy & Philosophy", 
             fontsize=22, fontweight='bold', ha='center', color='#1a73e8')
    
    # Strategy Blocks
    strategies = [
        ("Tiered Engineering", "Separation of Frontend (Flask), Backend (FastAPI), and AI (Ollama)."),
        ("Privacy-First Logic", "Local PII scrubbing sandbox prevents data leakage to external APIs."),
        ("Neural-Symbolic RAG", "Merging LLM generative power with verified FAISS medical definitions."),
        ("Local-First Design", "Full offline inference capability via high-performance Llama-3 8B."),
        ("Multimodal Pipeline", "OCR-first ingestion workflow designed for real-world scanned reports.")
    ]
    
    y = 0.75
    for title, desc in strategies:
        # Box for title
        plt.text(0.1, y, f" {title}:", fontsize=15, fontweight='bold', 
                 bbox=dict(facecolor='#e8f0fe', edgecolor='none', boxstyle='round,pad=0.2'), color='#1967d2')
        # Description
        plt.text(0.1, y-0.06, f"  {desc}", fontsize=12, color='#3c4043')
        y -= 0.15
        
    # Footer
    plt.text(0.5, 0.05, "Fig. 16 Strategic Architecture & Design Overview", 
             fontsize=12, style='italic', ha='center', color='#70757a')
    
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/ppt_design_strategy_summary.jpg', dpi=300, bbox_inches='tight')
    plt.close()
    print("Design Strategy slide image generated.")

if __name__ == '__main__':
    create_design_strategy_slide()
