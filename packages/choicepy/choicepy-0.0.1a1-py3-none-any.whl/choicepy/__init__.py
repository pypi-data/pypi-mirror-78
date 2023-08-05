import itertools
import os
import random
import string
from collections import Counter

import numpy as np


def get_lexicographic_list(n):
    """
    get_lexicographic_list(n)

    Returns a list that contains the first n lexicographically ordered strings
        ["a", "b", "c", ..., "z", "aa", "ab", "ac", ...]

    Parameters
    ----------
    n: int
       number of strings

    Returns 
    -------
    list 

    Example
    -------
    get_lexicographic_list(3) # returns ['a','b','c']
    """
    repetitions = range(n // 26 + 2)
    candidate_tuples = itertools.chain.from_iterable(itertools.product(
        string.ascii_lowercase, repeat=r) for r in repetitions)
    return list(map(lambda x: "".join(x), candidate_tuples))[1:n + 1]


def mode(elements):
    """
    mode(elements)

    Returns the elements with higest number of occurance.


    Parameters
    ----------
    elements: list
        a list of elements to be counted

    Returns
    -------
    list

    Example
    -------
    a = [1,1,2,3,3]
    mode(a) # returns [1,3]
    """
    if not isinstance(elements, list):
        raise TypeError("Not a list")

    if not elements:
        raise ValueError("Empty list provided")

    counts = Counter(elements)
    max_value = max(counts.values())
    return sorted(key for key, value in counts.items() if value == max_value)


def compare(numA, numB):
    """
    compare(numA, numB):

    Compares two numbers. Returns:
        1,  if the first number is greater than the second,
        0,  if they are equal,
       -1, if the first number is smaller than the second.

    Parameters
    ----------
    numA: integer or float
    numB: integer of float

    Returns
    -------
    integer

    """
    if numA > numB:
        return 1
    if numA < numB:
        return -1
    if numA == numB:
        return 0


def ranking_distance(rnkA, rnkB, method="kendalltau"):
    """
    Calculates the distance between two rankings

    """

    available_methods = {"kendalltau"}

    if method not in available_methods:
        raise ValueError("methods: please choose correct measure. \n Available measures:" + str(available_methods))

    candidates = sorted(rnkA)
    pairwise_comparisions = itertools.combinations(candidates, 2)

    if method == "kendalltau":
        distance = 0
        for c1, c2 in pairwise_comparisions:
            compA = compare(rnkA.index(c1), rnkA.index(c2))
            compB = compare(rnkB.index(c1), rnkB.index(c2))

            if compA != compB:
                distance += 1
        return distance


# kendall tau
# stackexchange
# https://stats.stackexchange.com/questions/168602/whats-the-kendall-taus-distance-between-these-2-rankings


def calculate_rank(vector):
    a = {}
    rank = 0
    for num in sorted(vector):
        if num not in a:
            a[num] = rank
            rank = rank + 1
    return [a[i] for i in vector]


def convert_condensed(voters):
    """
    This functions gets a list of voters and convert in each voter preferences in condensed string form. 

    Example:
    list_of_voters = [["a","b","c","d"],["b","a","c","d"]]

    convert_condensed(list_of_voters)
    ## Output: ['abcd', 'bacd']
    """
    return ["".join(voter) for voter in voters]


# This is nice, it might be useful
# list(itertools.combinations(list("abcd"),4))


def all_preferences(candidates, concentrate=False):
    """
    Generates all possible preferences given a list of candidates
    """
    permutations_tuple = list(itertools.permutations(candidates))
    permutations_list = list(map(list, list(permutations_tuple)))
    if concentrate:
        return convert_condensed(permutations_list)
    else:
        return permutations_list


def all_profiles(candidates, num_voters):
    profile_list = []
    prefs = all_preferences(candidates)
    profile_feed = list(itertools.product(prefs, repeat=num_voters))

    for p in profile_feed:
        profile_list.append(Profile(list(p)))

    return profile_list


def filter_unique(voterlist):
    unique_voter_list = []

    for v in voterlist:
        if not v in unique_voter_list:
            unique_voter_list.append(v)

    return unique_voter_list


def append_to_profile_list(profile, profile_list):
    for p in profile_list:
        if p == profile:
            return

    profile_list.append(profile)


def filter_unique_profile(profile_list):
    new_profile_list = []

    for p in profile_list:
        append_to_profile_list(p, new_profile_list)

    return new_profile_list


def remove_if_exists(profile, profile_list):
    try:
        profile_list.remove(profile)
    except:
        pass


def print_profile_list(profile_list):
    for p in profile_list:
        p.print_full()


def generate_mallows_culture_old(true_ordering, sigma, distance_weight=1, concentrate=False):
    preferences = all_preferences(true_ordering, concentrate=concentrate)
    kemeny_distances = np.array([ranking_distance(p, true_ordering) for p in preferences])
    kemeny_distances_weighted = kemeny_distances ** distance_weight
    probabilities = (1 / (kemeny_distances_weighted * sum(kemeny_distances_weighted))) * (1 - sigma)
    probabilities[
        kemeny_distances_weighted == 0] = sigma  # replace the zero distance ordering with sigma (assuming there is only one)
    return [list(preferences), list(probabilities)]


def get_mallows_normalization_constant(number_of_alternatives, dispersion_parameter):
    # Normalization constant is Z.
    normalization_constant = 1
    for j in range(1, number_of_alternatives):
        dispersionoverdistance = [dispersion_parameter ** j for j in range(0, j + 1)]
        sum_of_dispersionoverdistance = sum(dispersionoverdistance)
        normalization_constant *= sum_of_dispersionoverdistance
    return normalization_constant


# def get_transformed_mallows_normalization_constant(number_of_alternatives, dispersion_parameter, transformation_parameter):
#    # Normalization constant is Z.
#    normalization_constant = 1
#    for j in range(1,number_of_alternatives+1):
#        dispersionoverdistance = [dispersion_parameter ** (j ** np.exp(transformation_parameter)) for j in range(0,j)]
#        sum_of_dispersionoverdistance = sum(dispersionoverdistance)
#        normalization_constant *= sum_of_dispersionoverdistance
#    return normalization_constant

def get_transformed_mallows_normalization_constant(dispersion_parameter, transformation_parameter, kemeny_distances):
    normalization_constant = sum(
        dispersion_parameter ** (k ** np.exp(transformation_parameter)) for k in kemeny_distances)
    return normalization_constant


def mallows_pdf(distance, number_of_alternatives, dispersion_parameter):
    likelihood = dispersion_parameter ** distance
    probability = likelihood / get_mallows_normalization_constant(number_of_alternatives, dispersion_parameter)
    return probability


# def transformed_mallows_pdf(distance, number_of_alternatives, dispersion_parameter, transformation_parameter):
#    likelihood = dispersion_parameter ** (distance ** np.exp(transformation_parameter))
#    probability = likelihood / get_transformed_mallows_normalization_constant(number_of_alternatives, dispersion_parameter, transformation_parameter)
#    return probability

def transformed_mallows_pdf(distance, number_of_alternatives, dispersion_parameter, transformation_parameter,
                            kemeny_distances):
    likelihood = dispersion_parameter ** (distance ** np.exp(transformation_parameter))
    probability = likelihood / get_transformed_mallows_normalization_constant(dispersion_parameter,
                                                                              transformation_parameter,
                                                                              kemeny_distances)
    return probability


def generate_mallows_culture(reference_rank, dispersion_parameter, concentrate=False):
    number_of_alternatives = len(reference_rank)
    preferences = all_preferences(reference_rank, concentrate=concentrate)
    kemeny_distances = np.array([ranking_distance(p, reference_rank) for p in preferences])
    probabilities = [mallows_pdf(d, number_of_alternatives, dispersion_parameter) for d in kemeny_distances]
    return [list(preferences), list(probabilities), list(kemeny_distances)]


def generate_transformed_mallows_culture(reference_rank, dispersion_parameter, transformation_parameter=0,
                                         concentrate=False):
    number_of_alternatives = len(reference_rank)
    preferences = all_preferences(reference_rank, concentrate=concentrate)
    kemeny_distances = np.array([ranking_distance(p, reference_rank) for p in preferences])
    probabilities = [transformed_mallows_pdf(d, number_of_alternatives, dispersion_parameter, transformation_parameter,
                                             kemeny_distances)
                     for d in kemeny_distances]
    # probabilities = [transformed_mallows_pdf(d, number_of_alternatives, dispersion_parameter, transformation_parameter) for d in kemeny_distances]
    return [list(preferences), list(probabilities), list(kemeny_distances)]


def make_dictionary(pref1, pref2):
    return dict(zip(pref1, pref2))


def create_all_mappings(candidates):
    # This creates al mappings from candidate lists. I will use it to generate candidate permutations
    all_prefs = all_preferences(candidates)
    list_of_mappings = []

    for p in all_prefs:
        list_of_mappings.append(make_dictionary(candidates, p))

    return list_of_mappings


class Profile():

    def __init__(self, voters=None):
        if voters:
            self.set_voters(voters)
        else:
            self.voters = None
            self.candidates = None  # added because of approval voting

    def __getitem__(self, voter_no):
        return self.voters[voter_no]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.num_voters:
            next_voter = self.voters[self.n]
            self.n += 1
            return next_voter
        else:
            raise StopIteration

    def __eq__(self, other):
        # equality check
        if isinstance(other, list):
            return self.voters == other

        if isinstance(other, Profile):
            return self.voters == other.voters

    def __str__(self):
        if self.voters:
            term_rows, term_columns = list(map(int, (os.popen('stty size', 'r').read().split())))

            max_length = len(max(self.voters[0], key=len))
            justify_length = max_length + 3

            voters_printable = str(self.num_candidates) + " candidates, " + str(self.num_voters) + " voters \n"
            voters_printable += "Profile: " + str(self.print_summary()) + "\n"
            if self.num_voters * justify_length <= term_columns:
                voters_printable += "\n"

                voters_printable += "".join(
                    [("[" + str(item) + "]").ljust(justify_length) for item in range(self.num_voters)])
                voters_printable += "\n"
                for i in range(self.num_candidates):
                    for j in range(self.num_voters):
                        voters_printable += self.voters[j][i].ljust(justify_length)
                    voters_printable += "\n"
            return voters_printable
        else:
            return "Empty profile"

    def __repr__(self):
        return self.__str__()

    def print_full(self):
        term_rows, term_columns = list(map(int, (os.popen('stty size', 'r').read().split())))

        max_length = len(max(self.voters[0], key=len))
        justify_length = max_length + 3

        voters_printable = str(self.num_candidates) + " candidates, " + str(self.num_voters) + " voters \n"
        voters_printable += "Profile: " + str(self.print_summary()) + "\n\n"
        if True:

            voters_printable += "".join(
                [("[" + str(item) + "]").ljust(justify_length) for item in range(self.num_voters)])
            voters_printable += "\n"
            for i in range(self.num_candidates):
                for j in range(self.num_voters):
                    voters_printable += self.voters[j][i].ljust(justify_length)
                voters_printable += "\n"

        print(voters_printable)

    def set_voters(self, voter_list):
        self.voters = voter_list
        self.num_voters = len(self.voters)
        self.set_candidates(sorted(self.voters[0]))

    def set_candidates(self, candidates):
        if isinstance(candidates, list):
            self.candidates = sorted(candidates)
        elif isinstance(candidates, float) or isinstance(candidates, int):
            self.candidates = get_lexicographic_list(candidates)
        self.num_candidates = len(self.candidates)

    def generate_uniform_voters(self, candidate_list, num_voters):
        self.num_voters = num_voters
        self.set_candidates(candidate_list)
        self.voters = [random.sample(self.candidates, len(self.candidates)) for _ in range(num_voters)]

    def generate_mallows_voters(self, candidate_list, num_voters, dispersion_parameter, transformation_parameter=0):
        self.num_voters = num_voters
        self.set_candidates(candidate_list)
        orders, probs, _ = generate_transformed_mallows_culture(candidate_list, dispersion_parameter,
                                                                transformation_parameter)
        np_orders = np.array(orders)
        self.voters = np_orders[np.random.choice(len(orders), num_voters, p=probs)].tolist()

    def generate_mistaken_truth_voters(self, candidate_list, num_voters, stdev):
        self.num_voters = num_voters
        self.set_candidates(candidate_list)

        new_voters = []
        for v in range(num_voters):
            norms = np.array(list(range(len(candidate_list)))) + np.random.normal(0, stdev, len(candidate_list))
            norm_ranks = calculate_rank(norms)
            new_voter = np.take(candidate_list, norm_ranks)
            new_voters.append(list(new_voter))
        self.voters = new_voters

    def create_voter_permutations(self, with_myself=False):
        permutation_list = []
        voter_permutations = list(itertools.permutations(self.voters))
        unique_voter_permutations = filter_unique(voter_permutations)
        for p in unique_voter_permutations:
            if not list(p) == self.voters or with_myself:
                permutation_list.append(Profile(list(p)))
        return permutation_list

    def rename_candidates(self, dictionary):
        # I used this numpy implementation because I had it already. Later we should decide if we'd like to switch to numpy
        voters = np.array(self.voters)
        new_voters = np.copy(voters)
        for i in range(np.shape(voters)[0]):
            for j in range(np.shape(voters)[1]):
                new_voters[i, j] = dictionary[voters[i, j]]
        return new_voters.tolist()

    def create_candidate_permutations(self, with_myself=False):
        permutation_list = []

        candidate_permutations = []
        mappings = create_all_mappings(self.candidates)

        for m in mappings:
            candidate_permutations.append(self.rename_candidates(m))

        unique_candidate_permutations = filter_unique(candidate_permutations)

        for p in unique_candidate_permutations:
            if not list(p) == self.voters or with_myself:
                permutation_list.append(Profile(list(p)))
        return permutation_list

    def create_vc_permutations(self, with_myself=False):
        # Combination of both. First gets voters perms then candidate
        permutation_list = []
        final_list = []
        voter_permutations = list(itertools.permutations(self.voters))
        unique_voter_permutations = filter_unique(voter_permutations)

        for p in unique_voter_permutations:
            permutation_list.append(Profile(list(p)))

        for profile in permutation_list:
            final_list.extend(profile.create_candidate_permutations())

        return permutation_list + final_list

    def get_voter(self, voter_index):
        return self.voters[voter_index]

    def get_voters(self, concentrate=False):
        if concentrate:
            return convert_condensed(self.voters)
        else:
            return self.voters

    def summarize_voters(self):
        return dict(Counter(convert_condensed(self.voters)))

    def print_summary(self):
        summary = self.summarize_voters()
        sortedkeys = sorted(summary, key=str.lower)
        sortedlist = [k + ":" + str(summary[k]) + " | " for k in sortedkeys]
        return "".join(sortedlist)

    def dictator(self, dictator_index=None):
        # print(self.num_voters)
        if dictator_index is not None:
            if dictator_index <= self.num_voters:
                return self.voters[dictator_index][0]
            else:
                print("Invalid dictator index")
                return None
        else:
            return list(self.voters[random.randrange(self.num_voters)][0])

    def plurality(self):
        top_votes = [self.voters[i][0] for i in range(self.num_voters)]
        return mode(top_votes)

    def majority(self):
        winners = []
        top_votes = [self.voters[i][0] for i in range(self.num_voters)]
        counts = Counter(top_votes)
        plurality_winner = max(counts)
        if counts[plurality_winner] >= (0.5 * self.num_voters):
            winners.append(plurality_winner)

        return winners

    def approval(self, acceptable_rank=None):

        if acceptable_rank is None:
            acceptable_rank = [random.randint(1, self.num_candidates - 1) for iter in range(self.num_voters)]
        else:
            acceptable_rank = [acceptable_rank] * self.num_voters

        approved_candidates = [self.voters[i][0:acceptable_rank[i]] for i in range(self.num_voters)]
        approvals = [j for i in approved_candidates for j in i]  # concatenate list of lists
        #        print(acceptable_rank)
        #        print(approved_candidates)

        return mode(approvals)

    def condorcet(self):
        pairwise_comp_matrix = np.zeros((self.num_candidates, self.num_candidates))

        for voter in self.voters:
            for can1 in range(len(self.candidates)):
                for can2 in range(len(self.candidates)):
                    if can1 == can2:
                        pairwise_comp_matrix[can1, can2] = np.nan
                    else:
                        comparision = int(voter.index(self.candidates[can1]) < voter.index(self.candidates[can2]))
                        pairwise_comp_matrix[can1, can2] += comparision

        pairwise_positive_matrix = pairwise_comp_matrix - self.num_voters / 2

        winners = []

        for c, candidate in enumerate(self.candidates):

            if np.all(np.delete(pairwise_positive_matrix[c, :], c) > 0):
                winners.append(candidate)
        # print(pairwise_comp_matrix)
        return winners

    def generate_borda_rule(self, point_distribution):
        """
        This function gets a string and returns the corresponding list of points used in the Borda-count rule.
        :param point_distribution: string, valid inputs: "borda_0", "borda_1", "dowdall"
        :return: a list
            -"borda_0": returns [n-1,n-2,...,0]
            -"borda_1": returns [n,n-1,...,1]
            -"dowdall": returns [1, 1/2, 1/3, ..., 1/n]
            (n = len(self.candidates))
        """
        if point_distribution == "borda_0":
            points_list = [len(self.candidates) - i for i in range(1, len(self.candidates) + 1)]
        elif point_distribution == "borda_1":
            points_list = [len(self.candidates) - i for i in range(0, len(self.candidates))]
        elif point_distribution == "dowdall":
            points_list = [1 / i for i in range(1, len(self.candidates) + 1)]
        return points_list

    def borda(self, points_list=None):
        """
        Elects a winner according to the weighted rankings of the voters.
        :param points_list: a list (for example the output of generate_borda_rule(self, point_distribution))
        :return: a string (the name of the winner of the election)
        """

        voters = np.array(self.voters)
        if points_list is None:
            points_list = self.generate_borda_rule("borda_0")

        cumulated = Counter(voters[:, 0])
        for key in cumulated:
            cumulated[key] *= points_list[0]
        for v in range(1, len(voters[0][:])):
            count = Counter(voters[:, v])
            for key in count:
                count[key] *= points_list[v]
            cumulated += count
        max_value = max(cumulated.values())
        return sorted(key for key, value in cumulated.items() if value == max_value)

    def elect(self, rule):
        if rule == "dictator":
            return self.dictator()

        if rule == "condorcet":
            return self.condorcet()

        if rule == "approval":
            return self.approval()

        if rule == "plurality":
            return self.plurality()

        if rule == "borda":
            return self.borda()
