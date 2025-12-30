# Chapter V

## SUMMARY, CONCLUSIONS AND RECOMMENDATIONS

---

## SUMMARY

This study was entitled **"Fito: A Web-Based Tomato Leaf Disease Identification System,"** aimed to develop a system that can predict tomato leaf diseases through uploading tomato leaf images that can address and meet the farmers' needs in preventing the massive loss of tomato plantations. This early detection system is designed to provide convenience and accessibility, easy to use for farmers and other possible users, ensuring accurate information to address tomato diseases. This developed system can help reduce the time spent conducting studies to identify what kind of tomato diseases, providing a quick response of information and effective, sufficient solutions to prevent further spread.

The developed system shows a high capacity to predict an accurate result for different tomato diseases. The study used ISO/IEC 25010 standards to evaluate system quality, focusing on **Functional Suitability, Effectiveness, Efficiency, Usability, Reliability, Security, Compatibility, and Maintainability**. The system was designed to be accessible through a modern, responsive web interface, simple and intuitive for non-technical users, and accurate enough to provide meaningful decision support.

The classification model was trained on a comprehensive dataset of tomato leaf images, including 10 different disease classes plus healthy leaves, resulting in 11 total categories. The training utilized 20,452 training samples and 5,488 validation samples, with images preprocessed to 192×192 pixels. The model was trained for 35 epochs with a batch size of 20 and a learning rate of 0.0005, achieving excellent performance metrics suitable for real-world agricultural applications.

---

## CONCLUSIONS

This study of a web-based tomato leaf disease identification system highlights the critical role of timely identification in ensuring tomato crop health and productivity. The results from respondents, primarily farmers and agricultural practitioners, showed high satisfaction. The survey results show a high level of system **Functional Suitability, Effectiveness, Efficiency, Usability, Reliability, Security, Compatibility, and Maintainability**, with an overall mean indicating strong acceptance. The adopted method shows an accelerating performance of an **overall accuracy of 90.17%**, with excellent precision-recall and F1-score metrics, which shows that the process is best suitable for detecting diseases in tomato leaves.

The researcher's purpose for the system is to help farmers with the early detection of tomato diseases, improve crop management, and reduce detection time. It is designed to be accessible and easy to use, enabling quick identification and intervention. Key features include:

1. **Disease Detection Effectiveness** – The system achieves 90.17% overall accuracy across 11 classes (10 diseases + healthy), with individual class accuracies ranging from 78.38% (Healthy) to 99.67% (Unidentified), demonstrating robust classification capability.

2. **Reduced Response Time Efficiency** – The web-based interface provides instant predictions, eliminating the need for time-consuming manual inspection or waiting for expert consultations.

3. **High Usability for Non-Technical Users** – The intuitive interface allows farmers to simply upload images and receive clear, actionable results with disease information and management recommendations.

4. **System Reliability** – Consistent and accurate results ensure farmers can trust the system for making critical crop management decisions.

5. **Data Security** – The system protects farm data and user information through secure authentication and proper access controls.

6. **Compatibility** – The web-based platform works across existing tools and devices, making it accessible to users with various technical setups.

7. **Ease of Maintenance** – The well-documented codebase and modular architecture make it a valuable, long-term solution for tomato disease management.

The system's adherence to ISO/IEC 25010 standards assures that it meets quality benchmarks in software performance, usability, and security. The model demonstrates particularly strong performance in identifying specific diseases such as Mosaic Virus (98.44% accuracy), Unidentified cases (99.67% accuracy), Leaf Mold (95.53% accuracy), and Yellow Leaf Curl Virus (93.88% accuracy), while maintaining acceptable performance across all disease categories.

---

## RECOMMENDATIONS

The following recommendations were presented based on the findings and conclusion of the study **"Fito: A Web-Based Tomato Leaf Disease Identification System"**. The system has proven to be effective, accurate, and beneficial in helping farmers detect and manage tomato diseases at an early stage. The findings indicate that the technology can significantly improve disease control and crop productivity, making it a valuable tool in modern tomato farming practices.

### 1. Expand Implementation Beyond Initial Deployment

Given these results, it is strongly recommended that the implementation of **"Fito: A Web-Based Tomato Leaf Disease Identification System"** be extended beyond the initial deployment area. Large-scale tomato plantations, as well as smallholder and independent tomato farmers, can greatly benefit from this innovation. With appropriate training and support, the system can help improve disease management even in rural farming communities.

### 2. Integration with Academic Institutions

Agricultural institutions offering agriculture-related courses are in a strategic position to utilize this system for academic and research purposes. Through field application and integration into agricultural curricula, students and faculty can contribute to the system's improvement while gaining valuable hands-on experience in smart farming technologies. The system can serve as:

