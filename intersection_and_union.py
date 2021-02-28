import joblib
import functools
import operator
from preprocessing import preProcessSentence

# handles AND and AND NOT operations
def intersection_op(pos_list_1,pos_list2, NOT):
    output = list()
    top_1 =0
    top_2 = 0
    comparisons = 0
    #AND NOT scenario retrieve all postings in first and not in second
    if NOT:
        while top_1<len(pos_list_1) and top_2 < len(pos_list2):
            comparisons+=1
            if pos_list_1[top_1] <pos_list2[top_2]:
                output.append(pos_list_1[top_1])
                top_1+=1
            elif pos_list_1[top_1] >pos_list2[top_2]:
                top_2+=1
            else:
                top_1+=1
                top_2+=1
        while top_1 < len(pos_list_1):
            output.append(pos_list_1[top_1])
            top_1+=1
    else:
        while top_1<len(pos_list_1) and top_2 < len(pos_list2):
            comparisons+=1
            if pos_list_1[top_1]==pos_list2[top_2]:
                output.append(pos_list_1[top_1])
                top_1+=1
                top_2+=1
            elif pos_list_1[top_1] <pos_list2[top_2]:
                top_1+=1
            else:
                top_2+=1
    return output,comparisons

# invokes the intersection method
def AND_operator(postings, NOT):
    comparison_accumulator =0
    initial_output = postings[0]
    for posting in postings[1:]:
        output, comparisons = intersection_op(initial_output,posting, NOT)
        comparison_accumulator+=comparisons
    return output, comparison_accumulator

# performs the OR operation also OR NOT is covered as in main method we first perform the NOT operation on the second operand
def Union_op(pos_list_1,pos_list_2, NOT):
    output = list()
    top_1 =0
    top_2 = 0
    comparisons = 0

    while top_1<len(pos_list_1) and top_2 < len(pos_list_2):
        comparisons+=1
        if pos_list_1[top_1]==pos_list_2[top_2]:
            output.append(pos_list_1[top_1])
            top_1+=1
            top_2+=1
        elif top_1<len(pos_list_1) and pos_list_1[top_1] <pos_list_2[top_2]:
            output.append(pos_list_1[top_1])
            top_1+=1
        else:
            output.append(pos_list_2[top_2])
            top_2+=1


    while top_1 < len(pos_list_1):
        output.append(pos_list_1[top_1])
        top_1+=1
    while top_2 < len(pos_list_2):
        output.append(pos_list_2[top_2])
        top_2+=1
    return output,comparisons    

# performs the OR operation
def OR_operator(postings, NOT):
    comparison_accumulator =0
    initial_output = postings[0]
    for posting in postings[1:]:
        output, comparisons = Union_op(initial_output,posting, NOT)
        comparison_accumulator+=comparisons
    return output, comparison_accumulator
if __name__=="__main__":
    inverted_index = joblib.load('inverted_index')
    document_index_map = joblib.load('document_index_map')
    document_index_map_keys = list(document_index_map.keys())
    document_index_map_values = list(document_index_map.values())


    #Makes a set of all document postings
    doc_ids = list(map(lambda x: x[1],inverted_index.values()))
    all_docids = set(functools.reduce(operator.iconcat, doc_ids, []))
    #all_docids = set(document_index_map_values)

    print(all_docids)
    number_of_queries = int(input("Enter number of queries"))
    for query in range(number_of_queries):
        query = str(input("Enter the query with terms separated by space"))
        query = preProcessSentence(query)
        query=' '.join(query)
        print("query terms",query)
        query_terms = query.split(" ")
        operation_sequence = str(input("Enter the operation sequence separated by comma"))
        operators = operation_sequence.split(",")
        output = None
        comparisons_sum = 0
        skip = False
        # if len(list(set(operators)))==1:
        #     query_terms.sort(key=lambda x: len(inverted_index.get(x)[1]))
        #     print("Sorted",query_terms)




        # for each operator in the given list we iterate through them to perform the opertions and obtain final result
        for index,operator in enumerate(operators):
            pos_lists = []
            NOT = False
            
            if "and" in operator.lower():
                if index ==0:
                    pos_list_1 = inverted_index.get(query_terms[index])
                    if not pos_list_1:
                        print("Term not found: {}\nHence, operation has failed".
                              format(query_terms[index]))
                        skip = True
                        break
                    else:
                        pos_list_1 = pos_list_1[1]
                else:
                    # to use the output from applying previous operation
                    pos_list_1  = output
                pos_list_2 = inverted_index.get(query_terms[index+1])
                # covers AND NOT
                if "not" in operator.lower():
                    NOT = True
                    pos_list_2 = pos_list_2[1] if pos_list_2 else []
                else:
                    if not pos_list_2:
                        print("Term not found: {}\nHence, operation has failed".
                                  format(query_terms[index]))
                        skip = True
                        break
                    else:
                        pos_list_2 = pos_list_2[1]
                pos_list_1.sort()
                pos_list_2.sort()
                pos_lists.append(pos_list_1)
                pos_lists.append(pos_list_2)
                output,comparisons = AND_operator(pos_lists, NOT)
                comparisons_sum+=comparisons
                # print("Number of comparisons",comparisons_sum)
                # print("The merged postings are", output)
            elif "or" in  operator.lower():
                if index ==0:
                    pos_list_1 = inverted_index.get(query_terms[index])
                    if not pos_list_1:
                        pos_list_1 = []
                    else:
                        pos_list_1 = pos_list_1[1]
                else:
                    pos_list_1  = output
                pos_list_2 = inverted_index.get(query_terms[index+1])
                if not pos_list_2:
                    pos_list_2 = []
                else:
                    pos_list_2 = pos_list_2[1]
                # covers or not
                if "not" in operator.lower():
                    NOT = True
                    not_items = inverted_index.get(query_terms[index+1])
                    if not_items:
                        not_items = not_items[1]
                    else:
                        not_items = []
                    pos_list_2 = [x for x in all_docids if x not in not_items]
                if not pos_list_2:
                    pos_list_2 = []
                pos_list_1.sort()
                pos_list_2.sort()
                pos_lists.append(pos_list_1)
                pos_lists.append(pos_list_2)
                output,comparisons = OR_operator(pos_lists, NOT)
                comparisons_sum+=comparisons
        # skip scenario is true only if the terms are absent in dictionary
        if not skip:
            print("Number of comparisons",comparisons_sum)
            print("Number of documents matched", len(output))
            print("The retrieved documents are: [", end="")
            for out in output:
                index = document_index_map_values.index(out)
                print(document_index_map_keys[index], end=", ")
            print(']')