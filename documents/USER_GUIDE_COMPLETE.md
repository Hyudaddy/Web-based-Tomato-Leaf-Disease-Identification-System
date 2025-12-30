# 📖 Fito User Guide - Complete Beginner's Guide

## Welcome to Fito!

**Fito** (Tomato Leaf Disease Identification System) is a web-based application that helps farmers and agricultural practitioners identify tomato leaf diseases using artificial intelligence. Simply upload a photo of a tomato leaf, and Fito will analyze it and tell you if the plant is healthy or diseased.

---

## 🎯 What Can Fito Do?

✅ **Identify 10 Common Tomato Diseases** - Instant disease detection  
✅ **Provide Treatment Recommendations** - Get actionable advice  
✅ **Access Disease Library** - Learn about each disease  
✅ **90.17% Accuracy** - Reliable AI-powered predictions  
✅ **Works on Any Device** - Desktop, tablet, or smartphone  
✅ **Free to Use** - No registration required for basic features

---

## 📱 Getting Started

### Step 1: Access the System

1. Open your web browser (Chrome, Firefox, Safari, or Edge)
2. Go to the Fito website: `http://localhost:3000` (for local installation)
3. You'll see the home page with a welcome message

### Step 2: Navigate the Website

The navigation menu at the top has several options:

| Menu Item | What It Does |
|-----------|--------------|
| **Home** | Main landing page with system introduction |
| **About** | Information about Fito and how it works |
| **Fito** | Disease detection tool (upload images here) |
| **Information** | Complete disease library with photos and details |
| **FAQ** | Frequently asked questions |
| **Contact** | Get in touch with support |
| **Log-in** | Admin access (for authorized users only) |

---

## 🔍 How to Detect Tomato Diseases

### Step-by-Step Guide

#### 1. Go to the Detection Page

- Click on **"Fito"** in the navigation menu
- You'll see an upload area on the left side

#### 2. Upload Your Image

**Option A: Drag and Drop**
- Take a photo of a tomato leaf with your camera or phone
- Drag the image file and drop it into the upload box

**Option B: Click to Browse**
- Click anywhere in the upload box
- Select an image from your computer or phone
- Click "Open"

#### 3. Review Your Image

- The uploaded image will appear in the preview area
- Make sure the leaf is clearly visible
- If you want to change the image, click the **×** button in the top-right corner

#### 4. Analyze the Disease

- Click the **"Analyze Disease"** button
- Wait a few seconds while Fito processes your image
- You'll see "Analyzing..." with a loading animation

#### 5. View Results

After analysis, you'll see:

**A. Disease Name**
- Large text showing the identified disease (e.g., "Early Blight" or "Healthy")

**B. Confidence Score**
- Percentage showing how confident the AI is (e.g., "92.45%")
- Higher percentage = more confident prediction

**C. Evaluation Metrics**
- Accuracy, Precision, Recall, and F1-Score
- These show how well the model performs

**D. All Predictions**
- List of all possible diseases with their confidence scores
- Helps you see alternative possibilities

**E. Disease Information**
- Detailed information about the identified disease
- Symptoms, visual cues, treatment, and prevention tips

---

## 📊 Understanding Your Results

### Confidence Levels

| Confidence | Meaning | What to Do |
|------------|---------|------------|
| **85-100%** | High confidence - Very reliable | Trust the result and follow recommendations |
| **70-84%** | Medium confidence - Fairly reliable | Consider the result but verify if possible |
| **Below 70%** | Low confidence - Uncertain | Retake photo or consult an expert |

### What If It Says "Unidentified"?

If Fito cannot identify the image, it means:
- The image might not be a tomato leaf
- The image quality is too poor
- The disease is not in our database

**What to do:**
1. Make sure you're photographing a tomato leaf
2. Take a clearer, better-lit photo
3. Try photographing a different leaf
4. Consult with an agricultural expert

---

## 📚 Using the Disease Library

### Step 1: Access the Library

- Click **"Information"** in the navigation menu
- You'll see a complete list of all diseases Fito can identify

### Step 2: Browse Diseases

For each disease, you'll find:

**Sample Images**
- 5 real photos showing what the disease looks like
- Scroll horizontally to see all images

**Disease Type Badge**
- Color-coded badge (Fungal, Bacterial, Viral, Pest, or Healthy)

**Severity Indicator**
- Visual bar showing how serious the disease is
- Low (green), Medium (yellow), High (orange), Very High (red)

**Symptoms**
- List of visible signs to look for
- Helps you identify diseases manually

**Visual Cues**
- Specific visual characteristics
- Colors, patterns, and textures

**Treatment**
- Recommended actions to treat the disease
- Includes chemical and organic options

**Prevention**
- How to prevent the disease from occurring
- Best practices for healthy crops

**Impact**
- Description of how the disease affects tomato plants
- Potential yield loss and economic impact

### Diseases Covered

1. **Healthy Tomato Leaf** - No disease present
2. **Bacterial Spot** - Bacterial infection
3. **Early Blight** - Fungal disease
4. **Late Blight** - Fungal disease
5. **Leaf Mold** - Fungal disease
6. **Septoria Leaf Spot** - Fungal disease
7. **Spider Mites** - Pest infestation
8. **Target Spot** - Fungal disease
9. **Yellow Leaf Curl Virus** - Viral disease
10. **Mosaic Virus** - Viral disease

---

## 📸 Tips for Best Results

### Taking Good Photos

✅ **DO:**
- Use good lighting (natural daylight is best)
- Focus on the leaf (not blurry)
- Fill the frame with the leaf
- Photograph the most affected area
- Take photos from directly above
- Use a plain background if possible

❌ **DON'T:**
- Take photos in dim light or darkness
- Use flash (can wash out colors)
- Photograph from too far away
- Include multiple leaves in one photo
- Take blurry or out-of-focus images
- Photograph wet or dirty leaves

### Image Requirements

- **Format:** JPG, JPEG, PNG
- **Size:** Any size (system will resize automatically)
- **Quality:** Clear and in focus
- **Subject:** Single tomato leaf
- **Lighting:** Well-lit, natural colors

---

## 🎓 Understanding Model Metrics

When you analyze an image, you'll see four evaluation metrics. Here's what they mean:

### 1. Accuracy (90.17%)

**What it is:** Overall correctness of the model  
**What it means:** Out of 100 predictions, about 90 are correct  
**Formula:** (Correct Predictions) / (Total Predictions)

### 2. Precision

**What it is:** How many disease predictions are actually correct  
**What it means:** When Fito says "diseased," it's usually right  
**Why it matters:** Reduces false alarms

### 3. Recall

**What it is:** How many actual diseases are caught  
**What it means:** Fito catches most real disease cases  
**Why it matters:** Ensures diseases aren't missed

### 4. F1-Score

**What it is:** Balance between Precision and Recall  
**What it means:** Overall reliability score  
**Why it matters:** Shows balanced performance

---

## 🔐 Admin Features (For Authorized Users Only)

### Logging In

1. Click **"Log-in"** in the navigation menu
2. Enter your admin email and password
3. Click **"Sign In"**
4. You'll be redirected to the admin dashboard

### Admin Dashboard

**What you can do:**
- View prediction statistics
- Manage the dataset
- See recent predictions
- Monitor system performance
- Update disease information

### Dataset Management

- View all uploaded images
- Organize images by disease class
- Delete incorrect predictions
- Export data for analysis

> **Note:** Admin access is restricted. Contact your system administrator if you need admin privileges.

---

## ❓ Frequently Asked Questions

### General Questions

**Q: Do I need to create an account?**  
A: No! Basic disease detection is free and doesn't require registration.

**Q: How accurate is Fito?**  
A: Fito has an overall accuracy of 90.17%, which is excellent for agricultural AI systems.

**Q: Can I use Fito on my phone?**  
A: Yes! Fito works on any device with a web browser.

**Q: Is my data private?**  
A: Yes. Images are processed securely and only stored if you're logged in as an admin.

### Technical Questions

**Q: What diseases can Fito detect?**  
A: Fito can identify 10 common tomato diseases plus healthy leaves (11 categories total).

**Q: How long does analysis take?**  
A: Usually 2-5 seconds, depending on your internet connection.

**Q: What if Fito gives a wrong result?**  
A: AI isn't perfect. Always verify with the disease library or consult an expert for important decisions.

**Q: Can I use Fito offline?**  
A: No, Fito requires an internet connection to process images.

### Usage Questions

**Q: Can I upload multiple images at once?**  
A: Currently, you can only analyze one image at a time.

**Q: What image formats are supported?**  
A: JPG, JPEG, and PNG formats are supported.

**Q: Why does it say "Unidentified"?**  
A: This means the image doesn't clearly match any disease in our database. Try a clearer photo or different leaf.

**Q: Can I save my results?**  
A: Results are displayed on screen. You can take a screenshot to save them.

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Issue: "Image not recognized" or "Unidentified"

**Solutions:**
1. Make sure you're photographing a tomato leaf (not other plants)
2. Take a clearer, better-lit photo
3. Photograph the diseased area more closely
4. Try a different leaf from the same plant

#### Issue: Upload button doesn't work

**Solutions:**
1. Refresh the page (F5 or Ctrl+R)
2. Try a different browser
3. Check your internet connection
4. Make sure the image file isn't corrupted

#### Issue: Analysis takes too long

**Solutions:**
1. Check your internet connection
2. Try a smaller image file
3. Refresh the page and try again
4. Contact support if the problem persists

#### Issue: Results don't make sense

**Solutions:**
1. Check the confidence score (low confidence = uncertain result)
2. Review the "All Predictions" section for alternatives
3. Compare with the disease library images
4. Retake the photo with better lighting

#### Issue: Can't access admin dashboard

**Solutions:**
1. Make sure you have admin credentials
2. Check that you're using the correct email and password
3. Contact your system administrator
4. Clear your browser cache and try again

---

## 📞 Getting Help

### Need Assistance?

**For Technical Support:**
- Click **"Contact"** in the navigation menu
- Fill out the contact form
- Describe your issue in detail
- Include screenshots if possible

