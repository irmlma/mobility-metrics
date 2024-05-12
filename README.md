# Individual mobility metrics

[![arXiv](https://img.shields.io/badge/arXiv-2311.11749-b31b1b.svg)](https://arxiv.org/abs/2311.11749)

## Requirements, dependencies, and installation

This code has been tested on

- Python 3.10, trackintel 1.2.2, geopandas 0.14.0

To create a virtual environment and install the required dependencies, please run the following:
```shell
git clone https://github.com/irmlma/mobility-metrics.git
cd mobility-metrics
conda env create -f environment.yml
conda activate metrics
```
in your working folder. You can then install the package in edit mode using:
```
pip install -e .
```

## Evaluate mobility behavior using mobility metrics

Dataset distribution plots will be shown after metric calculation, and stored in the `.\data\input` folder (will be created if not existing). Input data of location visit sequences should be stored in the `.\data\input` folder. We implement basic mobility metrics as follows: 

### Basic metrics
Run 
```
python mobmetric/scripts/run_metrics.py
```
for examples of calculating basic mobility metrics. The metric can be specified with the input arguement `metric`, accepting one of the arguements [`rg`, `locf`, `jump`,`wait`]: 
- Location visitation frquency. 
- Radius of gyration. Radius of gyration calculation receives the following parameter:
    - `method` of [`duration`, `count`]. `count` calculates with visitation frequency of locations, and `duration` calculates by additionally weighting the locations by their activity duration.
- Jump length. Distance of moving between consecutive locations. 
- Wait time. Time of waiting between consecutive locations. 

### Entropy
- Random Entropy
- Uncorrelated Entropy
- Real Entropy
Run 
```
python mobmetric/scripts/run_entropy.py
```
for examples of calculating entropy for location traces. 


### Mobility motifs
Run 
```
python mobmetric/scripts/run_motifs.py
```
for examples of calculating mobility motifs. Motifs calculation receives the following parameter:
- `proportion_filter` default 0.005. Filter to control how frequent a pattern could be considered a motifs, e.g., 0.005 means patterns occuring more than 0.5% of all the patterns are considered motifs.
- `time_format` of [`absolute`, `relative`], default `relative`. Specify whether the input dataset is in absolute time format (e.g., time available as columns `started_at` and `finished_at`) or in relative time format (e.g., time available as columns `started_at` and `duration`) (obtained directly from mobility simulation). 

## TODO:
None

## Citation
If you find this code useful for your work or use it in your project, please consider citing:

```shell
@misc{hong_revealing_2023,
    title={Revealing behavioral impact on mobility prediction networks through causal interventions},
    author={Hong, Ye and Xin, Yanan and Dirmeier, Simon and Perez-Cruz, Fernando and Raubal, Martin},
    publisher={arXiv},
    year={2023},
    url = {https://arxiv.org/abs/2311.11749},
    doi = {10.48550/arXiv.2311.11749},
}
```

## Contact
If you have any questions, open an issue or let me know: 
- Ye Hong {hongy@ethz.ch}
