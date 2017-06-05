from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from emails import app_settings

User = get_user_model()

TYPOS = {  # from digitalcoding.com/tools/typo-generator.html & past experience
    'yahoo': 'tahoo gahoo hahoo uahoo 7ahoo 6ahoo yzhoo yshoo ywhoo yqhoo\
              yagoo yaboo yanoo yajoo yauoo yayoo yahio yahko yahlo yahpo\
              yah0o yah9o yahoi yahok yahol yahop yaho0 yaho9 ahoo yhoo yaoo\
              yaho yaho ayhoo yhaoo yaoho yyahoo yaahoo yahhoo yahooo yahooo',
    'hotmail': 'gotmail botmail notmail jotmail uotmail yotmail hitmail\
                hktmail hltmail hptmail h0tmail h9tmail hormail hofmail\
                hogmail hoymail ho6mail ho5mail hotnail hotkail hotjail\
                hotmzil hotmsil hotmwil hotmqil hotmaul hotmajl hotmakl\
                hotmaol hotma9l hotma8l hotmaik hotmaip hotmaio otmail\
                htmail homail hotail hotmil hotmal hotmai ohtmail htomail\
                homtail hotamil hotmial hotmali hhotmail hootmail hottmail\
                hotmmail hotmaail hotmaiil hotmaill hotmailo',
    'gmail.com': 'gmail.co.uk gmail.es gmail.fr gmail.pl gmail.pt gmail.sk\
                  gmail.cz gmail.lt',
    'gmail': 'vmail bmail hmail tmail gnail gkail gjail gmzil gmsil gmwil\
              gmqil gmaul gmajl gmakl gmaol gma9l gma8l gmaik gmaip gmaio gail\
              gmil gmal gmai mgail gamil gmial gmali ggmail gmmail gmaail\
              gmaiil gmaill',
    'googlemail': 'fooglemail vooglemail booglemail hooglemail yooglemail\
                   tooglemail gioglemail gkoglemail gloglemail gpoglemail\
                   g0oglemail g9oglemail goiglemail gokglemail golglemail\
                   gopglemail go0glemail go9glemail gooflemail goovlemail\
                   gooblemail goohlemail gooylemail gootlemail googkemail\
                   googpemail googoemail googlwmail googlsmail googldmail\
                   googlrmail googl4mail googl3mail googlenail googlekail\
                   googlejail googlemzil googlemsil googlemwil googlemqil\
                   googlemaul googlemajl googlemakl googlemaol googlema9l\
                   googlema8l googlemaik googlemaip googlemaio ooglemail\
                   goglemail goglemail goolemail googemail googlmail googleail\
                   googlemil googlemal googlemai ogoglemail gogolemail\
                   goolgemail googelmail googlmeail googleamil googlemial\
                   googlemali ggooglemail goooglemail goooglemail googglemail\
                   googllemail googleemail googlemmail googlemaail googlemaiil\
                   googlemaill googlemailm',
    'btinternet': 'btinterbet btineternet',
    'btconnect': 'tconnect',
    '.com': '.con .cim .coom .ccom .cpm',
    '.co.uk': '.co.ul .couk .co.yk .co.ik .com.uk .cco.uk .co.um .co.un .co.ui\
               .co.uj'
}


def fix_typos(dry_run=True):
    for correct, wrong in TYPOS.items():
        for typo in wrong.split():
            if correct.startswith('.'):  # TLD typo
                d = {'email__endswith': typo}
                bad = typo
                good = correct
            else:  # domain typo
                end = '.' if '.' not in correct else ''
                bad = '@' + typo + end
                good = '@' + correct + end
                d = {'email__icontains': bad}

            for u in User.objects.filter(**d):
                new = u.email.replace(bad, good)
                print(u.username, u.email, '->', new)
                if not dry_run:
                    app_settings.EMAILS_FIX_TYPOS(u, new)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-w', action='store_true',
                            help='Update broken emails, merge accounts.')

    def handle(self, *args, **options):
        if options.get('w'):
            fix_typos(dry_run=False)
        else:
            print("Dry run, use: 'email_typos -w' if it goes smooth.")
            fix_typos()
