# DataButler
##### A python-based software for automatic data profiling and cataloging

It takes a lot of man-hours and energy to transform data dumps into forms that are more understandable and suitable for databases. The objective of DataButler is to model a framework that performs data profiling and cataloging, thereby providing more efficient search/discover functionalities.

### Process Flow
![Methodology](https://github.com/DataButler/Data-Butler/blob/master/Processflow.png)

### Installation

```sh
pip install data_butler

#In case of missing English spacy model (en_core_web_sm)
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz

```
### Directions
```sh
import data_butler

data_butler.db('file directory/filename.csv')
```
### Authors
Keerthi Pullela, Rahul Madhu, Rukmini Sunil, Sagar Kurada, Xema Pathak

### Acknowledgments
Professor Matthew Lanham, 
Krannert School of Management,
Purdue University\
Mike Lutz, Caleb Keller, 
Samtec Inc. 
