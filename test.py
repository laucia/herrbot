from en2de import english_to_ipa
from en2de import ipa_to_german
from en2de import cleanup_german



def print_parts(phrase):
    print(phrase)
    ipa = english_to_ipa(phrase)
    # print("0", ipa)
    german1 = ipa_to_german(ipa)
    # print("1", german1)
    german2 = cleanup_german(german1)
    print(german2)
    print("")


print_parts("The sexy quick brown radical fox jumps over the lazy dog")
print_parts("Similar to regular parentheses, but the substring matched by the group is accessible")
print_parts("Mr and Mrs Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. They were the last people you’d expect to be involved in anything strange or mysterious, because they just didn’t hold with such nonsense.")
print_parts("Double, double toil and trouble; Fire burn, and caldron bubble. Fillet of a fenny snake, In the caldron boil and bake; Eye of newt, and toe of frog, Wool of bat, and tongue of dog, Adder's fork, and blind-worm's sting,")
print_parts("I made a garland for her head, And bracelets too, and fragrant zone; She looked at me as she did love, And made sweet moan")
print_parts("Following the Russian Revolution, the Russian Soviet Federative Socialist Republic became the largest and leading constituent of the Soviet Union")
print_parts("Know that I don't like your implementation")