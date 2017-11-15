import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

spam_data = pd.read_csv('spam.csv')

spam_data['target'] = np.where(spam_data['target']=='spam',1,0)

X_train, X_test, y_train, y_test = train_test_split(spam_data['text'], 
                                                    spam_data['target'], 
                                                    random_state=0)
def add_feature(X, feature_to_add):
    """
    Returns sparse feature matrix with added feature.
    feature_to_add can also be a list of features.
    """
    from scipy.sparse import csr_matrix, hstack
    return hstack([X, csr_matrix(feature_to_add).T], 'csr')

def predict_eval_spam():
    vect = CountVectorizer(min_df=5, ngram_range=(2,5), analyzer='char_wb').fit(X_train)

    X_train_vectorized = vect.transform(X_train)
    X_test_vectorized = vect.transform(X_test)
    
    length_of_doc = X_train.str.len()
    digit_count = X_train.str.count('\d')
    non_word_char_count = X_train.str.count('\W')
    X_train_vectorized = add_feature(X_train_vectorized, [length_of_doc, digit_count, non_word_char_count])
    
    length_of_doc = X_test.str.len()
    digit_count = X_test.str.count('\d')
    non_word_char_count = X_test.str.count('\W')
    X_test_vectorized = add_feature(X_test_vectorized, [length_of_doc, digit_count, non_word_char_count])
        
    model = LogisticRegression(C=100)
    model.fit(X_train_vectorized, y_train)
    
    predictions = model.predict(X_test_vectorized)

    feature_names = np.array(vect.get_feature_names())
    feature_names = np.append(feature_names, ['length_of_doc', 'digit_count', 'non_word_char_count'])
    
    sorted_coef_index = model.coef_[0].argsort()
    smallest_coef = feature_names[sorted_coef_index[:10]].tolist()
    biggest_coef = feature_names[sorted_coef_index[:-11:-1]].tolist()
    
    return roc_auc_score(y_test, predictions), smallest_coef, biggest_coef