# d
Just another CLI task management tool

### Examples
```
# Create task list in current directory
$ d --init

# Add some tasks
$ d -a wake up

# Add several tasks at once
$ d -a survive -a go to sleep

# List all tasks
$ d -l
 1. [ ] wake up
 2. [ ] survive
 3. [ ] go to sleep

# Finish several tisks and list all
$ d -f 1 2 -l
 1. [X] wake up
 2. [X] survive
 3. [ ] go to sleep
 
# Change task
$ d -c 2
text: <enter text>
```
