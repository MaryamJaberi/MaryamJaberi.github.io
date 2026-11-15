import { TaskSession, ModelConfig } from '../types/studio';

export const DEFAULT_MODEL_CONFIG: ModelConfig = {
  modelId: 'gemini-2.5-flash',
  modelName: 'Gemini 2.5 Flash',
  temperature: 0.7,
  topP: 0.95,
  maxOutputTokens: 2048,
  systemInstruction: 'You are an advanced Google AI Studio assistant. Provide clear, well-structured, evidence-backed answers. Use concise paragraphs, bullet points for key items, and high-quality runnable code snippets with proper language annotations.',
  safetyLevel: 'standard',
};

export const INITIAL_SESSIONS: TaskSession[] = [
  {
    id: 'session-1',
    title: 'Paleoclimatic Shifts Analysis',
    category: 'Research',
    createdAt: '2026-09-18T12:00:00Z',
    updatedAt: '2026-09-18T13:30:00Z',
    pinned: true,
    modelConfig: { ...DEFAULT_MODEL_CONFIG },
    messages: [
      {
        id: 'msg-1',
        role: 'user',
        content: 'Explain the climatic transitions of the Paleocene-Eocene Thermal Maximum (PETM) and provide a concise Python function to calculate carbon isotope excursions.',
        timestamp: '1:15 PM',
        status: 'success',
      },
      {
        id: 'msg-2',
        role: 'assistant',
        content: `The Paleocene-Eocene Thermal Maximum (PETM) occurred approximately 56 million years ago. It represents one of the most abrupt global warming events in geological history, characterized by a rapid release of thousands of gigatons of carbon into Earth's exogenic reservoir.

During this interval, global sea surface temperatures rose by approximately 5°C to 8°C. This temperature spike triggered widespread benthic foraminiferal extinctions, marked poleward migrations of terrestrial flora, and substantial ocean acidification.

Key geochemical markers and ecological outcomes include:
• Negative Carbon Isotope Excursion (CIE): A pronounced 3‰ to 5‰ drop in δ13C values observed in marine and terrestrial carbonate strata.
• Extreme Ocean Acidification: Marked dissolution of deep-sea calcium carbonate deposits globally.
• Accelerated Hydrological Cycling: Intensified continental weathering and localized monsoonal expansion.

Here is a verified Python function for calculating isotope excursions and normalizing baseline signatures:`,
        timestamp: '1:16 PM',
        tokenCount: {
          prompt: 34,
          completion: 218,
        },
        codeBlocks: [
          {
            id: 'code-1',
            language: 'python',
            title: 'carbon_isotope_excursion.py',
            code: `import numpy as np

def calculate_cie(baseline_values: list[float], event_values: list[float]) -> dict:
    """
    Computes the Carbon Isotope Excursion (CIE) magnitude
    and standardized statistical confidence interval.
    """
    baseline_mean = float(np.mean(baseline_values))
    event_nadir = float(np.min(event_values))
    delta_cie = event_nadir - baseline_mean
    
    return {
        "baseline_mean_permil": round(baseline_mean, 2),
        "nadir_permil": round(event_nadir, 2),
        "cie_magnitude_permil": round(abs(delta_cie), 2),
        "anomaly_direction": "negative" if delta_cie < 0 else "positive"
    }

# Example validation on marine core samples
sample_baseline = [2.8, 2.9, 3.1, 2.7, 3.0]
sample_event = [-0.8, -1.2, -0.4, 0.1]
result = calculate_cie(sample_baseline, sample_event)
print("Calculated CIE:", result)`,
          },
        ],
        status: 'success',
      },
    ],
  },
  {
    id: 'session-2',
    title: 'TypeScript GeoJSON Bounds Parser',
    category: 'Code',
    createdAt: '2026-09-17T15:20:00Z',
    updatedAt: '2026-09-17T16:05:00Z',
    pinned: false,
    modelConfig: { ...DEFAULT_MODEL_CONFIG, temperature: 0.2 },
    messages: [
      {
        id: 'msg-3',
        role: 'user',
        content: 'Write a type-safe TypeScript function to compute the bounding box (BBox) of a GeoJSON FeatureCollection without external dependencies.',
        timestamp: '4:02 PM',
        status: 'success',
      },
      {
        id: 'msg-4',
        role: 'assistant',
        content: `A bounding box in geospatial standards is represented as a 4-tuple [minX, minY, maxX, maxY]. In geographic coordinates, this corresponds directly to [westLng, southLat, eastLng, northLat].

The algorithm handles coordinates across standard Point, LineString, and Polygon geometries safely. It avoids mutations and accounts for multi-dimensional coordinate nesting.

Core features of this implementation:
• Strict TypeScript typings for coordinates and GeoJSON geometries.
• Iterative traversal without deep recursion to avoid call stack limits on large datasets.
• Edge-case handling for empty collections and single-point entities.`,
        timestamp: '4:03 PM',
        tokenCount: {
          prompt: 28,
          completion: 185,
        },
        codeBlocks: [
          {
            id: 'code-2',
            language: 'typescript',
            title: 'geoBounds.ts',
            code: `export type BoundingBox = [minLng: number, minLat: number, maxLng: number, maxLat: number];

export interface GeoCoordinate {
  lng: number;
  lat: number;
}

export function computeGeoBounds(coordinates: [number, number][]): BoundingBox {
  if (coordinates.length === 0) {
    throw new Error("Cannot compute bounding box for empty coordinate array.");
  }

  let minLng = Infinity;
  let minLat = Infinity;
  let maxLng = -Infinity;
  let maxLat = -Infinity;

  for (const [lng, lat] of coordinates) {
    if (lng < minLng) minLng = lng;
    if (lat < minLat) minLat = lat;
    if (lng > maxLng) maxLng = lng;
    if (lat > maxLat) maxLat = lat;
  }

  return [minLng, minLat, maxLng, maxLat];
}`,
          },
        ],
        status: 'success',
      },
    ],
  },
  {
    id: 'session-3',
    title: 'Achaemenid & Roman Administration',
    category: 'Historical',
    createdAt: '2026-09-16T09:10:00Z',
    updatedAt: '2026-09-16T10:00:00Z',
    pinned: false,
    modelConfig: { ...DEFAULT_MODEL_CONFIG, temperature: 0.6 },
    messages: [
      {
        id: 'msg-5',
        role: 'user',
        content: 'Compare the administrative delegation mechanisms of the Achaemenid Satrapy system with the Roman Provincial system.',
        timestamp: '9:12 AM',
        status: 'success',
      },
      {
        id: 'msg-6',
        role: 'assistant',
        content: `Both the Achaemenid Empire and the Roman Empire governed multi-ethnic territories spanning millions of square kilometers. Each empire maintained cohesion by balancing centralized royal authority with regional autonomy.

The Achaemenid satrapy framework, formalized by Darius I, emphasized local cultural preservation alongside fixed taxation. The Royal Road communications network and the "Eye of the King" inspectors ensured accountability without micro-managing regional customs.

Key comparative dimensions:
• Bureaucratic Structure: Achaemenid satraps held civil command while separate military generals reported directly to Susa, preventing regional insurrections. Roman provinces were governed by proconsuls or imperial legates who often held unified civil and military powers.
• Legal Pluralism: The Persian court recognized Babylonian, Egyptian, and Jewish domestic legal codes. Rome gradually exported the Roman legal apparatus, culminating in the Antonine Constitution of 212 CE.
• Fiscal Infrastructure: Darius established standardized gold darics and silver sigloi with surveyed regional tribute quotes. Rome established direct census-based land and poll taxation.`,
        timestamp: '9:14 AM',
        tokenCount: {
          prompt: 26,
          completion: 240,
        },
        status: 'success',
      },
    ],
  },
];

export const STARTER_PROMPTS = [
  {
    category: 'Geosciences',
    title: 'Paleoclimatic Modeling',
    prompt: 'Summarize the Milankovitch cycles and explain how eccentricity, obliquity, and precession drive glacial-interglacial cycles.',
  },
  {
    category: 'Data Science',
    title: 'Python Time-Series Tool',
    prompt: 'Write a clean Python script using pandas and numpy to calculate rolling 30-day volatility and plot anomalies in environmental records.',
  },
  {
    category: 'World History',
    title: 'Silk Road Economic Networks',
    prompt: 'Analyze the major overland trade routes of the Silk Road during the Tang Dynasty and Abbasid Caliphate, detailing currency and commodities.',
  },
  {
    category: 'Architecture',
    title: 'System Design for Geospatial API',
    prompt: 'Design a RESTful API specification for querying historical territorial boundaries with spatial indexing, caching, and rate limiting.',
  },
];
