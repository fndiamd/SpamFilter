import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import email
import email.policy
import re
import pickle

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

email = ["My Dear Good Friend. May i use this medium to open a mutual communication with you seeking your acceptance towards  investing in your country under your management as my partner, My name is Aisha  Gaddafi and  presently living in Oman, i am a Widow and single Mother with three Children, the only biological  Daughter of late Libyan President (Late Colonel Muammar Gaddafi) and presently i am under political  asylum protection by the Omani Government. Please Reply me in my box. (aishagaddafi7710@gmail.com). I have funds worth Twenty Seven Million Five Hundred Thousand United State Dollars,$27.500.000.00 US Dollars which i want to entrust to you for investment projects in your country. If you are willing to handle this project on my behalf, kindly reply urgent to enable me provide you more  details to start the transfer process, I shall appreciate your urgent response through my email address. Below : (aishagaddafi7710@gmail.com). Best Regards. Mrs Aisha."]
email[0] = input_preprocessing(email[0])
email

email = vect.transform(email)
prediction = model.predict(email)
prediction

if prediction == 0:
    print("Email is not spam.")
else:
    print("Email is spam.")