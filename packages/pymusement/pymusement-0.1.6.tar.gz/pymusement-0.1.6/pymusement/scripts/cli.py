import click
from pymusement import PARKS

@click.command()
@click.argument('name', nargs=1, type=click.Choice(PARKS.keys()))
@click.option('--type', type=click.Choice(['rides', 'shows']), prompt='Please choose rides or shows')
def cli(name, type):
    park = PARKS[name]
    if type == 'rides':
        print_rides(park.rides())
    if type == 'shows':
        print_shows(park.shows())

def print_rides(ride_array):
    longest_name = max(len(key['name']) for key in ride_array)
    one_closed = False in [key['isOpen'] for key in ride_array]
    for ride in ride_array:
        line = ''
        line += ride['name'] + ' ' * (longest_name - len(ride['name']))
        line += ' ' * 3
        if ride['isOpen'] is True:
            line += 'Open'
            # make sure the times are aligned b/c closed longer than open
            if one_closed:
                line += ' ' * 2
        else:
            line += 'Closed'

        line += ' ' * 5
        if ride['wait'] == -9:
            line += 'Virtual Line'
        else:
            line += str(ride['wait']) + ' mins'
        click.echo(line)

def print_shows(show_array):
    longest_name = max(len(key['name']) for key in show_array)
    for show in show_array:
        line = ''
        line += show['name'] + ' ' * (longest_name - len(show['name']))
        line += ' ' * 3
        line += '\n'
        if not show['showtimes']:
            line += 'No Shows \n'
        else:
            if show['endtimes'] is not None and show['endtimes'][0] is not None:
                for time, end in zip(show['showtimes'], show['endtimes']):
                    line += time + ' - ' + end + '\n'
                    
                        
            else:
                for time in show['showtimes']:
                    line += time + '\n'
        click.echo(line)
if __name__ == "__main__":
    cli()

