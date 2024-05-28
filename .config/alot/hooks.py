from pathlib import Path
import alot.buffers
from datetime import datetime
import re
import alot
import tempfile
import webbrowser
from alot.helper import string_sanitize
from alot.helper import string_decode
import os


new_mail_file = Path.home() / '.config' / 'alot' / 'new_mail'


def check_mail(new_mail_file):
    with open(new_mail_file, 'r') as fh:
        new_mail = fh.read()[0] == '1' 
    if new_mail:
        with open(new_mail_file, 'w') as fh:
            fh.write('0')
            fh.write('\n')
    return new_mail


def check_notmuch(ui):
    ui.notify('checking!')
    notmuch_out = os.popen('notmuch new').readlines()
    new_mail = len(notmuch_out) > 1
    if new_mail:
        for buf in ui.get_buffers_of_type(alot.buffers.SearchBuffer):
            buf.rebuild()


def loop_hook(**kwargs):
    new_mail = check_mail(new_mail_file)
    ui = kwargs['ui']
    if new_mail:
        ui.notify(datetime.now().strftime('New update from notmuch.'))
        for buf in ui.get_buffers_of_type(alot.buffers.SearchBuffer):
            buf.rebuild() 


# def pre_buffer_focus(ui, dbm, buf):
#     if buf.modename == 'search':
#         buf.rebuild()


# Helper method to extract the raw html part of a message. Note that it
# only extracts the first text/html part found.
def _get_raw_html(msg):
    mail = msg.get_email()

    for part in mail.walk():
        ctype = part.get_content_type()

        if ctype != "text/html":
            continue

        cd = part.get('Content-Disposition', '')

        if cd.startswith('attachment'):
            continue

        enc = part.get_content_charset() or 'utf-8'

        raw = string_decode(part.get_payload(decode=True), enc)

        return string_sanitize(raw)

    return None


# Opens HTML emails in an external browser.
# Related issue:
#  - https://github.com/pazz/alot/issues/1153
def open_in_browser(ui=None):
    ui.notify("Opening message in browser...")
    msg = ui.current_buffer.get_selected_message()

    htmlstr = _get_raw_html(msg)

    if htmlstr is None:
        ui.notify("Email has no html part")
        return

    temp = tempfile.NamedTemporaryFile(prefix="alot-",suffix=".html",
                                       delete=False)
    temp.write(htmlstr.encode("utf-8"))
    temp.flush()
    temp.close()
    webbrowser.open(temp.name)


async def pre_envelope_send(ui, dbm, cmd):
    e = ui.current_buffer.envelope
    if re.match('.*[Aa]ttach', e.body_txt, re.DOTALL) and\
       not e.attachments:
        msg = 'no attachments. send anyway?'
        if not (await ui.choice(msg, select='yes')) == 'yes':
            raise Exception('operation cancelled')


def reply_prefix(*args, **kwargs):
    # On Tue, 9 Apr 2019 at 18:17 John Doe, <john.doe@example.com> wrote:
    return "On {2:%a, %-d %b %Y at %I:%M %p %Z} {0}, <{1}> wrote:\n\n".format(*args)


def forward_prefix(*args, **kwargs):
    # ---------- Forwarded message ---------
    # From: John Doe <john.doe@example.com>
    # Date: Wed, 10 Apr 2019 at 00:23
    # Subject: Re: Cool mail
    # To: Jane Doe <jane.doe@example.com>
    # requires patched alot (https://github.com/pazz/alot/pull/1390)
    subject = alot.db.utils.decode_header(kwargs["message"].get("Subject", ""))
    to = alot.db.utils.decode_header(kwargs["message"].get("To", ""))
    return (" ---------- Forwarded message ---------\n"
               " From: {0} <{1}>\n"
               " Date: {2:%a, %-d %b %Y at %I:%M %p %Z}\n"
               " Subject: {3}\n"
               " To: {4}\n\n\n"
            ).format(*args, subject, to)
