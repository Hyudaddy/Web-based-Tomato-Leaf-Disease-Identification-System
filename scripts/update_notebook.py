import json
import os

notebook_path = r'c:\Users\hewer\Desktop\Web-based-Tomato-Leaf-Disease-Identification-System-main\Test_Model_Performance.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The correct order from training (fixes the 0.00 accuracy issue)
trained_classes_code = [
    "trained_classes = [\n",
    "    'Tomato___Bacterial_spot',\n",
    "    'Tomato___Early_blight',\n",
    "    'Tomato___Late_blight',\n",
    "    'Tomato___Leaf_Mold',\n",
    "    'Tomato___Septoria_leaf_spot',\n",
    "    'Tomato___Spider_mites Two-spotted_spider_mite',\n",
    "    'Tomato___Target_Spot',\n",
    "    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',\n",
    "    'Tomato___Tomato_mosaic_virus',\n",
    "    'Tomato___healthy'\n",
    "]\n"
]

# 1. Update the Data Path cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'TEST_DATA_PATH =' in source:
            cell['source'] = [
                "# 1. MODEL PATH\n",
                "MODEL_PATH = r'backend/trained_model_fito_outdoor.h5'\n",
                "\n",
                "# 2. TEST DATASET PATH\n",
                "TEST_DATA_PATH = r'C:/Users/hewer/Desktop/DATASET/test'\n",
                "\n",
                "# 3. SETTINGS\n",
                "IMG_SIZE = 224\n",
                "BATCH_SIZE = 32\n",
                "\n",
                "import os\n",
                "if os.path.exists(MODEL_PATH):\n",
                "    print(f\"Model found at: {MODEL_PATH}\")\n",
                "if os.path.exists(TEST_DATA_PATH):\n",
                "    print(f\"Test dataset found at: {TEST_DATA_PATH}\")\n"
            ]

# 2. Update the Generator cell with the Label Fix
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'flow_from_directory' in source and 'test_generator =' in source:
            cell['source'] = trained_classes_code + [
                "\n",
                "test_datagen = ImageDataGenerator(rescale=1./255)\n",
                "\n",
                "test_generator = test_datagen.flow_from_directory(\n",
                "    TEST_DATA_PATH,\n",
                "    target_size=(IMG_SIZE, IMG_SIZE),\n",
                "    batch_size=BATCH_SIZE,\n",
                "    class_mode='categorical',\n",
                "    classes=trained_classes, # <--- FIXED: Explicit class order\n",
                "    shuffle=False\n",
                ")\n",
                "\n",
                "class_names = list(test_generator.class_indices.keys())\n",
                "print(f\"\\nLoaded {test_generator.samples} images across {len(class_names)} classes.\")\n"
            ]

# 3. Define Visualization Cells
f1_graph_source = [
    "# Plot F1-Score per Class\n",
    "plt.figure(figsize=(12, 6))\n",
    "f1_scores = report_df.loc[class_names, 'f1-score']\n",
    "colors = sns.color_palette('viridis', len(class_names))\n",
    "\n",
    "ax = sns.barplot(x=f1_scores.index, y=f1_scores.values, palette=colors)\n",
    "plt.title('F1-Score per Tomato Disease Class', fontsize=16, fontweight='bold')\n",
    "plt.xlabel('Disease Class', fontsize=12)\n",
    "plt.ylabel('F1-Score', fontsize=12)\n",
    "plt.xticks(rotation=45, ha='right')\n",
    "plt.ylim(0, 1.1)\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(format(p.get_height(), '.2f'), \n",
    "                (p.get_x() + p.get_width() / 2., p.get_height()), \n",
    "                ha='center', va='center', \n",
    "                xytext=(0, 9), textcoords='offset points', fontweight='bold')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]

accuracy_graph_source = [
    "# Plot Accuracy (Recall) per Class\n",
    "plt.figure(figsize=(12, 6))\n",
    "accuracy_scores = report_df.loc[class_names, 'recall']\n",
    "colors = sns.color_palette('magma', len(class_names))\n",
    "\n",
    "ax = sns.barplot(x=accuracy_scores.index, y=accuracy_scores.values, palette=colors)\n",
    "plt.title('Accuracy (Recall) per Tomato Disease Class', fontsize=16, fontweight='bold')\n",
    "plt.xlabel('Disease Class', fontsize=12)\n",
    "plt.ylabel('Accuracy', fontsize=12)\n",
    "plt.xticks(rotation=45, ha='right')\n",
    "plt.ylim(0, 1.1)\n",
    "\n",
    "for p in ax.patches:\n",
    "    ax.annotate(format(p.get_height(), '.2f'), \n",
    "                (p.get_x() + p.get_width() / 2., p.get_height()), \n",
    "                ha='center', va='center', \n",
    "                xytext=(0, 9), textcoords='offset points', fontweight='bold')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]

# Remove existing visualization cells to avoid duplicates
nb['cells'] = [c for c in nb['cells'] if not ("Plot F1-Score per Class" in "".join(c['source']) or "Plot Accuracy (Recall) per Class" in "".join(c['source']))]

# Add the visualization cells at the end
nb['cells'].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": f1_graph_source})
nb['cells'].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": accuracy_graph_source})

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully with Label Fix and Visualizations!")
