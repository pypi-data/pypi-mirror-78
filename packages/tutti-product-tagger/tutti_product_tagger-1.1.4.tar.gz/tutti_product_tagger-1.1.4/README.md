# PRODUCT TAGGER

This is a Python package that contains the logic behind Team Data's product tagging algorithm.

## Usage

Example of usage:

```python
import pandas as pd
import tutti_product_tagger

ad_title = 'Salon Tisch (Vintage)'
ad_body = 'Wunderschöner antiker Salontisch wegen Wohnungsauflösung abzugeben, CHF 250.00'

# You can assign a tag to a string:
print(tutti_product_tagger.assign_tag_to_string(ad_title))
# Output: {'tag': 'table'}

# Or you can set up a data frame of strings and tag them all at once:
df = pd.DataFrame({'title': [ad_title], 'body': [ad_body]})
tag = df.apply(tutti_product_tagger.assign_tag_to_subject_body, axis=1, subject_col='title', body_col='body')
print(tag[0])
# Output: table
```

## Publishing to PyPI
To publish version x.y.z to PyPI, execute these commands:


`git checkout x.y.z`

`~/product-tagger/venv/bin/python3.7 setup.py sdist bdist_wheel`

`~/product-tagger/twine upload --repository pypi ~/product-tagger/dist/*x.y.z*`

Your `~/.pypirc` should be similar to:

```
[distutils]
index-servers =
    pypi
    pypitest

[pypi]
username: oscartutti
password: xxxxx

[pypitest]
repository: https://test.pypi.org/legacy/
username: oscartutti
password: xxxxx
```
