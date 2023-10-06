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
for examples of calculating basic mobility metrics. The metric can be specified with the input arguement `metric`, accepting one of the  arguements ["rg", "locf", "jump","wait"]: 
- Location visitation frquency. 
- Radius of gyration. Radius of gyration can be calculated either a) with visitation frequency of locations or b) weighting the locations by their activity duration.
- Jump length. Distance of moving between consecutive locations. 
- Wait time. Time of waiting between consecutive locations. 

Dataset distribution plots will be shown after metric calculation. 

## Known issues:


## TODO:
- mobility motifs