- A practical teaching tool for plant pathology courses
- A research platform for studying disease patterns and progression
- A demonstration of applied machine learning in agriculture
- A foundation for student projects and thesis work

### 3. Continuous Model Improvement and Dataset Expansion

To maintain and improve the system's 90.17% accuracy rate, continuous model refinement is essential:

- **Expand the dataset** with images from diverse geographical locations, different growth stages, and varying environmental conditions
- **Address class-specific weaknesses** by collecting more samples for classes with lower performance (e.g., Healthy leaves at 78.38% accuracy, Target Spot at 84.46% accuracy)
- **Implement periodic retraining** using updated datasets and improved architectures
- **Collect real-world feedback** from farmers to identify edge cases and difficult-to-classify scenarios

### 4. Enhance User Training and Support

Provide comprehensive training programs for farmers and agricultural technicians:

- Develop user manuals and video tutorials on proper image capture techniques
- Conduct training sessions on interpreting system outputs and confidence scores
- Create guidelines for different lighting conditions and camera angles
- Establish a support system for addressing user questions and technical issues

### 5. Strengthen Cross-Platform Compatibility

Optimize the system for various devices and network conditions:

- Ensure consistent performance across smartphones, tablets, and desktop computers
- Optimize for low-bandwidth environments common in rural areas
- Test compatibility with different browsers and operating systems
- Consider developing a progressive web app (PWA) or native mobile application for offline functionality

### 6. Implement Confidence Threshold System

Establish clear confidence levels for predictions to guide user decision-making:

- **High Confidence (≥85%)**: Display prediction with treatment recommendations
- **Medium Confidence (70-84%)**: Suggest expert verification and show alternative possibilities
- **Low Confidence (<70%)**: Recommend expert consultation and image quality improvement

### 7. Integration with Extension Services and Agricultural Programs

Collaborate with agricultural extension services and government programs:

- Partner with Department of Agriculture extension offices
- Integrate with existing agricultural advisory systems
- Provide the system as a complementary tool for agricultural extension workers
- Establish feedback mechanisms for continuous improvement

### 8. Future Research and Development Directions

Explore advanced features and capabilities:

- **Severity Assessment**: Implement disease severity classification (mild, moderate, severe)
- **Multi-Disease Detection**: Enable identification of multiple diseases on a single leaf
- **Temporal Tracking**: Allow users to track disease progression over time
- **Treatment Effectiveness**: Monitor and evaluate treatment outcomes
- **Localized Recommendations**: Provide region-specific treatment guidelines based on local agricultural practices
- **Integration with IoT**: Connect with environmental sensors for comprehensive crop monitoring
- **Expand to Other Crops**: Adapt the system for other vegetable crops beyond tomatoes

### 9. Establish Quality Assurance and Monitoring

Implement ongoing performance monitoring:

- Track prediction accuracy in real-world deployments
- Monitor user feedback and satisfaction metrics
- Analyze misclassification patterns to identify improvement areas
- Maintain expert review system for low-confidence predictions
- Conduct periodic field validation studies

### 10. Ensure Long-Term Sustainability

Develop strategies for sustainable operation and maintenance:

- Establish clear data governance and privacy policies
- Maintain strong security practices and regular security audits
- Create a sustainable funding model for ongoing development and support
- Build a community of users and contributors for knowledge sharing
- Document all system components for future maintainers

---

## CONCLUSION

To conclude, **"Fito: A Web-Based Tomato Leaf Disease Identification System"** has demonstrated strong potential to revolutionize tomato disease management. With an overall accuracy of **90.17%** and excellent performance across multiple disease categories, the system provides reliable, accessible, and timely disease identification for farmers and agricultural practitioners.

The system successfully addresses the critical need for early disease detection in tomato cultivation, offering a practical solution that combines machine learning technology with user-friendly design. The adherence to ISO/IEC 25010 quality standards ensures that the system meets professional benchmarks for software quality, usability, and reliability.

With further development, institutional collaboration, and responsible implementation, this system can be a reliable tool, not only for large plantations but also for small-scale farmers and academic institutions. The combination of high accuracy, ease of use, and comprehensive disease information makes Fito a valuable asset in the fight against tomato crop diseases.

Overall, the system is **highly recommended for continued use and further research**, as it offers practical solutions to real-world agricultural challenges. By empowering farmers with accessible technology and accurate information, Fito contributes to improved crop management, reduced losses, and enhanced food security in tomato production.

---

**Document Information:**
- **System Name:** Fito - Tomato Leaf Disease Identification System
- **Overall Model Accuracy:** 90.17%
- **Total Disease Classes:** 11 (10 diseases + healthy)
- **Evaluation Framework:** ISO/IEC 25010
- **Document Version:** 1.0
- **Date:** December 2025
