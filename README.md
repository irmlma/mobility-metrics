# mobility-metrics

## Install

Install the package in edit mode using:
```
pip install -e .
```

## Evaluate

### Entropy
- Random Entropy
- Uncorrelated Entropy
- Real Entropy
Run 
```
python example/run_entropy.py
```
for examples of calculating entropy for location traces. 

### Basic metrics
Run 
```
python example/run_metrics.py
```
for examples of calculating basic mobility metrics. The metric can be specified with the input arguement `metric`, accepting one of the  arguements [`rg`, `locf`, `jump`,`wait`]: 
- Location visitation frquency. 
- Radius of gyration. Radius of gyration calculation receives the following parameter:
    - `method` of [`duration`, `count`]. `count` calculates with visitation frequency of locations, and `duration` calculates by additionally weighting the locations by their activity duration.
- Jump length. Distance of moving between consecutive locations. 
- Wait time. Time of waiting between consecutive locations. 

Dataset distribution plots will be shown after metric calculation. 

### Mobility motifs
Run 
```
python example/run_motifs.py
```
for examples of calculating mobility motifs. Motifs calculation receives the following parameter:
- `proportion_filter` default 0.005. Filter to control how frequent a pattern coulf be considered a motifs, e.g., 0.005 means patterns occuring more than 0.5% of all the patterns are considered motifs.
- `time_format` of [`absolute`, `relative`], default `relative`. Specify whether the input dataset is in absolute time format (e.g., started_at, finished_at) or in relative time format (e.g., started_at, duration) (obtained from mobility simulation). 

Dataset distribution plot and motifs distribution plots will be shown after mobility motifs calculation.

## Known issues:

## TODO:

