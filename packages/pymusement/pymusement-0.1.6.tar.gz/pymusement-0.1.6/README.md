# PyMusement
A python package and CLI to get wait times for rides at various theme parks
test
## Example
### CLI
Get wait times right from your terminal
```
pymusement islands-adventure --type rides
```

### Library
```
from pymusement.parks.universal.IslandsOfAdventure import IslandsOfAdventure

ioa = IslandsOfAdventure()
print ioa.rides()
# or print ioa.shows() if you want show times instead
```
A full list of the rides and shows in the park will be displayed!

## Getting Started
```
pip install pymusement
```

Based on amusement by rambleraptor


## Parks

| Park Name                     | Rides       | Shows       |
| ------------------------------|-------------|-------------|
| Magic Kingdom                 |             |             |
| Epcot                         |             |             |
| Hollywood Studios             |             |             |
| Animal Kingdom                |             |             |
| Disneyland                    |             |             |
| Disney's California Adventure |             |             |
| Universal Studios Florida     |x            |x            |
| Islands of Adventure          |x            |x            |
| Universal Studios Hollywood   |x            |x            |
| Universal Studios Japan       |             |
| Hersheypark                   |x            |             |

## Work to be done
* Fix API for Disney Parks,
* Find alternative for Seaworld parks
* Add Six Flags parks
