from senticnet.senticnet import SenticNet
##NOTE TO SELF YOU STILL HAVE TO FIX THE EXCEPTION HERE

class SenticValuer:
    def getSentics(self, word):
        senticsAndItensity = []
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

            senticsAndItensity.append(float(sentics['pleasantness']))
            senticsAndItensity.append(float(sentics['attention']))
            senticsAndItensity.append(float(sentics['sensitivity']))
            senticsAndItensity.append(float(sentics['aptitude']))
            senticsAndItensity.append(float(polarity_intensity))

            return senticsAndItensity

        except Exception as e:
            defaultsentics = [0.0, 0.0, 0.0, 0.0, 0.0]
            return defaultsentics



# ##TESTING AREA
# yas = SenticValuer()
# print(yas.getSentics("believe"))