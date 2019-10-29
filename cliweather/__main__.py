import sys
from argparse import ArgumentParser

from cliweather.core import SetUnitAction, Unit, ForecastType, parser_loader

parsers = parser_loader.load_parsers('./cliweather/parsers')

argparser = ArgumentParser(prog='cliweather',
                           description='Command line weather')

required = argparser.add_argument_group('required arguments')
required.add_argument('-p', '--parser',
                      choices=parsers.keys(),
                      required=True,
                      dest='parser',
                      help=('Specify which parser will be used to scrape '
                            'weather information.'))

unit_values = [name.title() for name, value in Unit.__members__.items()]

argparser.add_argument('-u', '--unit',
                       choices=unit_values,
                       required=False,
                       action=SetUnitAction,
                       dest='unit',
                       help=('Specify the unit that will be used to display '
                             'the temperature'))

argparser.add_argument('-a', '--areacode',
                       required=True,
                       dest='area_code',
                       help=('The code area to get the weather broadcast '
                             'from'))

argparser.add_argument('-v', '--version',
                       action='version',
                       version='%(prog)s 1.0')

argparser.add_argument('-td', '--today',
                       dest='forecast_option',
                       action='store_const',
                       const=ForecastType.TODAY,
                       help='Show the weather forecast for the current day')

args = argparser.parse_args()

if not args.forecast_option:
    print((f'{argparser.prog}: error: One of these arguments must be used: '
           '-td/--today, -5d/--fivedays, -10d/--tendays, -w/--weekend'),
          file=sys.stderr)
    sys.exit()

parser = parsers[args.parser]()

results = parser.run(args)

for result in results:
    print(results)
