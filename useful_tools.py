import random
from call_counter import CallCounter


@CallCounter.count_calls
def paths_to_steps(steps, hops, cache=None):
    if steps <= 0:
        return [[]]
    if cache is None:
        cache = {}
    key = f'{steps}:{hops}'
    if key in cache:
        return cache[key]
    # result = list()
    # for hop in hops:
    #     if steps - hop >= 0:
    #         for previous in paths_to_steps(steps-hop, hops):
    #             result.append([hop]+previous)
    result = [[hop] + previous
              for hop in hops
              if steps - hop >= 0
              for previous in paths_to_steps(steps-hop, hops, cache)]
    cache[key] = result
    return result


@CallCounter.count_calls
def paths_to_target(target, choices, cache=None):
    if target < 0:
        return None
    if target == 0:
        return {frozenset()}
    if cache is None:
        cache = {}
    key = f'{target}:{choices}'
    if key in cache:
        return cache[key]
    # result = set()
    # for choice in choices:
    #     if target - choice >= 0:
    #         for previous in paths_to_target(target-choice, choices - {choice}):
    #             if previous is not None:
    #                 result.add(frozenset(previous | {choice}))
    result = {frozenset(previous | {choice})
              for choice in choices
              if target-choice >= 0
              for previous in paths_to_target(target-choice, choices - {choice}, cache)
              if previous is not None}
    cache[key] = result
    return result


def find_target_pairs():
    # Generate 2 lists
    length = 5
    list_a = random.sample(range(length * 4), length)
    list_b = random.sample(range(length * 4), length)
    target = random.randint(length, length * 3)
    print(f'from: {list_a} + {list_b} find target = {target}')
    # Prepare lists for calculations
    list_a.sort(reverse=True)
    list_b.sort()
    print(f'sort: {list_a} + {list_b}')
    index_a = 0
    index_b = 0
    closest_pairs = list()
    closest_distance = -1
    while index_a < len(list_a) and index_b < len(list_b):
        # Perform the target calculation
        element_a = list_a[index_a]
        element_b = list_b[index_b]
        element_sum = element_a + element_b
        distance = abs(element_sum - target)
        print(f'Checking @ ({index_a},{index_b}): {element_a} + {element_b} = {element_sum} vs {target}')
        # Determine if we're close to the target
        if closest_distance == -1:
            closest_distance = distance
            closest_pairs.append((element_a, element_b))
        elif distance == closest_distance:
            closest_pairs.append((element_a, element_b))
        elif distance < closest_distance:
            closest_distance = distance
            closest_pairs.clear()
            closest_pairs.append((element_a, element_b))
        # Now determine which indices to try next
        if element_sum >= target:
            index_a += 1
        if element_sum <= target:
            index_b += 1

    # Now print out the pairs
    for pair in closest_pairs:
        element_sum = pair[0] + pair[1]
        distance = element_sum - target
        if distance == 0:
            print(f'{pair[0]} + {pair[1]} = {element_sum} (perfect match)')
        else:
            print(f'{pair[0]} + {pair[1]} = {element_sum} (distance {distance})')


def pound_pound(phrase):
    """
    Standard pound pound master joke
    :param phrase: a phrase that will be processed via pound pound
    :return: the processed phrase
    """
    return "".join((substitution(letter) for letter in phrase))


def substitution(x):
    if x == "#":
        return "Pound "
    else:
        return str(x)


def poem(input_dictionary):
    """
    Writes a poem
    :param input_dictionary: A dictionary of replacements, for 'color', 'plural_noun', and 'celebrity'
    """
    # Use a breakpoint in the code line below to debug your script. # Press ⌘F8 to toggle breakpoints.
    print(f'Roses are {input_dictionary.get("color", "default").upper()}')
    print(f'{input_dictionary["plural_noun"].upper()} are blue')
    print(f'I love {input_dictionary["celebrity"].upper()}')


def get_user_input(condition=True):
    """
    Gets the user's input for a poem
    :param condition: A learning condition
    :return: returns the user's input for poem()
    """
    if condition:
        print(f'Condition is {condition}')
    else:
        raise ValueError("You specified a false condition")
    return_value = {
        "color": input("Enter a color: "),
        "plural_noun": input("Enter a plural noun: "),
        "celebrity": input("Enter a celebrity: ")
    }
    return return_value
