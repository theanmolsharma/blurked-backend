import re
import spacy


class Filter:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.ents = []
        pass

    def remove_postal_codes(self, text):
        return re.sub("[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$", "<POSTAL INDEX NUMBER>", text)

    def remove_emails(self, text):
        return re.sub("(([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?))(?![^<]*>)",
                      "<EMAIL>", text)

    def remove_phone_numbers(self, text):
        return re.sub("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", "<PHONE NUMBER>", text)

    def remove_urls(self, text):
        text = re.sub("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", "<URL>",text)
        return re.sub("([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", "<URL>",text)

    def remove_dates(self, text):
        text = re.sub("(\d{4}[- /.]\d{2}[- /.]\d{,2})|(\d{2}[- /.]\d{2}[- /.]\d{,4})", "<DATUM> ", text)
        text = re.sub(
            "(\d{1,2}[^\w]{,2}(january|february|march|april|may|june|july|august|september|october|november|december|January|February|March|April|May|June|July|August|September|October|November|December)([- /.]{,2}(\d{4}|\d{2})){,1})(?P<n>\D)(?![^<]*>)",
            "<DATE> ", text)
        text = re.sub(
            "(\d{1,2}[^\w]{,2}(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)([- /.]{,2}(\d{4}|\d{2})){,1})(?P<n>\D)(?![^<]*>)",
            "<DATE> ", text)
        return text

    def remove_gender(self, text):
        return re.sub("(male|female|Male|Female|MALE|FEMALE)", '<GENDER>', text)

    def process(self, text):
        doc = self.nlp(text)
        self.ents = list(doc.ents)

    def remove_address(self, text):
        for ent in self.ents:
            if ent.label_ == 'GPE':
                text = text.replace(ent.text, '<ADDRESS>')
        return text

    def remove_name(self, text):
        for ent in self.ents:
            if ent.label_ == 'PERSON':
                text = text.replace(ent.text, '<NAME>')
        return text

    def filter(self, text, options):
        self.process(text)
        if options['removeName']:
            text = self.remove_name(text)
        if options['removeAddress']:
            text = self.remove_address(text)
        if options['removePostalCode']:
            text = self.remove_postal_codes(text)
        if options['removeEmail']:
            text = self.remove_emails(text)
        if options['removePhone']:
            text = self.remove_phone_numbers(text)
        if options['removeURL']:
            text = self.remove_urls(text)
        if options['removeDate']:
            text = self.remove_dates(text)
        if options['removeGender']:
            text = self.remove_gender(text)
        return text
