import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# Set the style
plt.style.use('seaborn-v0_8-muted')
os.makedirs('images', exist_ok=True)

def save_fig(name):
    path = os.path.join('images', name)
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# FIG 7: Hematology Metrics
def gen_fig7():
    metrics = ['Precision', 'Recall', 'F1-Score']
    values = [0.99, 0.98, 0.985]
    plt.figure(figsize=(8, 6))
    bars = plt.bar(metrics, values, color='#1f77b4', width=0.6)
    plt.ylabel('Performance Score')
    plt.title('Fig 7. T5-Transformer Metrics: Hematology Report Simplification')
    plt.ylim(0, 1.1)
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, 
                 f'{bar.get_height():.3f}', ha='center', va='bottom', fontweight='bold')
    save_fig('fig7_hematology.jpg')

# FIG 8: Radiology Metrics
def gen_fig8():
    metrics = ['Precision', 'Recall', 'F1-Score']
    values = [0.97, 0.96, 0.965]
    plt.figure(figsize=(8, 6))
    bars = plt.bar(metrics, values, color='#2c3e50', width=0.6)
    plt.ylabel('Performance Score')
    plt.title('Fig 8. Llama-3 Metrics: Radiology Report Interpretation')
    plt.ylim(0, 1.1)
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, 
                 f'{bar.get_height():.3f}', ha='center', va='bottom', fontweight='bold')
    save_fig('fig8_radiology.jpg')

# FIG 9: SHAP Feature Importance
def gen_fig9():
    features = ['Terminology Density', 'Sentence Length', 'Anatomic Context', 'Expert Feedback']
    importance = [0.35, 0.25, 0.20, 0.15]
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importance, y=features, palette='Blues_r')
    plt.title('Fig 9. SHAP Feature Importance for Medical Complexity Model')
    plt.xlabel('SHAP Importance Value')
    save_fig('fig9_shap_importance.jpg')

# FIG 10: Query Distribution
def gen_fig10():
    labels = ['Lab Interpretation', 'Clinical Dosage', 'General Mgmt']
    sizes = [60, 30, 10]
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e']
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title('Fig 10. Distribution of Patient Query Types (Pilot Phase)')
    save_fig('fig10_query_distribution.jpg')

# FIG 11: System Performance Summary
def gen_fig11():
    categories = ['OCR Pipeline', 'Simplification Core', 'Privacy Engine']
    accuracy = [0.95, 0.97, 0.988]
    latency = [0.5, 1.5, 0.3] # In seconds
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    
    width = 0.35
    x = range(len(categories))
    
    p1 = ax1.bar([i - width/2 for i in x], accuracy, width, label='Accuracy/ASR', color='#1f77b4')
    p2 = ax2.bar([i + width/2 for i in x], latency, width, label='Inference Latency (s)', color='#ff7f0e', alpha=0.7)
    
    ax1.set_ylabel('Accuracy / REDACTION Score', color='#1f77b4')
    ax2.set_ylabel('Latency (Seconds)', color='#ff7f0e')
    ax1.set_ylim(0, 1.1)
    ax2.set_ylim(0, 2.0)
    
    plt.title('Fig 11. System Performance: Doc 2 Me Operational Metrics')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    
    save_fig('fig11_performance_summary.jpg')

if __name__ == '__main__':
    gen_fig7()
    gen_fig8()
    gen_fig9()
    gen_fig10()
    gen_fig11()
