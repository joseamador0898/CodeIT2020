import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSaladSpree():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    num_salads = data.get("number_of_salads")
    street_map = data.get("salad_prices_street_map")
    #num_salads = 3
    #street_map = [["12", "12", "3", "X", "3"], ["23", "X", "X", "X", "3"], ["33", "21", "X", "X", "X"], ["9", "12", "3", "X", "X"], ["X", "X", "X", "4", "5"]]
    contiguous_shops = []
    for street in street_map:
        if len(street) < num_salads:
            continue
        helper_stack = []
        for i in range(len(street)):
            if street[i] != 'X':
                helper_stack.append(street[i])
            else:
                contiguous = []
                if len(helper_stack) < num_salads:
                    helper_stack.clear()
                else:
                    for i in range(len(helper_stack)):
                        contiguous.append(helper_stack.pop())
                    contiguous_shops.append(contiguous)
    # inputValue = data.get("input");
    min_sum = 99999999999
    for c in contiguous_shops:
        if len(c) >= num_salads:
            this_sum = minSumContiguous(c, num_salads, len(c))
            if this_sum < min_sum:
                min_sum = this_sum

    result = min_sum

    logging.info("My result :{}".format(result))
    return json.dumps({'result' : min_sum})

  
def minSumContiguous(arr, n, k):
    # k must be greater
    if (n > k):
        print("Invalid")
        return -1

    # Compute sum of first
    # window of size k
    res = 0
    for i in range(k):
        res += int(arr[i])

        # Compute sums of remaining windows by
    # removing first element of previous
    # window and adding last element of
    # current window.
    curr_sum = res
    for i in range(k, n):
        curr_sum += arr[i] - arr[i - k]
        res = min(res, curr_sum)

    return res




