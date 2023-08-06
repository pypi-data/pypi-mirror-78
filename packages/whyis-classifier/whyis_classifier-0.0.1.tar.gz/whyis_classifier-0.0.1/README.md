# whyis_classifier

## Installation
- install [whyis](http://tetherless-world.github.io/whyis/install) using this command
  ```
  WHYIS_BRANCH=master bash < <(curl -skL https://raw.githubusercontent.com/tetherless-world/whyis/master/install.sh)
  ```
- whyis will be installed in /apps/whyis

- In your knowledge graph directory, add the classifier agent to the list of inferencers in your config.py file:
  * Add the following import line: `import whyis_classifier.classifier_agent as cl`
  * Add the following line to the `inferencers` item in the `Config` dictionary constructor: `"Classifier": cl.Classifier()`

- Write your own classifier, using `whyisclassifier.WhyisClassifier` as its base class
  * You must provide your own identifier (an `rdflib.URIRef`) and write a `label()` method

- Locate your `whyis_classifier` installation, and in the file `user_classifiers.py`, import your classifier and add it to the `user_classifiers` dictionary in the form `'my_classifier_name': my_file.MyClassifier()`
  * To locate your `whyis_classifier` installation, run `python -c "import whyis_classifier as _; print(_.__path__[0])"`

- Reload your knowledge graph to run the inferencer over it
