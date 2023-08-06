# RefLabel

RefLabel is written as an extension to Kivy's Label widget, with a focus on the
[ref=] markup capability. 

RefLabel automatically prepends items in its item list with [ref=] markers, and
arranges them in a grid pattern before placing them in the text field of the 
label widget. RefLabel also inlcudes options and methods to accomodate this
goal, which are explained in the source file. 

Any item in the list that is already referenced will be left as is, where an
item with [ref=None] will have its reference removed. Assignment of automatic 
references may be halted by setting the references variable to False. 

Any instance method defined as ref\_\<name\> will be executed if the matching
referenced name in the label is selected.


### Requires:

- python3
- kivy


## Examples

```
from ftref import RefLabel

test = RefLabel(set_label=False)

test.cols = 3
test.rows = 3

test.items = ["One", "Two", "Three",
"Four", "Five", "Six",
"Seven", "Eight", "Nine"]

test.init()

print(test)
One Two Three
Four Five Six
Seven Eight Nine

print(test.text)
[ref=('One', 0)]One[/ref] [ref=('Two', 1)]Two[/ref] [ref=('Three', 2)]Three[/ref]
[ref=('Four', 3)]Four[/ref] [ref=('Five', 4)]Five[/ref] [ref=('Six', 5)]Six[/ref]
[ref=('Seven', 6)]Seven[/ref] [ref=('Eight', 7)]Eight[/ref] [ref=('Nine', 8)]Nine[/ref]
```

Change orientation:

```
test.orientation = 'lr-bt'
test.init()
print(test)
Seven Eight Nine
Four Five Six
One Two Three
```

refMethod decides between name or indicie upon selection:

```
test.refMethod = 'indicie'
test.selector(None, name=4, scope='items')
test.selected
[4]

test.clearselection()

test.refMethod = 'name'
test.selector(None, name=4, scope='items')
test.selected
['Five']
```

Selecting an item twice deselects it. Multiple selections can be made:

```
test.multi = True
test.selector(None, name=[4,5,6], scope='items')
test.selected
['Six', 'Seven']
```
