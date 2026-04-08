import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def gen_rag_diagram_v2():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Color Palette
    box_color_main = '#1f77b4'
    box_color_sub = '#aec7e8'
    text_color = 'white'
    text_color_sub = 'black'

    # 1. INPUT
    ax.add_patch(patches.Rectangle((0.5, 4.5), 2.5, 1, color=box_color_main, ec='black'))
    ax.text(1.75, 5, 'Input: Scanned Report\n(Anonymized Text)', color=text_color, ha='center', va='center', fontweight='bold', fontsize=10)

    # 2. EMBEDDINGS
    ax.add_patch(patches.Rectangle((4, 4.5), 2.5, 1, color=box_color_main, ec='black'))
    ax.text(5.25, 5, 'Semantic Search\n(FAISS Vector Database)', color=text_color, ha='center', va='center', fontweight='bold', fontsize=10)

    # 3. KNOWLEDGE
    ax.add_patch(patches.Rectangle((4, 2.7), 2.5, 0.8, color=box_color_sub, ec='black'))
    ax.text(5.25, 3.1, 'Verified Medical Jargon\n& Layman Definitions', color=text_color_sub, ha='center', va='center', fontsize=9)

    # 4. INFERENCE
    ax.add_patch(patches.Rectangle((7.5, 3.5), 2, 2, color=box_color_main, ec='black'))
    ax.text(8.5, 4.5, 'LLM Engine\n(Llama-3 8B / T5)\nInference Module', color=text_color, ha='center', va='center', fontweight='bold', fontsize=10)

    # 5. OUTPUT
    ax.add_patch(patches.Rectangle((7.5, 1.0), 2, 1, color='#2ca02c', ec='black'))
    ax.text(8.5, 1.5, 'OUTPUT:\nSimplified Summary', color=text_color, ha='center', va='center', fontweight='bold', fontsize=10)

    # ARROWS
    hw = 0.15 # head width
    # Input -> Search
    ax.arrow(3.0, 5.0, 0.8, 0, head_width=hw, fc='black', ec='black')
    # Search -> Inference
    ax.arrow(6.5, 5.0, 0.8, 0, head_width=hw, fc='black', ec='black')
    # Knowledge -> Inference
    ax.arrow(6.5, 3.1, 0.8, 0.6, head_width=hw, fc='black', ec='black')
    # Inference -> Output
    ax.arrow(8.5, 3.5, 0, -1.3, head_width=hw, fc='black', ec='black')

    # UPDATED TITLE
    plt.title('Fig 3.4. Generative Simplification Engine (RAG Pipeline) Workflow', fontsize=14, fontweight='bold', pad=20)
    
    os.makedirs('images', exist_ok=True)
    path = os.path.join('images', 'fig3_4_rag_pipeline.jpg')
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

if __name__ == '__main__':
    gen_rag_diagram_v2()
