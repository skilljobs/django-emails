"""
IMAP client that can receive instant pushes from Gmail or compatible IMAP account.
Idler keeps constatntly listening for newly received mail.

Requires settings: EMAIL_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD
and RECIPES, a dictionary of processing recipes.
"""
try:
    from emails import imap_recipes as recipe
except ImportError:
    print('No recipes are available.')
from email import message_from_string as parse
from imaplib2 import IMAP4_SSL
from threading import Thread, Event
import settings, time

RECIPES = {
    'Bounces': recipe.note_bounce,
    'Uploads': recipe.email_upload,
    'Unsubscribe': recipe.unsubscribe
}
FOLDER_LABEL = 'Process'
 # BT & test emails do not use SPF
SKIP_SPF = ['btinternet', 'test@'+settings.EMAIL_DOMAIN]

class Idler(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
        
    def work(self):
        try:
            for name, rec in RECIPES.items():
                self.process(name, rec)
        except IMAP4_SSL.abort: pass
    
    def start(self):
        self.thread.start()
    
    def stop(self):
        self.event.set()
    
    def join(self):
        self.thread.join()
    
    def idle(self):
        while True:
            if self.event.isSet():
                return
            self.needsync = False
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            self.M.idle(callback=callback)
            self.event.wait()
            if self.needsync:
                self.event.clear()
                self.work()
    
    def process(self, label, recipe):
        self.M.select(FOLDER_LABEL+'/' + label)
        status, data = self.M.uid('search', None, 'UnSeen')
        if data[0]:
            for num in data[0].split():
                status, data = self.M.uid('fetch', num, '(RFC822)')
                msg = parse(data[0][1])
                skip_spf = any([True for s in SKIP_SPF if s in msg['From']])
                if 'pass' in msg.get('Received-SPF', '') or skip_spf:
                    print(recipe(msg))
                else:
                    print("Didn't pass sender checks: %s" % msg.get('From', 'No sender'))
                self.M.uid('store', num, '+FLAGS', 'Seen')
        self.M.expunge()


def login():
    m = IMAP4_SSL(settings.EMAIL_SERVER)
    m.login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD)
    m.select(FOLDER_LABEL)
    return m

def logout(worker, m):
    worker.stop()
    worker.join()
    m.close()
    m.logout()

def receive(seconds):
    M = login()
    worker = Idler(M)
    try:
        worker.start()
        worker.work()
        time.sleep(seconds)
    finally:
        logout(worker, M)
