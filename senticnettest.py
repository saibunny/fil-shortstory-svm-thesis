from senticnet.senticnet import SenticNet
##NOTE TO SELF YOU STILL HAVE TO FIX THE EXCEPTION HERE

class SenticValuer:
    def getSentics(self, word):
        senticsAndItensity = ""
        sn = SenticNet('en')
        try:
            sentics = sn.sentics(word)
            polarity_intensity = sn.polarity_intense(word)
            # print(sentics)
            # print(sentics['pleasantness'])
            # print(sentics['attention'])
            # print(sentics['sensitivity'])
            # print(sentics['aptitude'])
            # print(polarity_intensity)

            senticsAndItensity = senticsAndItensity + sentics['pleasantness'] + ', ' \
                                 + sentics['attention'] + ', ' \
                                 + sentics['sensitivity'] + ', ' \
                                 + sentics['aptitude'] + ', '\
                                 + polarity_intensity

            return senticsAndItensity

        except Exception as e:
            print(word + " does not exist")



# ##TESTING AREA
# yas = SenticValuer()
# print(yas.getSentics("believe"))
