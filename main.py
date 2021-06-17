import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import email
import email.policy
from email.parser import Parser
from email.utils import parseaddr, formataddr
import re
import pickle
import sys
import subprocess

nltk.download('punkt')
nltk.download('stopwords')


def input_preprocessing(email):
    email = re.sub(r"[^a-zA-Z0-9]+", ' ', email)
    stopList = set(stopwords.words('english'))
    emailToken = word_tokenize(email.lower())
    email = [word for word in emailToken if word not in stopList]
    email = ' '.join([str(elem) for elem in email])
    return email

model = pickle.load(open('model/email-spam-detection-model.sav', 'rb'))
vect =  pickle.load(open("model/vectorized.pickel", "rb"))

BRANDING_HEADER = 'X-SPAM-CHECK'

def apply_filter(frm, to, content):
    content = vect.transform(content)
    prediction = model.predict(content)
    if prediction == 1:
        oldSubject = content.get('Subject')
        del content['Subject']
        content['Subject'] = "!!! SPAM !!!" + oldSubject
    return frm, to, content

EX_TEMPFAIL = 75
EX_UNAVAILABLE = 69

def parse_args():
    try:
        cli_from = sys.argv[1].lower()
        cli_to = [x.lower() for x in sys.argv[2:]]
    except IndexError:
        sys.exit(EX_UNAVAILABLE)
    else:
        return cli_from, cli_to

def get_content():
    content = ''.join(sys.stdin.readlines())
    return Parser().parsestr(content)

def re_inject(frm, to, content):
    if BRANDING_HEADER in content:
        return True

    content[BRANDING_HEADER] = 'yes'

    p = subprocess.Popen(
        ['/usr/sbin/sendmail', '-G', '-i', '-f', frm] + to,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    p.communicate(content.as_bytes())
    ret = p.wait()

    if ret == 0:
        return True

    return False

def main():
    frm, to = parse_args()
    content = get_content()

    if not re_inject(*apply_filter(frm, to, content)):
        sys.exit(EX_TEMPFAIL)

if __name__ == '__main__':
    main()