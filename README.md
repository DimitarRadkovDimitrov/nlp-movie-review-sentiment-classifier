# Movie Review Sentiment Analysis

Reviewing various classical machine learning methods to determine effectiveness in training model for movie review sentiment analysis. [See details](./Report.pdf).

## Prerequisites

* Install all python package dependencies.
    ```
    pipenv install
    ```

<br>

## Build 

* Compile all java programs.
    ```
    javac DataAnalyzer.java Document.java
    ```

<br>

## Run

* Run data analyzer on movie review data (optional).
    ```
    java DataAnalyzer <positive_review_folder> <negative_review_folder>
    ```

* Run data preprocessor.
    ```
    pipenv run python3 data_preprocessor.py <review_root_folder>
    ```

* Run sentiment analysis test.
    ```
    pipenv run python3 sentiment_analysis_test.py <review_folder_f1> <review_folder_f2>
    ```
