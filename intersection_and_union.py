


def intersection_op(pos_list_1,pos_list2):
    output = list()
    top_1 =0
    top_2 = 0
    comparisons = 0

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


def AND_operator(postings):
    comparison_accumulator =0
    initial_output = postings[0]
    for posting in postings[1:]:
        output, comparisons = intersection_op(initial_output,posting)
        comparison_accumulator+=comparisons
    return output, comparison_accumulator


def Union_op(pos_list_1,pos_list_2):
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
            top_2+=1
            output.append(pos_list_2[top_2])

    while top_1 < len(pos_list_1):
        output.append(pos_list_1[top_1])
        top_1+=1
    while top_2 < len(pos_list_2):
        output.append(pos_list_2[top_2])
        top_2+=1
    return output,comparisons    

def OR_operator(postings):
    comparison_accumulator =0
    initial_output = postings[0]
    for posting in postings[1:]:
        output, comparisons = Union_op(initial_output,posting)
        comparison_accumulator+=comparisons
    return output, comparison_accumulator
if __name__=="__main__":
    inverted_index = dict()
    terms = ["IR","Deeplearning","hyperbolic"]
    for index,term in enumerate(terms):
        if term not in inverted_index:
            inverted_index[term] = []
        else:
            inverted_index.append(index)

    inverted_index["IR"].extend([3,9])

    inverted_index["Deeplearning"].extend([12,34,3,9])

    inverted_index["hyperbolic"].extend([3,56])

    print("inverted_index",inverted_index)

    #Makes a set of all document postings
    all_docids = set(sum(inverted_index.values(), []))
    
    number_of_queries = int(input("Enter number of queries"))

    for query in range(number_of_queries):
        query = str(input("Enter the query with terms separated by space"))
        query_terms = query.split(" ")
        operation_sequence = str(input("Enter the operation sequence separated by comma"))
        operators = operation_sequence.split(",")
        output = None
        comparisons_sum = 0
        for index,operator in enumerate(operators):
            pos_lists = []

            if "NOT" in operator:
                not_items = inverted_index.get(query_terms[index+1])                
                pos_list_2 = [x for x in all_docids if x not in not_items]
            else:
                pos_list_2 = inverted_index.get(query_terms[index+1])
                
            if "AND" in operator:
                if index ==0:
                    pos_list_1 = inverted_index.get(query_terms[index])
                else:
                    pos_list_1  = output
                print("pos_list_1",pos_list_1)
                #pos_list_2 = inverted_index.get(query_terms[index+1])
                pos_list_1.sort()
                pos_list_2.sort()
                pos_lists.append(pos_list_1)
                pos_lists.append(pos_list_2)
                output,comparisons = AND_operator(pos_lists)
                comparisons_sum+=comparisons
                print("Number of comparisons",comparisons_sum)
                print("The merged postings are", output)
            elif "OR" in  operator:
                        if index ==0:
                            pos_list_1 = inverted_index.get(query_terms[index])
                        else:
                            pos_list_1  = output
                        #pos_list_2 = inverted_index.get(query_terms[index+1])
                        pos_list_1.sort()
                        pos_list_2.sort()
                        pos_lists.append(pos_list_1)
                        pos_lists.append(pos_list_2)
                        output,comparisons = OR_operator(pos_lists)
                        comparisons_sum+=comparisons
                        print("Number of comparisons",comparisons_sum)
                        print("The merged postings are", output)