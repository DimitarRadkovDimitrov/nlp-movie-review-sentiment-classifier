import sys
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score
from numpy import average
from warnings import simplefilter
from data_preprocessor import prepare_data_for_feature_one, prepare_data_for_feature_two

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

def test_feature_one(feature_one_all_reviews):
    print("FEATURE 1 - TEST")
    print("----------------")

    x_train_data, x_test_data, x_train_labels, x_test_labels = train_test_split(
        feature_one_all_reviews.data, 
        feature_one_all_reviews.target, 
        test_size=0.15, 
        stratify=feature_one_all_reviews.target)

    folds = get_k_folds(x_train_data, x_train_labels, 5)
    
    print("ML Classifier 1 - Naive Bayes Multinomial")
    best_feature_for_NB = get_best_feature_size_for_classifier(0, folds, x_test_data, x_test_labels)
    print("Best feature size = %d, f-measure with test folds: %f\n" % (best_feature_for_NB['feature_size'], best_feature_for_NB['test_result']))

    print("ML Classifier 2 - Support Vector Machine")
    best_feature_for_SDG = get_best_feature_size_for_classifier(1, folds, x_test_data, x_test_labels)
    print("Best feature size = %d, f-measure with test folds: %f\n" % (best_feature_for_SDG['feature_size'], best_feature_for_SDG['test_result']))

    print("ML Classifier 3 - K Nearest Neighbours")
    best_feature_for_KNN = get_best_feature_size_for_classifier(2, folds, x_test_data, x_test_labels)
    print("Best feature size = %d, f-measure with test folds: %f\n" % (best_feature_for_KNN['feature_size'], best_feature_for_KNN['test_result']))

def test_feature_two(feature_two_all_reviews):
    print("FEATURE 2 - TEST")
    print("----------------")

    x_train_data, x_test_data, x_train_labels, x_test_labels = train_test_split(
        feature_two_all_reviews.data, 
        feature_two_all_reviews.target, 
        test_size=0.15, 
        stratify=feature_two_all_reviews.target)

    folds = get_k_folds(x_train_data, x_train_labels, 5)
    
    print("ML Classifier 1 - Naive Bayes Multinomial")
    best_feature_for_NB = get_best_feature_size_for_classifier(0, folds, x_test_data, x_test_labels)
    print("Best feature size = %d, f-measure with test folds: %f\n" % (best_feature_for_NB['feature_size'], best_feature_for_NB['test_result']))

    print("ML Classifier 2 - Support Vector Machine")
    best_feature_for_SDG = get_best_feature_size_for_classifier(1, folds, x_test_data, x_test_labels)
    print("Best feature size = %d, f-measure with test folds: %f\n" % (best_feature_for_SDG['feature_size'], best_feature_for_SDG['test_result']))

    print("ML Classifier 3 - K Nearest Neighbours")
    best_feature_for_KNN = get_best_feature_size_for_classifier(2, folds, x_test_data, x_test_labels)
    print("Best feature size = %d, f-measure with test folds: %f\n" % (best_feature_for_KNN['feature_size'], best_feature_for_KNN['test_result']))


def get_k_folds(training_data, training_labels, num_of_folds):
    kf = KFold(n_splits=num_of_folds)
    folds = []

    for train_index, test_index in kf.split(training_data):
        fold = {}
        fold['train_data'] = [training_data[i] for i in train_index]
        fold['train_labels'] = [training_labels[i] for i in train_index]
        fold['test_data'] = [training_data[i] for i in test_index]
        fold['test_labels'] = [training_labels[i] for i in test_index]
        folds.append(fold)

    return folds
    
def get_best_feature_size_for_classifier(classifier, folds, held_out_data, held_out_labels):
    result_dict = {}
    best_validation_result = 0

    i = 500
    while i <= 3000:
        pipeline = build_feature_pipeline(classifier, i)
        results = get_cross_validation_performance(folds, pipeline, held_out_data, held_out_labels)
        print("Validation set f-measure for feature size = %d: %f" % (i, results[0]))

        if results[0] > best_validation_result:
            best_validation_result = results[0]
            result_dict['test_result'] = results[1]
            result_dict['feature_size'] = i
        i += 500
    return result_dict    

def build_feature_pipeline(classifier, feature_size):
    feature_pipeline = None

    if classifier == 0:
        feature_pipeline = Pipeline([
            ('vect', CountVectorizer()), 
            ('chisq', SelectKBest(score_func=chi2, k=feature_size)),
            ('clf', MultinomialNB())])
    elif classifier == 1:
        feature_pipeline = Pipeline([
            ('vect', CountVectorizer()), 
            ('chisq', SelectKBest(score_func=chi2, k=feature_size)), 
            ('clf', SGDClassifier(
                loss='hinge', 
                penalty='l2',
                alpha=1e-3, 
                random_state=42,))])
    else:
        feature_pipeline = Pipeline([
            ('vect', CountVectorizer()), 
            ('chisq', SelectKBest(score_func=chi2, k=feature_size)),
            ('clf', KNeighborsClassifier(n_neighbors=5))])

    return feature_pipeline

def get_cross_validation_performance(folds, pipeline, validation_set_data, validation_set_labels):
    validation_f1_vals = []
    test_f1_vals = []

    for fold in folds:
        pipeline.fit(fold['train_data'], fold['train_labels'])

        #test with validation set
        predicted_val_set = pipeline.predict(validation_set_data)
        validation_f1_vals.append(f1_score(validation_set_labels, predicted_val_set, "weighted"))

        #test with test data
        predicted_test_set = pipeline.predict(fold['test_data'])
        test_f1_vals.append(f1_score(fold['test_labels'], predicted_test_set, "weighted"))

    average_f1_validation = average(validation_f1_vals)
    average_f1_test = average(test_f1_vals)
    return (average_f1_validation, average_f1_test)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pipenv run python " + sys.argv[0] + " <review_folder_f1> <review_folder_f2>")
        exit()
    
    feature_one_all_reviews = load_files(sys.argv[1])
    feature_two_all_reviews = load_files(sys.argv[2])
    
    test_feature_one(feature_one_all_reviews)
    test_feature_two(feature_two_all_reviews)