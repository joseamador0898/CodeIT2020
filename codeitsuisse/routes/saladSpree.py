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


    contiguous_shops = []
    #Check each street
    for street in street_map:
        #Skip if street is less than number of salads
        if len(street) < num_salads:
            continue
        #Use helper stack 
        helper_stack = []
        for i in range(len(street)):
            #
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




