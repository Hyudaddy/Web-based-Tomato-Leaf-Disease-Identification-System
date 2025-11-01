export interface DiseaseInfo {
  id: string
  name: string
  scientificName: string
  type: 'Fungal' | 'Bacterial' | 'Viral' | 'Pest' | 'Healthy'
  symptoms: string[]
  visualCues: string[]
  conditions: string[]
  impact: string
  treatment: string[]
  prevention: string[]
  severity: 'Low' | 'Medium' | 'High' | 'Critical'
  images?: string[]
  description?: string
}

export const diseaseDatabase: DiseaseInfo[] = [
  {
    id: 'healthy',
    name: 'Healthy Tomato Leaf',
    scientificName: 'Solanum lycopersicum (Healthy)',
    type: 'Healthy',
    symptoms: [
      'Uniform green color',
      'No lesions, spots, or yellowing',
      'Normal leaf structure and firmness'
    ],
    visualCues: [
      'Smooth edges',
      'Consistent texture',
      'No discoloration'
    ],
    conditions: [
      'Optimal growing conditions',
      'Proper nutrition and watering',
      'Good air circulation'
    ],
    impact: 'Baseline for healthy plant growth',
    treatment: [
      'Continue current care practices',
      'Maintain optimal growing conditions'
    ],
    prevention: [
      'Regular monitoring',
      'Proper spacing',
      'Good air circulation',
      'Balanced nutrition'
    ],
    severity: 'Low'
  },
  {
    id: 'early-blight',
    name: 'Early Blight',
    scientificName: 'Alternaria solani',
    type: 'Fungal',
    symptoms: [
      'Brown to black concentric rings ("target spots") on older leaves',
      'Yellowing around affected areas',
      'Leaves dry up and fall prematurely'
    ],
    visualCues: [
      'Circular lesions with dark concentric rings',
      'Starts from lower leaves, progressing upward'
    ],
    conditions: [
      'Warm (24–29°C) temperatures',
      'Humid environments',
      'Poor air circulation'
    ],
    impact: 'Reduces photosynthesis and yield',
    treatment: [
      'Remove infected leaves immediately',
      'Apply copper-based fungicides',
      'Improve air circulation',
      'Avoid overhead watering'
    ],
    prevention: [
      'Crop rotation',
      'Proper plant spacing',
      'Remove plant debris',
      'Use resistant varieties'
    ],
    severity: 'Medium'
  },
  {
    id: 'late-blight',
    name: 'Late Blight',
    scientificName: 'Phytophthora infestans',
    type: 'Fungal',
    symptoms: [
      'Large, irregular, water-soaked patches on leaves',
      'Underside of leaves may show white fungal growth',
      'Rapid leaf collapse in humid weather'
    ],
    visualCues: [
      'Greasy dark-green to brown lesions',
      'Often expanding rapidly'
    ],
    conditions: [
      'Cool, wet conditions (15–22°C)',
      'High humidity',
      'Poor drainage'
    ],
    impact: 'Can destroy entire plant and fruit quickly',
    treatment: [
      'Apply systemic fungicides immediately',
      'Remove infected plant parts',
      'Improve drainage',
      'Reduce humidity'
    ],
    prevention: [
      'Avoid overhead watering',
      'Improve drainage',
      'Use resistant varieties',
      'Monitor weather conditions'
    ],
    severity: 'Critical'
  },
  {
    id: 'septoria-leaf-spot',
    name: 'Septoria Leaf Spot',
    scientificName: 'Septoria lycopersici',
    type: 'Fungal',
    symptoms: [
      'Numerous small (1–3 mm) round grayish spots with dark borders',
      'Typically appear on lower leaves first',
      'Leaves turn yellow and fall off'
    ],
    visualCues: [
      'Dense spotting across leaf surfaces',
      'Often uniform distribution'
    ],
    conditions: [
      'High humidity',
      'Rain splashes',
      'Poor air circulation'
    ],
    impact: 'Severe defoliation, reduced fruit yield',
    treatment: [
      'Remove infected leaves',
      'Apply fungicide',
      'Improve air circulation',
      'Avoid overhead watering'
    ],
    prevention: [
      'Crop rotation',
      'Proper spacing',
      'Remove plant debris',
      'Use drip irrigation'
    ],
    severity: 'High'
  },
  {
    id: 'bacterial-spot',
    name: 'Bacterial Spot',
    scientificName: 'Xanthomonas campestris pv. vesicatoria',
    type: 'Bacterial',
    symptoms: [
      'Small, dark, water-soaked spots on leaves and fruits',
      'Lesions turn brown with yellow halos',
      'Rough, scabby fruit surfaces'
    ],
    visualCues: [
      'Leaf margins often torn or dry near lesions',
      'Spots with yellow halos'
    ],
    conditions: [
      'Warm, moist weather',
      'High humidity',
      'Plant wounds'
    ],
    impact: 'Affects both foliage and fruit marketability',
    treatment: [
      'Apply copper-based bactericides',
      'Remove infected plant parts',
      'Improve air circulation',
      'Avoid working when plants are wet'
    ],
    prevention: [
      'Use disease-free seeds',
      'Avoid overhead watering',
      'Proper spacing',
      'Crop rotation'
    ],
    severity: 'High'
  },
  {
    id: 'leaf-mold',
    name: 'Leaf Mold',
    scientificName: 'Cladosporium fulvum',
    type: 'Fungal',
    symptoms: [
      'Pale green or yellow spots on upper leaf surfaces',
      'Olive-green to brown mold growth on undersides',
      'Leaves curl, dry, and drop'
    ],
    visualCues: [
      '"Velvety" texture on leaf undersides',
      'Yellow spots on upper surfaces'
    ],
    conditions: [
      'High humidity',
      'Poor air circulation',
      'Greenhouse conditions'
    ],
    impact: 'Common in greenhouses; affects photosynthesis',
    treatment: [
      'Improve ventilation',
      'Apply fungicide',
      'Remove infected leaves',
      'Reduce humidity'
    ],
    prevention: [
      'Proper ventilation',
      'Avoid overcrowding',
      'Monitor humidity levels',
      'Use resistant varieties'
    ],
    severity: 'Medium'
  },
  {
    id: 'yellow-leaf-curl-virus',
    name: 'Yellow Leaf Curl Virus',
    scientificName: 'TYLCV',
    type: 'Viral',
    symptoms: [
      'Curling and yellowing of young leaves',
      'Stunted plant growth and reduced fruit set',
      'Thickened leaf texture'
    ],
    visualCues: [
      'Distorted leaf shape',
      'Bright yellow veins'
    ],
    conditions: [
      'High whitefly population',
      'Warm temperatures',
      'Poor vector control'
    ],
    impact: 'Severe yield losses (up to 100%)',
    treatment: [
      'Remove infected plants immediately',
      'Control whitefly populations',
      'Use systemic insecticides',
      'No cure for infected plants'
    ],
    prevention: [
      'Use resistant varieties',
      'Control whitefly vectors',
      'Remove infected plants',
      'Use reflective mulches'
    ],
    severity: 'Critical'
  },
  {
    id: 'mosaic-virus',
    name: 'Mosaic Virus',
    scientificName: 'Tomato Mosaic Virus / Tobacco Mosaic Virus',
    type: 'Viral',
    symptoms: [
      'Mosaic-like mottling of light and dark green on leaves',
      'Leaf distortion and blistering',
      'Reduced plant vigor'
    ],
    visualCues: [
      'Patchy "mosaic" color pattern',
      'Light/dark green areas'
    ],
    conditions: [
      'Spread via contact',
      'Contaminated tools',
      'Infected seeds'
    ],
    impact: 'Long-lasting infection; no cure',
    treatment: [
      'Remove infected plants',
      'Disinfect tools',
      'No chemical treatment available'
    ],
    prevention: [
      'Use virus-free seeds',
      'Disinfect tools regularly',
      'Avoid contact with infected plants',
      'Control aphid vectors'
    ],
    severity: 'High'
  },
  {
    id: 'target-spot',
    name: 'Target Spot',
    scientificName: 'Corynespora cassiicola',
    type: 'Fungal',
    symptoms: [
      'Circular brown spots with lighter centers (target-like)',
      'Spots may coalesce forming large necrotic patches',
      'Severe infection leads to defoliation'
    ],
    visualCues: [
      'Lesions with concentric zones',
      'Often dry and cracked'
    ],
    conditions: [
      'Warm and wet weather',
      'High humidity',
      'Poor air circulation'
    ],
    impact: 'Defoliation, lower yield, poor fruit development',
    treatment: [
      'Apply fungicide',
      'Remove infected leaves',
      'Improve air circulation',
      'Avoid overhead watering'
    ],
    prevention: [
      'Proper spacing',
      'Good air circulation',
      'Crop rotation',
      'Remove plant debris'
    ],
    severity: 'High'
  },
  {
    id: 'spider-mites',
    name: 'Spider Mites',
    scientificName: 'Tetranychus urticae',
    type: 'Pest',
    symptoms: [
      'Tiny yellow or white specks on leaves',
      'Webbing on undersides of leaves',
      'Leaves turn bronze or curl, eventually dropping'
    ],
    visualCues: [
      'Fine silk-like web',
      'Stippling damage on leaves'
    ],
    conditions: [
      'Hot, dry environments',
      'Low humidity',
      'Stressed plants'
    ],
    impact: 'Weakens plants, reduces photosynthesis',
    treatment: [
      'Apply miticide',
      'Increase humidity',
      'Use beneficial insects',
      'Remove heavily infested leaves'
    ],
    prevention: [
      'Regular monitoring',
      'Maintain proper humidity',
      'Introduce beneficial insects',
      'Avoid over-fertilization'
    ],
    severity: 'Medium'
  }
]

export const getDiseaseInfo = (diseaseName: string): DiseaseInfo | undefined => {
  return diseaseDatabase.find(disease => 
    disease.name.toLowerCase().includes(diseaseName.toLowerCase()) ||
    disease.id === diseaseName.toLowerCase().replace(/\s+/g, '-')
  )
}
