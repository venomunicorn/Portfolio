import React from 'react';
import TopicSection from './TopicSection';

// Complete syllabus data structure
const SYLLABUS_DATA = {
  "QUANTITATIVE APTITUDE (Pre + Mains)": [
    "Number System - Types of Numbers: Natural, Whole, Integers, Rational, Irrational, Real",
    "Divisibility Rules",
    "Factorization & Prime Factorization", 
    "HCF & LCM (word problems)",
    "Remainder Theorem",
    "Unit Digit & Cyclicity",
    "Simplification & Approximation",
    "Surds & Indices",
    "Fractions, Decimals",
    "Percentage",
    "Profit & Loss",
    "Discount & Marked Price",
    "Simple Interest & Compound Interest",
    "Ratio & Proportion",
    "Partnership",
    "Averages",
    "Mixture & Alligation",
    "Time & Work",
    "Work & Wages",
    "Pipes & Cisterns",
    "Time, Speed & Distance",
    "Boats & Streams",
    "Trains",
    "Problems on Ages",
    "Linear Equations",
    "Quadratic Equations",
    "Polynomials",
    "Factorization",
    "Inequalities",
    "Lines & Angles",
    "Triangles (Properties, Types, Congruence, Similarity)",
    "Circles (Tangent, Chord, Secant)",
    "Polygons (Properties)",
    "Quadrilaterals",
    "2D Mensuration: Triangle, Square, Rectangle, Circle",
    "3D Mensuration: Cube, Cuboid, Cylinder, Cone, Sphere",
    "Trigonometric Ratios",
    "Trigonometric Identities",
    "Heights & Distances",
    "Statistics: Mean, Median, Mode",
    "Data Interpretation: Pie Charts, Bar Graphs",
    "Probability",
    "Permutation & Combination"
  ],
  
  "REASONING ABILITY (Pre + Mains)": [
    "Analogy",
    "Classification / Odd One Out",
    "Number Series",
    "Alphabet Series",
    "Coding-Decoding (Old & New Pattern)",
    "Blood Relations",
    "Direction & Distance",
    "Ranking & Ordering",
    "Syllogism",
    "Statement & Conclusion",
    "Statement & Assumption",
    "Statement & Arguments",
    "Cause & Effect",
    "Seating Arrangement (Linear)",
    "Seating Arrangement (Circular)",
    "Puzzle Test",
    "Input-Output",
    "Coded Inequalities",
    "Decision Making",
    "Mirror Image",
    "Water Image",
    "Embedded Figures",
    "Figure Series",
    "Paper Folding & Cutting",
    "Venn Diagrams"
  ],

  "ENGLISH LANGUAGE (Pre + Mains)": [
    "Synonyms & Antonyms",
    "One Word Substitution",
    "Idioms & Phrases",
    "Spelling Correction",
    "Parts of Speech",
    "Tenses",
    "Subject-Verb Agreement",
    "Articles",
    "Prepositions",
    "Active & Passive Voice",
    "Direct & Indirect Speech",
    "Error Spotting",
    "Sentence Improvement",
    "Reading Comprehension",
    "Cloze Test",
    "Fill in the Blanks",  
    "Para Jumbles",
    "Sentence Rearrangement"
  ],

  "GENERAL AWARENESS / GENERAL KNOWLEDGE": [
    "Indian History (Ancient, Medieval, Modern)",
    "Indian National Movement",
    "Geography (India & World)",
    "Indian Polity & Constitution",
    "Economy Basics",
    "Physics Basics",
    "Chemistry Basics", 
    "Biology Basics",
    "Art & Culture",
    "Environment & Ecology",
    "Sports",
    "Awards & Honours",
    "Books & Authors",
    "Important Days & Themes",
    "International Organizations",
    "Banking Awareness",
    "Computer Knowledge",
    "Current Affairs - National",
    "Current Affairs - International",
    "Government Schemes"
  ],

  "DESCRIPTIVE SECTION (Tier 3 / Mains)": [
    "Essay Writing - Economic Issues",
    "Essay Writing - Social Topics", 
    "Essay Writing - Current Issues",
    "Essay Writing - Technology",
    "Letter Writing - Formal",
    "Letter Writing - Informal",
    "Precis Writing"
  ],

  "INTERVIEW (IBPS PO / MHA IB)": [
    "Self Introduction",
    "Academic Background Discussion",
    "Work Experience Discussion",
    "Why Banking / Why Government Job",
    "Current Affairs Questions",
    "HR Questions - Strengths & Weaknesses",
    "Banking/Finance Basics",
    "National Security Scenarios"
  ],

  "STATE SPECIFIC (Patwari/VDO)": [
    "State History",
    "State Geography", 
    "State Culture & Traditions",
    "State Government Schemes",
    "Rural Development",
    "Panchayati Raj",
    "Agriculture Basics",
    "Hindi Grammar",
    "Local Current Affairs"
  ]
};

function SyllabusDisplay() {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8 text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          📚 Complete Syllabus Coverage
        </h2>
        <p className="text-gray-600">
          Click on any topic to expand and see subtopics. Use Start/Finish buttons to track your progress.
        </p>
      </div>

      {Object.entries(SYLLABUS_DATA).map(([topic, subtopics], index) => (
        <TopicSection
          key={index}
          topic={topic}
          subtopics={subtopics}
          topicId={topic.replace(/\s+/g, '_').toLowerCase()}
        />
      ))}
    </div>
  );
}

export default SyllabusDisplay;
