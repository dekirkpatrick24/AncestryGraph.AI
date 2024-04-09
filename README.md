# AncestryGraph.AI
Have you ever wondered, "Where did I come from?". AncestryGraph.AI is a React/Leaflet app for visually mapping your ancestors' migration through space and time and attempts to answer what chain of events lead to your existance using node/edge graphs and generative AI.

![Ancestry-Graph-AI Logo](static/AncestryAI.gif) class="AppDemo"

[![PyPI - Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.12-blue)](https://www.python.org/downloads/)
![Version](https://img.shields.io/badge/version-0.1-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![pyTest: Passed](https://img.shields.io/badge/pyTests-passed-red)

Ancestry.com and equivelent websites do a great job of answering the who, where, and when for a family tree but somewhat fail on the "how" and "why". AncestryGraph.AI builds a node/edge network graph transcribed on custom maps by Leaflet to walk users through animated migrations and time to show what historical events influenced their ancestors. This finally answers questions like: "How did my ancestors live and spend their time?", "Why did my ancestors come to America?", "What hobbies and occupations did my ancestors have?", and "What historical events were crucial to bringing my ancestors together?".

**License:** Ancestry-Graph-AI is free to use under the [MIT License](LICENSE.txt).

**References**: Please cite the appropriate papers if Chemprop is helpful to your research.

## Table of Contents

- [Documentation](#documentation)
- [Requirements](#requirements)
- [ToDo](#todo)

## Documentation

* 

## Requirements

* Ancestry.com or equivelent .ged file export of your family tree
* Python 3.10 or 3.12 (not tested with < 3.10)
* Leaflet 1.9.4
* Typeahead.js 0.11.1
* MySQL 8/MariaDB 11.4 or Postgres 16.2
* Neo4j 4.4 (Optional if nodes < 1 million and edges < 2 million, use MySQL/MariaDB otherwise)
* Google Gemini Account (Optional)

## Todo

* Neo4j ingestion functions


 .AppDemo {
    width: 100%;
    margin: 10px auto;  /* Add margins for better spacing */
}
