# FLY Graph

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bissim/FLY-graph)](https://github.com/bissim/FLY-graph/releases) [![Travis CI Build Status](https://travis-ci.com/bissim/FLY-graph.svg?branch=master)](https://travis-ci.com/bissim/FLY-graph) [![Release](https://github.com/bissim/FLY-graph/workflows/Release/badge.svg)](https://github.com/bissim/FLY-graph/releases) [![GitHub license](https://img.shields.io/github/license/bissim/FLY-graph?logo=open-source-initiative)](https://github.com/bissim/FLY-graph/blob/master/LICENCE)

[![Maven Central](https://img.shields.io/maven-central/v/io.github.bissim/fly-graph)](https://search.maven.org/search?q=g:io.github.bissim%20AND%20a:fly-graph) [![Java Deploy](https://github.com/bissim/FLY-graph/workflows/Java%20Deploy/badge.svg)](https://github.com/bissim/FLY-graph/packages)

[![PyPI](https://img.shields.io/pypi/v/fly-graph)](https://pypi.org/project/fly-graph/) [![Python Deploy](https://github.com/bissim/FLY-graph/workflows/Python%20Deploy/badge.svg)](https://pypi.org/project/fly-graph/)

Graph library for [**FLY language**](https://github.com/spagnuolocarmine/FLY-language); it enhances FLY capability by introducing *graph* ADT methods to handle graphs.

It is based on common graph libraries like [JGraphT](https://github.com/jgrapht/jgrapht) for Java and [NetworkX](https://github.com/networkx/networkx) for Python. **FLY Graph** defines a common API by picking a minimal subset of the intersection of both library features; such features include:

- basic graph creation and manipulation;
- graph serialization;
- graph tours (breadth-first, depth-first);
- connectivity and strong connectivity;
- directed acyclic graphs and topological order;
- minimum-spanning tree.

## ⚠️ WARNING ⚠️

This library is not intended for stand-alone use in non-FLY project as it is part of FLY language; if you just need a library to handle graphs, just refer to above-mentioned, well-known libraries.
