// src/featureExtractor.js

export const extractFeatures = (boqText) => {
    const features = {};
  
    // Series extraction (e.g., SKN, Alucobond, Framing Member)
    const seriesMatch = boqText.match(/\b(SK[-\s]?\d+|Alucobond|Framing Member)\b/i);
    features.Series = seriesMatch ? seriesMatch[0].trim() : null;
  
    // Minimum Thickness extraction (e.g., mentions of thickness)
    const thicknessMatch = boqText.match(/(\b\d+\s*mm\b|\bminimum thickness of\s*\d+\s*mm\b|\bminimum\s*\d+\s*mm\b|\d+\s*mm thk\.|\bwind pressure\b)/i);
    features.MinThickness = thicknessMatch ? thicknessMatch[0].replace(/minimum thickness of|minimum|thk\./gi, '').trim() : null;
  
    // Approved Makes extraction (e.g., Saint Gobain, Alucobond)
    const makesMatch = boqText.match(/(Saint\s*Gobain|Alucobond|Hilti|Fischer|Secondary\s*Steel\s*-?\s*M\.S\. structure)/i);
    features.ApprovedMakes = makesMatch ? makesMatch[0].trim() : null;
  
    // Reflective Coating extraction
    const reflectiveCoatingMatch = boqText.match(/(surface\s*#\d+|Framing\s*member\s*-?\s*Finish)/i);
    features.ReflectiveCoating = reflectiveCoatingMatch ? `Reflective coating shall be on ${reflectiveCoatingMatch[0].trim()}` : null;
  
    // Glass extraction (e.g., insulated glass, laminated glass)
    const glassMatch = boqText.match(/(insulated\s*glass\s*unit|insulated\s*glass|Glass\s*type\s*-?\s*Single\s*glass\s*\/\s*Laminated|Laminated\s*Glass)/i);
    features.Glass = glassMatch ? glassMatch[0].trim() : null;
  
    // Special Seal extraction
    const specialSealMatch = boqText.match(/(hermetically\s*sealed(?:\s*with\s*the\s*two\s*lites\s*of\s*glass)?|hardware)/i);
    features.SpecialSeal = specialSealMatch ? specialSealMatch[0].trim() : null;
  
    // Air Gap extraction
    const airGapMatch = boqText.match(/(\b\d+\s*mm\s*air\s*gap\b|\b\d+\s*mm\s*air\s*space\b|Glass\s*type\s*-?\s*Single\s*glass\s*\/\s*Laminated)/i);
    features.AirGap = airGapMatch ? airGapMatch[0].replace(/air\s*space/i, 'air gap').trim() : null;
  
    // Spacer extraction
    const spacerMatch = boqText.match(/(black\s*aluminum\s*spacers|black\s*aluminium\s*spacers|SGP\s*\/\s*PVB)/i);
    features.Spacer = spacerMatch ? spacerMatch[0].trim() : null;
  
    // Special Bend/Shape extraction
    const specialBendShapeMatch = boqText.match(/(Bent\s*at\s*corners|toughened\s*clear\s*glass)/i);
    features.SpecialBendShape = specialBendShapeMatch ? specialBendShapeMatch[0].trim() : null;
  
    // Primary Sealant extraction
    const primarySealantMatch = boqText.match(/(Poly[-\s]*Isobutylene|Spider\s*fittings)/i);
    features.PrimarySealant = primarySealantMatch ? primarySealantMatch[0].trim() : null;
  
    // Secondary Silicon Sealant extraction
    const secondarySealantMatch = boqText.match(/(Dow\s*Corning\s*3362|DC\s*991H|Silicone|Sillicone)/i);
    features.SecondarySiliconSealant = secondarySealantMatch ? secondarySealantMatch[0].trim() : null;
  
    // Codal Reference extraction
    const codalReferenceMatch = boqText.match(/(BS\s*EN\s*\d+|IS\s*875\s*part\s*III|AS\s*1288)/i);
    features.CodalReference = codalReferenceMatch ? codalReferenceMatch[0].trim() : null;
  
    // Special Treatment extraction
    const specialTreatmentMatch = boqText.match(/(heat\s*strengthened|thermoplastic\s*core\s*of\s*anti\s*oxidant\s*LDPE|Type\s*of\s*canopy\s*-?\s*Glass\s*canopy)/i);
    features.SpecialTreatment = specialTreatmentMatch ? specialTreatmentMatch[0].trim() : null;
  
    return features;
  };
  