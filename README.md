# AncestryGraph.AI
Have you ever wondered, "Why am I here and how did I get here?". AncestryGraph.AI is a React/Leaflet app and graph database for visually mapping your ancestors' migration through space and time and attempts to answer what chain of events lead to your existence using node/edge graph theory and generative AI.

<div align="center">
  <img src="static/AncestryAI.gif">
</div>

[![PyPI - Python Version](https://img.shields.io/badge/python-3.10--3.12-blue)](https://www.python.org/downloads/)
![Version](https://img.shields.io/badge/version-0.2-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![pyTest: Passed](https://img.shields.io/badge/pyTests-passed-red)

Ancestry.com and equivelent websites do a great job of answering the who, where, and when for a family tree but somewhat fail on the "how" and "why". AncestryGraph.AI builds a node/edge network graph transcribed on custom maps by Leaflet to walk users through animated migrations and time to show what historical events influenced their ancestors. Google's Gemini generative AI is also leveraged to tell a complete story about our relatives. It comprises birth place, movements, and time periods as the input mixed with Gemini's knowledge of historical events and the diapora of people, painting a well educated guess at how and why our ancestors lived. This finally answers questions like: "Why did my ancestors come to this country?", "What historical events were crucial to bringing my ancestors together?", and "How did my ancestors live and spend their time?".

**License:** Ancestry-Graph-AI is free to use under the [MIT License](LICENSE.txt)

## Table of Contents

- [Requirements](#requirements)
- [ToDo](#todo)
  

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
* Add datetime filter based on start and end dates
