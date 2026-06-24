import json

notebook_data = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Tomato Leaf Disease Model - Final Performance Evaluation\n",
    "\n",
    "This notebook contains the complete evaluation pipeline for the tomato disease identification system, including:\n",
    "- Dataset organization check\n",
    "- Class label synchronization fix\n",
    "- Confusion Matrix visualization (Raw & Normalized)\n",
    "- Per-Class Performance Metrics (Precision, Recall, F1-Score)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import tensorflow as tf\n",
    "import numpy as np\n",
    "import os\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from tensorflow.keras.preprocessing.image import ImageDataGenerator\n",
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "import pandas as pd\n",
    "\n",
    "print(\"✅ Libraries loaded successfully\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. MODEL & DATA PATHS\n",
    "MODEL_PATH = r'backend/trained_model_fito_outdoor.h5'\n",
    "TEST_DATA_PATH = r'C:/Users/hewer/Desktop/DATASET/test'\n",
    "\n",
    "# 2. SETTINGS\n",
    "IMG_SIZE = 224\n",
    "BATCH_SIZE = 32\n",
    "\n",
    "if os.path.exists(MODEL_PATH):\n",
    "    print(f\"✅ Model found at: {MODEL_PATH}\")\n",
    "else:\n",
    "    print(f\"❌ ERROR: Model not found at {MODEL_PATH}\")\n",
    "\n",
    "if os.path.exists(TEST_DATA_PATH):\n",
    "    print(f\"✅ Test dataset found at: {TEST_DATA_PATH}\")\n",
    "else:\n",
    "    print(f\"❌ ERROR: Test dataset folder not found.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. CLASS LABEL SYNCHRONIZATION FIX\n",
    "# Forced order to match how the model was trained (fixes the 0.00 accuracy issue)\n",
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
    "]\n",
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
    "print(f\"\\nLoaded {test_generator.samples} images across {len(class_names)} classes.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"Running predictions on test set... (This may take a moment)\")\n",
    "model = tf.keras.models.load_model(MODEL_PATH)\n",
    "predictions = model.predict(test_generator, verbose=1)\n",
    "predicted_classes = np.argmax(predictions, axis=1)\n",
    "true_classes = test_generator.classes\n",
    "\n",
    "print(\"✅ Prediction complete!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "report = classification_report(true_classes, predicted_classes, target_names=class_names, output_dict=True)\n",
    "report_df = pd.DataFrame(report).transpose()\n",
    "\n",
    "print(\"\\nDetailed Classification Report:\")\n",
    "print(\"=\" * 60)\n",
    "print(classification_report(true_classes, predicted_classes, target_names=class_names))\n",
    "\n",
    "accuracy = report_df.loc['accuracy', 'precision']\n",
    "print(f\"\\nFinal Test Accuracy: {accuracy:.2%}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visual 1: Raw Confusion Matrix\n",
    "cm = confusion_matrix(true_classes, predicted_classes)\n",
    "\n",
    "plt.figure(figsize=(12, 10))\n",
    "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', \n",
    "            xticklabels=class_names, yticklabels=class_names)\n",
    "plt.title('Confusion Matrix (Raw Counts)', fontsize=16, fontweight='bold')\n",
    "plt.xlabel('Predicted Disease', fontsize=12)\n",
    "plt.ylabel('Actual Disease', fontsize=12)\n",
    "plt.xticks(rotation=45, ha='right')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visual 2: Normalized Confusion Matrix\n",
    "cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]\n",
    "\n",
    "plt.figure(figsize=(12, 10))\n",
    "sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Greens', \n",
    "            xticklabels=class_names, yticklabels=class_names)\n",
    "plt.title('Normalized Confusion Matrix (Accuracy %)', fontsize=16, fontweight='bold')\n",
    "plt.xlabel('Predicted Disease', fontsize=12)\n",
    "plt.ylabel('Actual Disease', fontsize=12)\n",
    "plt.xticks(rotation=45, ha='right')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visual 3: Per-Class Performance Metrics (Precision, Recall, F1)\n",
    "# Extract metrics and melt for grouped bar chart\n",
    "metrics_df = report_df.loc[class_names, ['precision', 'recall', 'f1-score']]\n",
    "metrics_df.index.name = 'Class'\n",
    "metrics_df = metrics_df.reset_index()\n",
    "metrics_melted = metrics_df.melt(id_vars='Class', var_name='Metric', value_name='Score')\n",
    "\n",
    "plt.figure(figsize=(15, 8))\n",
    "ax = sns.barplot(data=metrics_melted, x='Class', y='Score', hue='Metric', palette='muted')\n",
    "\n",
    "plt.title('Performance Metrics per Tomato Disease Class', fontsize=16, fontweight='bold')\n",
    "plt.xlabel('Disease Class', fontsize=12)\n",
    "plt.ylabel('Score (0.0 - 1.0)', fontsize=12)\n",
    "plt.xticks(rotation=45, ha='right')\n",
    "plt.ylim(0, 1.2)\n",
    "plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')\n",
    "\n",
    "# Add values on bars\n",
    "for p in ax.patches:\n",
    "    height = p.get_height()\n",
    "    if height > 0:\n",
    "        ax.annotate(format(height, '.2f'), \n",
    "                    (p.get_x() + p.get_width() / 2., height), \n",
    "                    ha='center', va='center', \n",
    "                    xytext=(0, 9), textcoords='offset points', fontsize=9, fontweight='bold')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visual 4: F1-Score Summary (Detailed Comparison)\n",
    "plt.figure(figsize=(12, 6))\n",
    "f1_scores = report_df.loc[class_names, 'f1-score']\n",
    "colors = sns.color_palette('viridis', len(class_names))\n",
    "\n",
    "ax = sns.barplot(x=f1_scores.index, y=f1_scores.values, palette=colors)\n",
    "plt.title('F1-Score Overview', fontsize=16, fontweight='bold')\n",
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
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('Final_Model_Evaluation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_data, f, indent=1)

print("Created Final_Model_Evaluation.ipynb successfully!")
