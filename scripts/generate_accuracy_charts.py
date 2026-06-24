#!/usr/bin/env python3
"""
Generate Accuracy Charts (Figure 29) for Thesis
Creates professional charts showing model performance metrics
"""
import matplotlib.pyplot as plt
import numpy as np
import json
import os

def load_performance_data():
    """Load performance data from JSON file"""
    with open('performance_evaluation_results.json', 'r') as f:
        data = json.load(f)
    return data

def create_simple_accuracy_chart(data, save_path='figures/figure_29a_accuracy_simple.png'):
    """Create simple accuracy bar chart (left chart in reference)"""
    
    # Extract data
    classes = [item['name'] for item in data['classes']]
    accuracies = [item['accuracy'] for item in data['classes']]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bars
    x_pos = np.arange(len(classes))
    bars = ax.bar(x_pos, accuracies, color='#2E86AB', width=0.6)
    
    # Customize chart
    ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
    ax.set_xlabel('Disease Classes', fontsize=12, fontweight='bold')
    ax.set_title('Accuracy of the Classification', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(classes, rotation=45, ha='right', fontsize=9)
    ax.set_ylim(0, 1.0)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    
    # Add gridlines
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Add value labels on top of bars
    for i, (bar, acc) in enumerate(zip(bars, accuracies)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{acc:.2f}',
                ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Add legend
    ax.legend(['Classes'], loc='upper right', frameon=True, fancybox=True, shadow=True)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {save_path}")
    
    return fig

def create_multi_metric_chart(data, save_path='figures/figure_29b_accuracy_metrics.png'):
    """Create multi-metric comparison chart (right chart in reference)"""
    
    # Extract data
    classes = [item['name'] for item in data['classes']]
    accuracies = [item['accuracy'] for item in data['classes']]
    precisions = [item['precision'] for item in data['classes']]
    recalls = [item['recall'] for item in data['classes']]
    f1_scores = [item['f1_score'] for item in data['classes']]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Set up bar positions
    x_pos = np.arange(len(classes))
    width = 0.2  # Width of each bar
    
    # Create bars
    bars1 = ax.bar(x_pos - 1.5*width, accuracies, width, label='Accuracy', color='#2E86AB')
    bars2 = ax.bar(x_pos - 0.5*width, precisions, width, label='Precision', color='#F77F00')
    bars3 = ax.bar(x_pos + 0.5*width, recalls, width, label='Recall', color='#06A77D')
    bars4 = ax.bar(x_pos + 1.5*width, f1_scores, width, label='F1-Score', color='#D62828')
    
    # Customize chart
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('Disease Classes', fontsize=12, fontweight='bold')
    ax.set_title('Accuracy of the Classification', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(classes, rotation=45, ha='right', fontsize=9)
    ax.set_ylim(0, 1.0)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    
    # Add gridlines
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Add legend
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, ncol=2)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {save_path}")
    
    return fig

def create_combined_figure(data, save_path='figures/figure_29_combined.png'):
    """Create combined figure with both charts side by side"""
    
    # Extract data
    classes = [item['name'] for item in data['classes']]
    accuracies = [item['accuracy'] for item in data['classes']]
    precisions = [item['precision'] for item in data['classes']]
    recalls = [item['recall'] for item in data['classes']]
    f1_scores = [item['f1_score'] for item in data['classes']]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
    
    # LEFT CHART: Simple Accuracy
    x_pos = np.arange(len(classes))
    bars1 = ax1.bar(x_pos, accuracies, color='#2E86AB', width=0.6)
    
    ax1.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
    ax1.set_title('Accuracy', fontsize=12, fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(classes, rotation=45, ha='right', fontsize=8)
    ax1.set_ylim(0, 1.0)
    ax1.set_yticks(np.arange(0, 1.1, 0.1))
    ax1.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax1.set_axisbelow(True)
    ax1.legend(['Classes'], loc='upper right', fontsize=9)
    
    # RIGHT CHART: Multi-metric
    width = 0.2
    bars2_1 = ax2.bar(x_pos - 1.5*width, accuracies, width, label='Accuracy', color='#2E86AB')
    bars2_2 = ax2.bar(x_pos - 0.5*width, precisions, width, label='Precision', color='#F77F00')
    bars2_3 = ax2.bar(x_pos + 0.5*width, recalls, width, label='Recall', color='#06A77D')
    bars2_4 = ax2.bar(x_pos + 1.5*width, f1_scores, width, label='F1-Score', color='#D62828')
    
    ax2.set_ylabel('Score', fontsize=11, fontweight='bold')
    ax2.set_title('Accuracy of the Classification', fontsize=12, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(classes, rotation=45, ha='right', fontsize=8)
    ax2.set_ylim(0, 1.0)
    ax2.set_yticks(np.arange(0, 1.1, 0.1))
    ax2.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax2.set_axisbelow(True)
    ax2.legend(loc='upper right', fontsize=9, ncol=2)
    
    # Main title
    fig.suptitle('Figure 29: Accuracy Chart', fontsize=14, fontweight='bold', y=1.02)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {save_path}")
    
    return fig

def generate_all_charts():
    """Generate all chart variations"""
    print("=" * 80)
    print("📊 GENERATING ACCURACY CHARTS (Figure 29)")
    print("=" * 80)
    
    # Load data
    print("\n📂 Loading performance data...")
    data = load_performance_data()
    print(f"✅ Loaded data for {len(data['classes'])} classes")
    print(f"✅ Overall Accuracy: {data['overall_accuracy']:.4f} ({data['overall_accuracy']*100:.2f}%)")
    
    # Create charts
    print("\n📊 Creating charts...")
    
    # Simple accuracy chart
    print("\n1. Simple Accuracy Chart...")
    create_simple_accuracy_chart(data)
    
    # Multi-metric chart
    print("\n2. Multi-Metric Comparison Chart...")
    create_multi_metric_chart(data)
    
    # Combined figure
    print("\n3. Combined Figure (Both Charts)...")
    create_combined_figure(data)
    
    print("\n" + "=" * 80)
    print("✅ ALL CHARTS GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  📁 figures/figure_29a_accuracy_simple.png")
    print("  📁 figures/figure_29b_accuracy_metrics.png")
    print("  📁 figures/figure_29_combined.png")
    print("\nYou can now insert these charts into your thesis!")

if __name__ == "__main__":
    try:
        generate_all_charts()
        
        print("\n💡 Usage in Thesis:")
        print("-" * 80)
        print("1. Insert the chart image in your Chapter 4")
        print("2. Add caption: 'Figure 29: Accuracy Chart'")
        print("3. Reference it in your text")
        print("4. Add interpretation paragraph below the chart")
        
    except FileNotFoundError:
        print("\n❌ Error: performance_evaluation_results.json not found!")
        print("Please run: python scripts/generate_performance_table.py first")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
