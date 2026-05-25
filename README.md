# Physics-Informed Intelligent System for Natural Gas Metering Quality Control

## Overview

This software package implements a comprehensive physics-informed benchmark environment for intelligent quality assessment of natural gas metering systems using machine learning methods and physically constrained anomaly detection.

The developed framework combines:
- real metering data obtained from natural gas accounting nodes;
- physical balance equations of gas distribution systems;
- reconstruction of high-resolution temporal signals;
- synthetic generation of physically plausible anomalies;
- machine learning methods for anomaly detection;
- comparative benchmarking of intelligent algorithms.

The software is intended for:
- scientific research;
- intelligent metering systems;
- cyber-physical energy systems;
- smart gas infrastructure;
- sensor diagnostics;
- metrological verification;
- anomaly detection in gas transportation systems.

---

# Main Objectives of the System

The primary objective of the developed software complex is the creation of an experimental and analytical environment for evaluating the reliability and quality of natural gas metering under both normal and abnormal operating conditions.

The system solves several key scientific and engineering problems simultaneously:

- reconstruction of missing or sparse telemetry data;
- modeling of physical degradation processes;
- simulation of metrological failures;
- generation of benchmark datasets;
- validation of anomaly detection algorithms;
- evaluation of intelligent monitoring methods;
- testing of physics-informed machine learning approaches.

The software allows researchers to investigate how intelligent algorithms behave in conditions close to real industrial gas distribution systems.

---

# Scientific Motivation

Open datasets for commercial natural gas metering are extremely limited because such information is usually:
- commercially sensitive;
- related to critical infrastructure;
- restricted for cybersecurity reasons.

Therefore, fully open industrial datasets suitable for anomaly detection research are almost unavailable.

To overcome this limitation, the proposed software introduces a hybrid physics-informed benchmark methodology based on:
1. real industrial measurements;
2. physical gas flow constraints;
3. controlled anomaly injection.

This approach significantly improves the realism of benchmarking compared to purely synthetic datasets.

---

# Functional Architecture

The software package implements a complete data processing pipeline.

## 1. Loading Real Metering Data

The system loads real telemetry data obtained from gas flow meters and gas accounting nodes.

Typical signals include:
- gas flow rate;
- pressure;
- temperature;
- accumulated volume;
- corrected standard volume.

