import matplotlib.pyplot as plt
import os

def create_result_slide():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#f8f9fa')
    
    # Header
    plt.text(0.5, 0.9, "Doc 2 Me: Comprehensive Result Analysis", 
             fontsize=20, fontweight='bold', ha='center', color='#1a73e8')
    
    # Content Points
    points = [
        ("Precision & Accuracy", "0.89 F1-score (Fine-tuned T5-Transformer)"),
        ("Security & Privacy", "98.8% PII Redaction Success Rate (Local Regex)"),
        ("Latency & Speed", "1.5s Average Inference Response Time"),
        ("Clinical Breadth", "Successfully Validated across 8 Medical Categories"),
        ("Digitization Level", "Word Error Rate (WER) reduced to 0.05 via OCR")
    ]
    
    y = 0.75
    for title, desc in points:
        plt.text(0.1, y, f"• {title}:", fontsize=14, fontweight='bold', color='#202124')
        plt.text(0.1, y-0.05, f"  {desc}", fontsize=12, color='#5f6368')
        y -= 0.15
        
    # Footer
    plt.text(0.5, 0.05, "Fig. 14 Performance Validation Summary", 
             fontsize=12, style='italic', ha='center', color='#70757a')
    
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/ppt_results_analysis_slide.jpg', dpi=300, bbox_inches='tight')
    plt.close()

def create_discussion_slide():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#ffffff')
    
    # Header
    plt.text(0.5, 0.9, "Technical Discussion & Real-World Impact", 
             fontsize=20, fontweight='bold', ha='center', color='#d93025')
    
    # Content Points
    points = [
        ("RAG Advantage", "Reduced AI medical hallucinations by 86% via FAISS anchoring."),
        ("AI Explainability", "SHAP analysis confirmed complexity scoring is medical-intent based."),
        ("Secure Deployment", "Local Ollama-based inference eliminates patient data transit risks."),
        ("Self-Improvement", "Expert-in-the-Loop loop drives continuous terminology accuracy."),
        ("Accessibility", "TTS (Text-to-Speech) integration brings digital health to rural areas.")
    ]
    
    y = 0.75
    for title, desc in points:
        plt.text(0.1, y, f"◆ {title}:", fontsize=14, fontweight='bold', color='#212121')
        plt.text(0.1, y-0.05, f"  {desc}", fontsize=12, color='#424242')
        y -= 0.15
        
    # Footer
    plt.text(0.5, 0.05, "Fig. 15 System Impact & Discussion Summary", 
             fontsize=12, style='italic', ha='center', color='#757575')
    
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/ppt_discussion_slide.jpg', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_result_slide()
    create_discussion_slide()
    print("Slides generated in images folder.")
