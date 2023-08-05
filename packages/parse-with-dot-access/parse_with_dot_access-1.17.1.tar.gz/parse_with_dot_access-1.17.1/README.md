# a fork of parse with dot access

A mirror fork of [parse](https://github.com/r1chardj0n3s/parse) with dot notation access. 

## Get Started

```bash
pip install parse_with_dot_access
```

```python
from parse import parse

result = parse("{lat}, {long}", "12.21254, 105.15564")
print(result) # <Result () {'lat': '12.21254', 'long': '105.15564'}>
print(result["lat"]) # 12.21254 
print(result.long) # 105.15564
```

# For comprehensive documentation please refer to [the readme of upstream repo](https://github.com/r1chardj0n3s/parse).

