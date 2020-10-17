import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence_list = []
    label_list = []
    months = ["Jan","Feb","Mar","Apr","May","June","Jul","Aug","Sep","Oct","Nov","Dec"]
    returning = ["New_Visitor", "Returning_Visitor", "Other"]
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            evidence = []
            for idx in range(len(row)):
                if(idx in [0,2,4,11,12,13,14]):
                    evidence.append(int(row[idx]))
                elif(idx in [1,3,5,6,7,8,9]):
                    evidence.append(float(row[idx]))
                elif(idx is 10):
                    evidence.append(int(months.index(row[idx])))
                elif(idx is 15):
                    evidence.append(int(returning.index(row[idx])))
                elif(idx is 16):
                    if (row[16] == "TRUE"):
                        evidence.append(1)
                    else:
                        evidence.append(0)
            evidence_list.append(evidence)
            
            if (row[17] == "TRUE"):
                label_list.append(1)
            else:
                label_list.append(0)            
            

    # print("evidence")
    # for i in range (10):
    #     print(evidence_list[i])
    # print("labels")
    # for i in range (10):
    #     print(label_list[i])
    # print("data length")
    # print(len(evidence_list))

    return (evidence_list, label_list)
    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    # Fit model
    model.fit(evidence, labels)
    # X_training, X_testing, y_training, y_testing = train_test_split(
    # evidence, labels, test_size=0.4
    # )

    return model
    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # print(labels)
    sensitivity = 0
    specificity = 0
    num_pos = 0
    num_pos_right = 0
    num_neg = 0
    num_neg_right = 0
    idx = 0
    for (L,P) in zip(labels, predictions):
        # print("Lable : " + str(labels[idx]) + ". Pred : " + str(predictions[idx]))
        if(L != labels[idx] or P != predictions[idx]):
            input()
        idx += 1
        if(L == 1):
            # print("L : " + str(L) + ". P : " + str(P))
            num_pos += 1
            if(P == 1):
                num_pos_right += 1
        else:
            num_neg += 1
            if(P == 0):
                num_neg_right += 1
    if (num_pos != 0):
        sensitivity = num_pos_right/num_pos
    if (num_neg != 0):
        specificity = num_neg_right/num_neg
    # print(num_pos)
    # print(num_pos_right)
    # print(num_neg)
    # print(num_neg_right)
    # input()
    return (sensitivity, specificity)
    # raise NotImplementedError


if __name__ == "__main__":
    main()
