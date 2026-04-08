import matplotlib.pyplot as plt
import os

def create_hematology_sample():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')
    
    # Header
    plt.text(0.5, 0.95, "Doc 2 Me: Case Study A - Hematology (CBC)", 
             fontsize=18, fontweight='bold', ha='center', color='#1a73e8')
    
    # Original Text Box
    plt.text(0.05, 0.85, "Original Clinical Report:", fontsize=14, fontweight='bold', color='#202124')
    orig_text = ("Patient shows marked Leukocytosis (WBC: 18,000) with a left shift. \n"
                 "Peripheral smear reveals Thrombocytopenia (Platelets: 90,000). \n"
                 "Mild Microcytic Hypochromic Anemia noted.")
    plt.text(0.05, 0.70, orig_text, fontsize=11, color='#5f6368', 
             bbox=dict(facecolor='#f1f3f4', edgecolor='none', boxstyle='round,pad=1'))

    # AI Simplified Output
    plt.text(0.05, 0.55, "Doc 2 Me - Simplified Summary:", fontsize=14, fontweight='bold', color='#1e8e3e')
    simp_text = ("1. High White Blood Cell Count: This suggests your body is fighting a strong infection.\n"
                 "2. Low Platelet Count: Your blood may have difficulty clotting; watch for easy bruising.\n"
                 "3. Mild Anemia: Your red blood cells are smaller and paler than normal, often due to \n"
                 "   low iron levels, which may cause fatigue.")
    plt.text(0.05, 0.35, simp_text, fontsize=12, color='#202124', fontweight='bold',
             bbox=dict(facecolor='#e6f4ea', edgecolor='#1e8e3e', boxstyle='round,pad=1'))

    # Footer
    plt.text(0.5, 0.1, "*Accuracy verified via RAG Knowledge Base*", 
             fontsize=10, style='italic', ha='center', color='#70757a')
    
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/ppt_sample_hematology.jpg', dpi=300, bbox_inches='tight')
    plt.close()

def create_radiology_sample():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')
    
    # Header
    plt.text(0.5, 0.95, "Doc 2 Me: Case Study B - Radiology (Chest X-Ray)", 
             fontsize=18, fontweight='bold', ha='center', color='#d93025')
    
    # Original Text Box
    plt.text(0.05, 0.85, "Original Clinical Report:", fontsize=14, fontweight='bold', color='#202124')
    orig_text = ("Anterior-Posterior view of chest reveals bibasilar opacities. \n"
                 "Evidence of minor bilateral Pleural Effusion. \n"
                 "Cardiomegaly is present with a CTR of 0.62.")
    plt.text(0.05, 0.70, orig_text, fontsize=11, color='#5f6368', 
             bbox=dict(facecolor='#f1f3f4', edgecolor='none', boxstyle='round,pad=1'))

    # AI Simplified Output
    plt.text(0.05, 0.55, "Doc 2 Me - Simplified Summary:", fontsize=14, fontweight='bold', color='#1e8e3e')
    simp_text = ("1. Lung Cloudiness: There is 'haziness' at the bottom of both lungs, likely fluid.\n"
                 "2. Fluid Around Lungs: Small amount of water buildup is detected around the lung lining.\n"
                 "3. Enlarged Heart: Your heart appears larger than normal on the X-ray (CTR of 0.62), \n"
                 "   which might require further cardiac evaluation.")
    plt.text(0.05, 0.35, simp_text, fontsize=12, color='#202124', fontweight='bold',
             bbox=dict(facecolor='#e6f4ea', edgecolor='#1e8e3e', boxstyle='round,pad=1'))

    # Footer
    plt.text(0.5, 0.1, "*Accuracy verified via Llama-3 + Medical Vector Search*", 
             fontsize=10, style='italic', ha='center', color='#70757a')
    
    os.makedirs('images', exist_ok=True)
    plt.savefig('images/ppt_sample_radiology.jpg', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_hematology_sample()
    create_radiology_sample()
    print("Sample reports generated in images folder.")
