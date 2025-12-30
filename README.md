**DANCE** (Drosophila Aggression and Courtship Evaluator) provides an accessible, affordable, and robust solution for quantifying aggression and courtship behaviors in Drosophila. The DANCE hardware is orders of magnitude cheaper while achieving comparable performance to existing traditional setups. 

![DANCE_Github_30012025](https://github.com/user-attachments/assets/3efdfbbb-8cc2-4898-a668-61a973c37b8d)

**Figure:** (A) DANCE hardware and recordings setup for acquisition of aggression and courtship behaviors. (B-C) Top and side views of the DANCE setup with a smartphone camera for recording and electronic tablet used as a backlight. (D-E) DANCE aggression and courtship arenas to record behaviors.

## Key Features:
- **Ultra-low-cost (<$0.30), portable hardware** for automated behavioral analysis using everyday, repurposed materials.
- **Automated analysis** using machine-learning–based classifiers to quantify aggression and courtship behaviors.
- **Open-source pipeline** designed to be user-friendly and accessible to conduct sophisticated behavioral analysis.

## What DANCE measures
- Six machine–learning–based classifiers developed using JAABA
- Quantifies aggressive lunges and five courtship behaviors:
  - wing extension
  - circling
  - following
  - attempted copulation
  - copulation

## Hardware overview
- Fabricated from off-the-shelf, repurposed materials (medicine blister packs, acrylic sheets, paper tape)
- Recordings performed using smartphones or tablets
- Smartphone or tablet used as a backlight source

## Getting started
- **Hardware & recording setup:** See the DANCE preprint for detailed hardware components and recording requirements.
- **Behavioral classifiers:** JAABA-based classifier files (`.jab`) can be downloaded here:  
  https://drive.google.com/drive/folders/1N75OinwMuYrkIT3qclAJThCvfOZMuotj
- **Required software:**
  - FlyTracker: https://github.com/kristinbranson/FlyTracker
  - JAABA: https://github.com/kristinbranson/JAABA
- **Step-by-step analysis instructions:**  
  See [`DANCE_Analysis_step-by-step_instructions.md`](DANCE_Analysis_step-by-step_instructions.md)

## Citing DANCE
This repository contains the analysis codes used in the following publication:

R Sai Prathap Yadav, Paulami Dey, Faizah Ansar, Tanvi Kottat, Manohar Vasam, P Pallavi Prabhu, Shrinivas Ayyangar, Swathi Bhaskar S, Krishnananda Prabhu, Monalisa Ghosh, Pavan Agrawal*
(2025)
**DANCE provides an open-source and low-cost approach to quantify aggression and courtship in Drosophila**.  
*eLife*.  
DOI:  https://doi.org/10.7554/eLife.105465.3

The version of this repository used for the paper has been archived at Software Heritage as part of the eLife publication process.

## Patent information
The hardware is described in a patent application with the Indian Patent Office, titled: ‘Device for Measuring Complex Social Behaviors In Small Insects’. 
Application number: 202441072884. Inventors: Dr. Pavan Kumar Agrawal, Faizah Ansari, Rachagolla Saiprathap Yadav.




