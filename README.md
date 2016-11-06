# do
Simple command-line todo list app

### Examples
```
# Create task list in current directory
$ do --init

# Add some tasks
$ do -a wake up
$ do -a survive
$ do -a go to sleep

# List all tasks
$ do -l
 1. [ ] wake up
 2. [ ] survive
 3. [ ] go to sleep

# Finish some tisks and list all tasks
$ do -f 1 2 -l
 1. [X] wake up
 2. [X] survive
 3. [ ] go to sleep
 
# Change task
$ do -c 2
text: <enter text>
```
