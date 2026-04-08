import matplotlib.pyplot as plt
import os

def create_conclusion_slide():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#ffffff')
    
    # Header
    plt.text(0.5, 0.9, "Conclusion & Future Scope", 
             fontsize=24, fontweight='bold', ha='center', color='#1e8e3e')
    
    # Conclusion Points
    plt.text(0.1, 0.8, "Conclusion:", fontsize=18, fontweight='bold', color='#202124')
    conclusions = [
        "Doc 2 Me successfully simplifies medical reports through secure, RAG-driven AI.",
        "Achieved 98.8% privacy success and 0.89 F1-score for clinical accuracy.",
        "Proved that local LLM inference (Ollama) is a viable path for secure clinical apps."
    ]
    y_c = 0.73
    for c in conclusions:
        plt.text(0.13, y_c, f"• {c}", fontsize=13, color='#3c4043')
        y_c -= 0.07

    # Future Scope Points
    plt.text(0.1, 0.5, "Future Scope:", fontsize=18, fontweight='bold', color='#202124')
    scopes = [
        "Expansion to handle complex 3D medical imaging (MRI/CT scans).",
        "Implementation of multi-regional language support beyond Nepali/Hindi.",
        "Integration with Electronic Health Records (EHR) for direct hospital sync.",
        "Development of a mobile-native application for broader patient outreach."
    ]
    y_s = 0.43
    for s in scopes:
        plt.text(0.13, y_s, f"◆ {s}", fontsize=13, color='#3c4043')
        y_s -= 0.07
        
    # Final Summary Note
    plt.text(0.5, 0.1, "Project Completed: March 2026", 
             fontsize=12, fontweight='bold', ha='center', color='#1a73e8')
    
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/ppt_conclusion_future_slide.jpg', dpi=300, bbox_inches='tight')
    plt.close()
    print("Conclusion slide generated.")

if __name__ == '__main__':
    create_conclusion_slide()
