import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def gen_strategy_architecture_clean():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Styles
    main_blue = '#1f77b4'
    light_blue = '#aec7e8'
    sec_grey = '#f0f0f0'
    expert_orange = '#ff7f0e'
    text_color_light = 'white'
    text_color_dark = 'black'

    # 1. USER INTERFACE LAYER
    ax.add_patch(patches.Rectangle((0, 6.5), 12, 1, facecolor=main_blue, edgecolor='black', alpha=0.9))
    ax.text(6, 7, 'LAYER 1: USER INTERFACE (FLASK DASHBOARD)', color=text_color_light, ha='center', va='center', fontweight='bold', fontsize=12)
    
    # 2. LOGIC LAYER (SECURITY SANDBOX)
    # Dashed Sandbox
    ax.add_patch(patches.Rectangle((0.5, 3), 11, 3, facecolor=sec_grey, edgecolor='black', linestyle='--', linewidth=2, alpha=0.5))
    ax.text(6, 5.7, 'LAYER 2: LOGIC ENGINE (FASTAPI - SECURE SANDBOX)', color=text_color_dark, ha='center', va='center', fontweight='bold', fontsize=11)
    
    # Modules inside Layer 2
    ax.add_patch(patches.FancyBboxPatch((1, 3.5), 2.5, 1.5, boxstyle="round,pad=0.1", facecolor=light_blue, edgecolor='black'))
    ax.text(2.25, 4.25, 'Multimodal\nOCR Ingestion\n(Tesseract)', ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((4.5, 3.5), 3, 1.5, boxstyle="round,pad=0.1", facecolor='#ffcccc', edgecolor='black'))
    ax.text(6, 4.25, 'SECURE\nPII Scrubbing &\nAnonymization', ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((8.5, 3.5), 2.5, 1.5, boxstyle="round,pad=0.1", facecolor=light_blue, edgecolor='black'))
    ax.text(9.75, 4.25, 'Retrieval\nAugmentation\n(LangChain)', ha='center', va='center', fontsize=9, fontweight='bold')

    # 3. DATA & INTELLIGENCE LAYER
    ax.add_patch(patches.Rectangle((0, 0.5), 12, 2, facecolor='#2ca02c', edgecolor='black', alpha=0.7))
    ax.text(6, 1.5, 'LAYER 3: DATA & INTELLIGENCE HOSTING', color=text_color_light, ha='center', va='center', fontweight='bold', fontsize=12)
    
    ax.add_patch(patches.Rectangle((1.5, 0.8), 3, 1, facecolor='white', edgecolor='black'))
    ax.text(3, 1.3, 'FAISS Vector Index\n(12k+ Medical Terms)', ha='center', va='center', fontsize=9)
    
    ax.add_patch(patches.Rectangle((7.5, 0.8), 3, 1, facecolor='white', edgecolor='black'))
    ax.text(9, 1.3, 'Llama-3 8B Engine\n(Local Inference)', ha='center', va='center', fontsize=9)

    # EXPERT FEEDBACK LOOP
    ax.add_patch(patches.Circle((6, 0.4), 0.15, color=expert_orange))
    ax.text(6, 0, 'Medical Expert Review', ha='center', va='center', fontweight='bold', color=expert_orange)
    
    # ARROWS
    hw = 0.2
    ax.arrow(2.25, 6.5, 0, -1.2, head_width=hw, fc='black')
    ax.arrow(3.7, 4.25, 0.6, 0, head_width=hw, fc='black')
    ax.arrow(7.7, 4.25, 0.6, 0, head_width=hw, fc='black')
    ax.arrow(3.0, 3.5, 0, -1.2, head_width=hw, fc='black')
    ax.arrow(9.0, 3.5, 0, -1.2, head_width=hw, fc='black')
    ax.annotate("", xy=(3, 0.8), xytext=(6, 0.2), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color=expert_orange, lw=2))

    # REMOVED TITLE HEADING
    
    os.makedirs('images', exist_ok=True)
    path = os.path.join('images', 'strategy_architecture_diagram_v2.jpg')
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

if __name__ == '__main__':
    gen_strategy_architecture_clean()