**For Agricultural Advice:**
- Consult with local agricultural extension services
- Contact a plant pathologist or agronomist
- Visit your local Department of Agriculture office

**For System Issues:**
- Check the FAQ section first
- Try the troubleshooting steps above
- Contact your system administrator
- Report bugs through the contact form

---

## 🌱 Best Practices for Farmers

### Regular Monitoring

1. **Check plants weekly** - Early detection is key
2. **Photograph suspicious leaves** - Use Fito for quick diagnosis
3. **Keep records** - Track which diseases appear and when
4. **Act quickly** - Early treatment is more effective

### Disease Prevention

1. **Practice crop rotation** - Don't plant tomatoes in the same spot yearly
2. **Maintain plant spacing** - Good air circulation prevents disease
3. **Water properly** - Avoid wetting leaves, water at soil level
4. **Remove infected plants** - Prevent disease spread
5. **Use resistant varieties** - Choose disease-resistant tomato cultivars

### Using Fito Effectively

1. **Photograph multiple leaves** - Get a complete picture
2. **Compare results** - Check against the disease library
3. **Note confidence scores** - Higher is more reliable
4. **Verify before treatment** - Especially for expensive treatments
5. **Consult experts** - For serious or uncertain cases

---

## 📖 Glossary

**AI (Artificial Intelligence)** - Computer system that can learn and make decisions

**Confidence Score** - How certain the AI is about its prediction (0-100%)

**Disease Class** - Category of disease (e.g., Early Blight, Late Blight)

**F1-Score** - Balanced measure of model accuracy

**False Positive** - Healthy leaf incorrectly identified as diseased

**False Negative** - Diseased leaf incorrectly identified as healthy

**Fungal Disease** - Disease caused by fungi (e.g., Early Blight)

**Machine Learning** - AI technique where computers learn from data

**Precision** - Accuracy of positive predictions

**Recall** - Ability to find all positive cases

**Severity** - How serious a disease is (Low, Medium, High, Very High)

**Symptoms** - Visible signs of disease

**Unidentified** - Image that doesn't match any known disease

**Validation Accuracy** - How well the model performs on test data

---

## 🚀 Quick Start Checklist

Ready to use Fito? Follow this checklist:

- [ ] Open Fito website in your browser
- [ ] Navigate to the "Fito" page
- [ ] Take a clear photo of a tomato leaf
- [ ] Upload the image (drag-and-drop or click to browse)
- [ ] Click "Analyze Disease"
- [ ] Wait for results (2-5 seconds)
- [ ] Review the disease name and confidence score
- [ ] Read the disease information and recommendations
- [ ] Compare with the disease library if needed
- [ ] Take action based on the results

---

## 📊 System Specifications

### Technical Details

**Model Type:** Convolutional Neural Network (CNN)  
**Training Images:** 20,452 images  
**Validation Images:** 5,488 images  
**Image Size:** 192×192 pixels  
**Disease Classes:** 11 (10 diseases + healthy)  
**Overall Accuracy:** 90.17%  
**Training Epochs:** 35  
**Framework:** TensorFlow/Keras  

### Supported Browsers

✅ Google Chrome (recommended)  
✅ Mozilla Firefox  
✅ Safari  
✅ Microsoft Edge  
✅ Opera  

### Device Compatibility

✅ Desktop computers (Windows, Mac, Linux)  
✅ Laptops  
✅ Tablets (iPad, Android tablets)  
✅ Smartphones (iPhone, Android)  

---

## 🎓 Learning Resources

### Want to Learn More?

**About Tomato Diseases:**
- Visit the "Information" page for detailed disease profiles
- Check your local agricultural extension website
- Read tomato farming guides and manuals

**About AI and Machine Learning:**
- Explore how AI is used in agriculture
- Learn about image classification
- Understand how neural networks work

**About Fito:**
- Read the "About" page for system background
- Check the FAQ for common questions
- Contact support for specific inquiries

---

## 📝 Important Notes

### Limitations

⚠️ **Fito is a decision-support tool, not a replacement for expert advice**
- Always verify important diagnoses with an agronomist
- Use Fito as a first step in disease identification
- Combine AI results with your own observations

⚠️ **Image quality affects accuracy**
- Poor lighting, blur, or distance reduces accuracy
- Take multiple photos if you're unsure
- Follow the photography tips for best results

⚠️ **Not all diseases are covered**
- Fito identifies 10 common diseases
- Rare or new diseases may not be recognized
- "Unidentified" doesn't mean the plant is healthy

### Disclaimer

This system is provided for educational and informational purposes. While Fito achieves high accuracy (90.17%), it should not be the sole basis for agricultural decisions. Always consult with qualified agricultural professionals for disease diagnosis and treatment recommendations.

---

## 🎉 You're Ready!

Congratulations! You now know how to use Fito to identify tomato leaf diseases. 

**Remember:**
- Take clear, well-lit photos
- Check the confidence score
- Verify with the disease library
- Consult experts when needed
- Act quickly on disease detection

**Happy farming! 🌱🍅**

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**System:** Fito - Tomato Leaf Disease Identification System  
**Accuracy:** 90.17%  
**Support:** Available through the Contact page
