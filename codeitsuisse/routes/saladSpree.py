import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSaladSpree():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    num_salads = data.get("number_of_salads")
    street_map = data.get("salad_prices_street_map")
    contiguous_shops = []
    for street in street_map:
        helper_stack = []
        for i in range(len(street)):
            if street[i] != 'X':
                helper_stack.append(street[i])
            else:
                contiguous = []
                for ele in helper_stack:
                    contiguous.append(helper_stack.pop())
                contiguous_shops.append(contiguous)
    #inputValue = data.get("input");
    min_sum = 0
    for c in contiguous_shops:
        this_sum = minSumContiguous(c,num_salads,len(c))
        if this_sum < min_sum:
            min_sum = this_sum

    result = min_sum
    #result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result);

def minSumContiguous(arr, n, k): 
  
    # k must be greater 
    if (n < k): 
      
        print("Invalid") 
        return -1
      
    # Compute sum of first 
    # window of size k 
    res = 0
    for i in range(k): 
        res += arr[i] 
  
    # Compute sums of remaining windows by 
    # removing first element of previous 
    # window and adding last element of  
    # current window. 
    curr_sum = res 
    for i in range(k, n): 
      
        curr_sum += arr[i] - arr[i-k] 
        res =  min(res, curr_sum) 
  
    return res 



