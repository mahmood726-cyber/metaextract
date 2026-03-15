# MetaExtract v1.0

**Browser-Based Effect Estimate Extractor**

Paste any abstract or results text, get structured effect estimates (HR, OR, RR, MD, SMD, events) with confidence scoring and highlighted source text. Or enter an NCT ID to fetch and parse CT.gov results automatically.

## Quick Start

1. Open `MetaExtract.html` in any browser
2. Paste abstract text (or enter NCT ID and click "Fetch CT.gov")
3. Click "Extract All"
4. Review extracted estimates with highlighted source text
5. Copy as JSON, CSV, or meta-analysis format

## Features

- **18 effect estimate patterns**: HR, OR, RR, IRR, MD, SMD, ARD, NNT (with CI)
- **Event count extraction**: "131/2366 vs 170/2379" patterns
- **P-value linking**: Auto-attaches p-values to nearest effect
- **CT.gov integration**: Enter NCT ID → fetch + parse results section
- **Source highlighting**: Every extracted number highlighted in original text
- **Confidence scoring**: AUTO_VERIFIED / SPOT_CHECK / NEEDS_REVIEW
- **Export**: JSON, CSV, meta-analysis format (for RevMan/metafor)
- **Text normalization**: Unicode dashes, European decimals, OCR artifacts
- **Plausibility checks**: Rejects implausible values automatically

## Ported From

TextExtractor engine from [LivingMeta](https://github.com/mahmood726-cyber/livingmeta) and [rct_data_extractor_v2](https://github.com/mahmood726-cyber/rct-extractor-v2).

## License

MIT
