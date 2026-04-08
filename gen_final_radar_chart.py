import matplotlib.pyplot as plt
import numpy as np
import os

def gen_radar_chart():
    # Categories for the radar chart
    categories = ['Privacy Integrity\n(ASR 98.8%)', 'Clinical Accuracy\n(F1 0.89)', 
                  'Inference Speed\n(1.5s Latency)', 'Multimodal\n(OCR/PDF/Img)', 
                  'Multilingual\n(Regional TTS)', 'Expert Reliability\n(Feedback Loop)']
    
    # Values (normalized to 1.0 for the chart)
    values = [0.99, 0.89, 0.92, 0.95, 0.85, 0.90]
    
    # Number of variables
    num_vars = len(categories)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # The chart is circular, so we need to "close the loop"
    values += values[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=10, fontweight='bold')
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["20%", "40%", "60%", "80%", "100%"], color="grey", size=8)
    plt.ylim(0, 1)
    
    # Plot data
    ax.plot(angles, values, color='#1a73e8', linewidth=2, linestyle='solid')
    
    # Fill area
    ax.fill(angles, values, color='#1a73e8', alpha=0.25)
    
    # Title
    plt.title('Fig 16. System Maturity and Readiness Radar Chart', size=16, color='#202124', y=1.1, fontweight='bold')
    
    os.makedirs('images', exist_ok=True)
    path = os.path.join('images', 'final_maturity_radar_chart.jpg')
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

if __name__ == '__main__':
    gen_radar_chart()
