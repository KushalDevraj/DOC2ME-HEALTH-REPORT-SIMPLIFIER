import matplotlib.pyplot as plt
import os

def gen_simple_bar_chart():
    # Metrics and their scores (out of 100)
    metrics = ['Privacy Compliance', 'Medical Accuracy', 'System Speed', 'User Accessibility']
    scores = [99, 89, 92, 95]
    colors = ['#1a73e8', '#34a853', '#fbbc05', '#ea4335']

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create horizontal bars
    bars = ax.barh(metrics, scores, color=colors, height=0.6)
    
    # Add data labels at the end of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 5, bar.get_y() + bar.get_height()/2, f'{width}%', 
                ha='right', va='center', color='white', fontweight='bold', fontsize=12)

    # Styling
    ax.set_xlim(0, 110)
    ax.set_xlabel('Success / Performance Rating (%)', fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks(range(0, 101, 20))
    
    plt.title('Overall Project Success Metrics', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()

    os.makedirs('images', exist_ok=True)
    path = os.path.join('images', 'simple_project_metrics.jpg')
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved {path}")

if __name__ == '__main__':
    gen_simple_bar_chart()
