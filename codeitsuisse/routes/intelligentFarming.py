import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/intelligent-farming', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results_list = []

    for inp in data["list"]:
        result = ""
        gene = inp["geneSequence"]
        count = {'A':0, 'C':0, 'G':0, 'T':0}

        for i in gene:
            count[i] += 1

        pos = {}
        neg = {}
        flg = 0
        if count['C'] >= 2:
            pos['CC'] = count['C']//2
            count['C'] %= 2
        if count['A'] and count['C'] and count['G'] and count['T']:
            pos['ACGT'] = 1
            flg = 1
        neg['A'] = count['A'] - flg
        neg['C'] = count['C'] - flg
        neg['G'] = count['G'] - flg
        neg['T'] = count['T'] - flg

        for key,val in pos.items():
            print(key*val, end='')

        while sum(neg.values()):
            mn = min(2,neg['A'])
            neg['A'] -= mn
            print('A'*mn, end='')
            result = result + ('A'*mn)

            if mn == 0:
                print('C'*neg['C'],end='')
                result = result + ('C'*neg['C'])
                print('G'*neg['G'],end='')
                result = result + ('G'*neg['G'])
                print('T'*neg['T'],end='')
                result = result + ('T'*neg['T'])

                break

            mn = min(1,neg['C'])
            neg['C'] -= mn
            print('C'*mn, end='')
            result = result + ('C'*mn)

            if mn:
                mn = min(2,neg['A'])
                neg['A'] -= mn
                print('A'*mn, end='')
                result = result + ('A'*mn)

            mn = min(1,neg['G'])
            neg['G'] -= mn
            print('G'*mn, end='')
            result = result + 'G'*mn

            if mn:
                mn = min(2,neg['A'])
                neg['A'] -= mn
                print('A'*mn, end='')
                result = result + 'A'*mn

            mn = min(1,neg['T'])
            neg['T'] -= mn
            print('T'*mn, end='')
            result = result + 'T'*mn
        results_list.append(result)
        print(results_list)
        
    for idx,res in enumerate(data["list"]):
         res = results_list[idx]
    
    logging.info("My result :{}".format(result))
    return data




