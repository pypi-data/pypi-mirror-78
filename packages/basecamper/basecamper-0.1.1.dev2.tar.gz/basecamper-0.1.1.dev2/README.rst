===================
Granular Basecamper
===================


Utility package for satellite machine learning training


* Free software: MIT license
* Documentation: docs.granular.ai/basecamper.


Features
--------

* Polyaxon auto-param capture
* Configuration enforcement and management for translation into Dione environment
* Precomposed loss functions and metrics


TODO
----

* Shift build logic from cloudbuild to github actions


Build Details
-------------

* packages are managed using poetry
* packages poetry maintains pyproject.toml
* PRs and commits to `develop` branch trigger a google cloudbuild (image: cloudbuild.yaml, docs: cloudbuild_docs.yaml)
* Dockerfile builds image by exporting poetry dependencies as tmp_requirements.txt and installing them
