# NK Artificial Intelligence

Welcome to NKIA or NKAI in English. This project is used to categorize products based on its caracteristics, there is 29 different classes of food products. Another usage is to distinguish between food and non-food products.

## Requirements

- Install requirements:
  - ```pip install -r requirements.txt --user```

- Install NLTK stopwords:
  - ```python -m nltk.downloader stopwords```

## Usage

- Import classify class:
    - ``` from nkia.ml.classify_products import ClassifyProducts as cp ``` 
- Predict product class:
    - ```cp().inference_from_category_model(product_name=['frozen fish'])```
    - *Returns*: String containing the predicted class name
- Parameters:
    - ``` inference_from_category_model(ingredients=[''], allergics=[''], description=[''], product_name=['']) ```
    - All the parameters must be in a single string format.
- Predict if product is a food or not:
    - ```cp().inference_from_food_model(product_name=['chocolate cake'])```
    - *Returns*: String 'food' or 'not food'
    - **Note**: Food classifier just has the product name as parameter.

## Examples

- ```cp().inference_from_category_model(ingredients=['sugar salt vanilla orange'], allergics=['peanuts'], description=['this is an awesome product, hummmm'], product_name=['very delicious candy']) ```
