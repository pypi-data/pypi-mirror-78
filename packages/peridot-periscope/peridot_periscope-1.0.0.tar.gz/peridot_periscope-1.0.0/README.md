# Periscope (1.1)

![Periscope Logo](https://raw.githubusercontent.com/toto-bird/Periscope/master/logo.png)

### Usage:
Peri.dot
```
var periscope = include('periscope')

var pscope_add() -> Null {
    return(periscope.skip(
        'Out of date'
    ))
}

var pscope_sub() -> Null {
    assert(10 - 5 == 5)

    return(Null)
}

var pscope_mul() -> Null {
    assert(10 - 1 == 10, 'Hmm. Somethings not right')

    return(Null)
}
```

Bash
```bash
# Test files
periscope peritests/*

# More help
periscope -h
```
