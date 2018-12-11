from senticnet.senticnet import SenticNet

class SenticValuer:
    def getSentics(self, word):
        senticsAndItensity = []
        sn = SenticNet('en')
        try:
            sentics = sn.sentics(word)
            polarity_intensity = sn.polarity_intense(word)

            senticsAndItensity.append(float(sentics['pleasantness']))
            senticsAndItensity.append(float(sentics['attention']))
            senticsAndItensity.append(float(sentics['sensitivity']))
            senticsAndItensity.append(float(sentics['aptitude']))
            senticsAndItensity.append(float(polarity_intensity))

            return senticsAndItensity

        except Exception as e:
            defaultsentics = [0.0, 0.0, 0.0, 0.0, 0.0]
            return defaultsentics