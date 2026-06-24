# Image Integration Guide for Information Page

## Current Setup

The Information page is ready to display tomato leaf images from your dataset. The folder structure is already organized by disease type:

```
assets/tomato leaf/
├── healthy/
│   ├── 1af0bfe1-4bcf-4b8b-be66-5d0953eb647e___GH_HL Leaf 482.2.JPG
│   ├── 1bfeed83-f119-46cd-b806-0e17e1dae136___RS_HL 0017_180deg.JPG
│   ├── 1ca23194-53c1-44a9-973a-39aa073f4a33___RS_HL 0058_180deg.JPG
│   ├── 1ca3c77d-13d8-43cc-929f-9c3a79e5dd1b___RS_HL 0250.JPG
│   └── 1d024f2a-0ceb-4560-81fc-1114e6341f02___RS_HL 0431_flipTB.JPG
├── early blight/ [5 images]
├── late blight/ [5 images]
├── septoria leaf spot/ [5 images]
├── bacterial spot/ [5 images]
├── leaf mold/ [5 images]
├── yellow curl virus/ [5 images]
├── mosaic virus/ [5 images]
├── target spot/ [5 images]
└── spider mites/ [5 images]
```

## Current Implementation

The Information page displays placeholder image containers (5 images per disease) positioned horizontally in a single line, just as requested. The page features:

✅ Clean, simple layout (no cards)
✅ Typewriter effect on title
✅ Smooth scroll animations with AnimatedSection
✅ All disease information displayed
✅ Model evaluation metrics section
✅ Ready for actual images

## To Add Real Images

Once you're ready to add the actual tomato leaf images:

1. Copy 5 representative images from each disease folder in `assets/tomato leaf/` 
2. Place them in `frontend/public/diseases/[disease-folder]/` structure
3. Rename to simple numbers: 1.jpg, 2.jpg, 3.jpg, 4.jpg, 5.jpg
4. Update the placeholder div in the component to use `<Image>` tags

## File Location

**Main Information Page:** `frontend/src/app/information/page.tsx`

The page is fully functional and styled to match your existing pages (About, Home, etc.) with:
- Proper typography and spacing
- Typewriter effect
- Scroll animations
- Responsive design
- Green accent colors (#47f793)
