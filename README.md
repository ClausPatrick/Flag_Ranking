# Flag Entropy Analysis Project

## Overview

This project explores the entropy of national flags using advanced image processing techniques. By analyzing the spectral characteristics of flag images, we create a unique ranking that quantifies the visual complexity of different national flags.

## Key Features

- Spectral entropy calculation for flag images
- Color-weighted entropy analysis
- Comprehensive flag complexity ranking
- Supports various image sources (currently configured for Wikimedia Commons)

## Methodology

### Entropy Calculation
The project uses a custom `color_weighted_spectral_entropy()` function that:
- Applies Fourier Transform to each color channel
- Calculates entropy across Blue, Green, and Red channels
- Provides a balanced measure of flag complexity

### Ranking Process
1. Load flag images from a specified directory
2. Calculate spectral entropy for each flag
3. Generate a ranked list from most to least complex

## Requirements

### Dependencies
see pip_requirements.txt

### Installation
```bash
pip install pip_requirements.txt
```

## Project structure

```
flag-entropy-analysis/
│
├── download_flags.py      # Script to download flag images
├── flag_entropy.py        # Main entropy calculation script
├── flag_ranking.txt       # Output ranking of flag complexities
└── README.md              # Project documentation
```

## Sanity Checks

The script includes two built-in sanity checks:

1. white_field: A completely white image (expected to be near top)
2. random_distribution: A randomly generated image (expected to be near bottom)

## Interesting Observations

- Flags with simple color bands tend to have lower entropy
- Complex, multi-colored flags show higher entropy values
- The method captures both color and structural complexity


