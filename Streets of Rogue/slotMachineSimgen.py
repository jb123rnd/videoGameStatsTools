import random
import matplotlib.pyplot as plt

DEBUG = False

def playSlot(payed, money, hackedOdds=False, clover=False):
    rolls = 0
    maxRolls = random.choice(range(7,12))
    baseOdds = 48
    if hackedOdds:
        baseOdds += 15
    if clover:
        baseOdds += 10
    while(rolls < maxRolls and money > 0):
        rolls += 1
        money -= payed
        roll = random.choice(range(100))
        if DEBUG:
            print ("Rolled", roll)
        if roll < baseOdds:     # Let 0-odd non inclusive be wins
            money = money + payed*2
            if DEBUG:
                print ("We Won!, money is {}, # of rolls is {}".format(money, rolls))
        else:
            if DEBUG:
                print ("We Lost!, money is {}, # of rolls is {}".format(money, rolls))
        yield money, rolls
    # yield money   # unnecessary?


def quantitySim(sampleSize=1000, initialMoney=250, hackedOdds=False, clover=False):
    outcomes = []
    sampleSize = sampleSize
    initialMoney = initialMoney

    # print("Simulating {} scenarios!".format(sampleSize))
    for attempt in range(sampleSize):
        rollGen = playSlot(
            payed=50,
            money=initialMoney,
            hackedOdds=hackedOdds,
            clover=clover
        )
        rollValues = [value for value in rollGen]
        if DEBUG:
            print("Roll values is '{}'".format(rollValues))
            print("we have {} money!".format(rollValues[-1][0]))
        outcomes.append(rollValues[-1])
        
        print("\rRolls finished = {}%\r".format(int(attempt/sampleSize*100)), end="")
    # print("")

    sumOfWins = 0
    winnings = []

    for result in outcomes:
        if result[0] < initialMoney:
            # Loss
            pass
        else:
            sumOfWins += 1
        winnings.append(result[0]- initialMoney)
    averageWinnings = sum(winnings)/len(winnings)

    adjustedStrategy = round(sumOfWins / len(outcomes)*100, 3)
    if DEBUG:
        print("Adjusted Strategy Odds = {}%, avg Return = {}\nExpected Earnings on Win={}".format(
            adjustedStrategy,
            int(averageWinnings),
            round(averageWinnings * adjustedStrategy/100, 3)
        ))
    return adjustedStrategy, averageWinnings

tests = [50, 100, 150, 200, 250, 300, 350]
for money in tests:
    sim = quantitySim(sampleSize=100000, initialMoney=money, hackedOdds=True, clover=True)
    print("Initial={}, Break-Even or Better Odds is {}, Avg Earnings is {}".format(money,sim[0], sim[1]))

'''
if DEBUG:
    print("Outcomes is {}".format(outcomes))

outcomeMoney = [element[0] for element in outcomes]
if DEBUG:
    print ("outcomeMoney is {}".format(outcomeMoney))


plt.hist(outcomeMoney, density=False, bins=30)
plt.ylabel('Occurrence')
plt.xlabel('Outcome Money');
# plt.plot(outcomes)
plt.show()
'''