Input data format:
```csv
time,black,gray
15,2084,2095
17.5,2086,2097
...
2. Signal Reconstruction

Real industrial measurements are typically collected every 15 seconds.

For machine learning analysis this temporal resolution is often insufficient.

Therefore, the software reconstructs a one-second temporal signal using:

cubic spline interpolation;
PID-inspired dynamic reconstruction;
physically constrained smoothing.

The reconstruction algorithm preserves:

signal continuity;
physical smoothness;
realistic flow dynamics;
bounded rate of change.

This stage transforms sparse industrial telemetry into a high-resolution temporal dataset.

Physics-Informed Reconstruction

The reconstruction process combines:

interpolation theory;
control theory;
physical constraints of gas transportation.

Unlike ordinary interpolation, the implemented approach introduces:

derivative stabilization;
physically bounded dynamics;
inertia-aware reconstruction.

The algorithm prevents unrealistic discontinuities and high-frequency oscillations that cannot exist in real gas distribution systems.

Anomaly Injection Framework

The system generates physically plausible anomalies using controlled modification of real telemetry signals.

Implemented anomaly classes include:

Sensor Drift Injection

Gradual deviation of sensor calibration caused by:

aging;
thermal degradation;
ADC instability;
metrological drift.

This anomaly evolves slowly over time.

Leakage Injection

Simulation of gas leakage scenarios:

local pipeline leakage;
seal degradation;
pressure loss;
unauthorized extraction.

The anomaly affects:

flow balance;
pressure dynamics;
accumulated volume consistency.
Noise Burst Injection

Simulation of:

electromagnetic interference;
sensor instability;
transient communication disturbances;
ADC noise bursts.
Desynchronization Injection

Simulation of temporal misalignment between:

distributed sensors;
SCADA subsystems;
telemetry nodes.

This anomaly is especially important for distributed cyber-physical gas infrastructure.

Machine Learning Algorithms

The framework supports benchmarking of multiple anomaly detection methods.

Implemented Models
Isolation Forest

Tree-based anomaly isolation algorithm.

DBSCAN

Density-based clustering approach for outlier detection.

Autoencoder

Neural-network reconstruction-based anomaly detector.

Kalman-like Filter

Statistical filtering method for dynamic deviation estimation.

Double Control Method

Proposed physics-informed hybrid method combining:

statistical anomaly detection;
physical balance verification.
Double Control Method

The proposed Double Control approach introduces two complementary levels of verification:

Statistical Control

Analysis of temporal signal behavior using machine learning.

Physical Control

Verification of:

balance consistency;
flow dynamics;
physical plausibility.

This allows the system to detect anomalies that may remain invisible to purely statistical ML approaches.

Evaluation Metrics

The framework automatically computes:

ROC-AUC;
Precision;
Recall;
F1-score.

These metrics allow quantitative comparison between:

classical ML methods;
statistical filters;
physics-informed approaches.
Visualization System

The software automatically generates:

ROC curves;
reconstructed signal plots;
anomaly injection visualizations;
comparative graphs.

All graphical results are exported in high-quality PNG format suitable for:

scientific publications;
IEEE papers;
conference presentations;
Scopus-indexed journals.
Output Structure

After execution the system automatically creates:

data/
├── plots/
│   ├── roc_curves.png
│   ├── anomaly_signal.png
│
├── results/
│   ├── model_comparison.csv
│   ├── benchmark_dataset.csv
Benchmark Dataset

The generated benchmark dataset contains:

reconstructed normal signals;
anomalous signals;
labels;
model predictions;
anomaly scores.

The dataset can be directly used for:

ML training;
benchmarking;
reproducible research;
comparative studies.
Advantages of the Proposed Framework

Compared to traditional synthetic datasets, the proposed approach provides:

higher physical realism;
industrial plausibility;
controlled anomaly generation;
reproducibility;
explainability;
compatibility with real telemetry.

The framework combines advantages of:

real industrial data;
physical modeling;
intelligent analytics.
Potential Applications

The developed software can be applied in:

intelligent gas metering systems;
smart energy infrastructure;
SCADA diagnostics;
metrological verification;
cyber-physical security;
industrial anomaly detection;
predictive maintenance;
digital twins of gas distribution systems.
Scientific Contribution

The proposed framework introduces:

a hybrid physics-informed benchmark methodology;
physically constrained anomaly injection;
reconstruction-aware telemetry analysis;
intelligent metering quality assessment;
combined statistical and physical anomaly verification.

The approach can serve as a foundation for future research in:

intelligent energy systems;
physics-informed machine learning;
industrial AI;
anomaly detection in critical infrastructure.
Repository Structure
project/
│
├── main.py
├── rec_date.csv
├── requirements.txt
│
├── data/
│   ├── plots/
│   └── results/
│
└── README.md
Requirements

Recommended environment:

Python 3.11+
NumPy
Pandas
Matplotlib
Scikit-learn
SciPy

Install dependencies:

pip install numpy pandas matplotlib scipy scikit-learn
Run

Execute:

python main.py
Future Development

Planned extensions include:

LSTM and Transformer models;
graph neural networks;
digital twin integration;
real SCADA connectivity;
online anomaly detection;
adaptive thresholding;
multi-agent distributed analysis;
retrieval-augmented diagnostics.
Author Notes

The framework was developed for scientific research in:

intelligent metering;
gas distribution systems;
industrial anomaly detection;
cyber-physical systems;
AI-assisted metrology.

The project focuses on explainable and physics-informed machine learning approaches for critical infrastructure monitoring.