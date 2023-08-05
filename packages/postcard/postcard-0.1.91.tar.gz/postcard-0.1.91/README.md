## Postcard

POP3/SMTP client and more!

Thanks for use.


## How to use
### POP3
#### For decorator
```python
from postcard import Pop3

pop = Pop3()

@pop.process(user="xxx", pwd="xxx")
def get_content():
    content = pop.retrieve()["content"]
    print(content)
```


#### For usual
```python
from postcard import Pop3

pop = Pop3()

pop.login(user="xxx", pwd="xxx")
...
pop.close()
```