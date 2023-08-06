# log_points
 
## Documentation
### log_point
```
log_point(message=None)
```
Returns the file and line called from and the message if one is given.

<code>log_point()</code> also keeps track of how many times it has been called from each line and if this exceeds a maximum will kill the program.

### pointer
```
pointer(message=None, back_colour=0, font_colour=0)
```
Returns the file and line called from and the message if one is given but coloured with a given background and font colour.
