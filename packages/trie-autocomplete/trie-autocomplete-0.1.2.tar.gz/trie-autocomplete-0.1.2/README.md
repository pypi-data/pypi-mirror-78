# Trie

## Usage

```python
from trie import Trie

trie = Trie()

for key, value in dictionary.items():  # some data
    trie[key] = value

for key in trie.autocomplete(key_with_typo):  # results a generator of keys
    print(key, trie[key])
```
