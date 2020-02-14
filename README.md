# Vietnamese Speech to Text - Wavenet

## Python 2.7

### Dependencies: 
* Flask==0.12.2
* gunicorn==19.7.1
* librosa==0.5.0
* numpy==1.14.2
* pylint==1.8.4
* scikit-learn==0.19.1
* scipy==1.0.1
* six==1.11.0
* sugartensor==1.0.0.2
* tensorflow==1.0.0
* Werkzeug==0.14.1
* Scrapy==1.5.0

### Data processing: 
1. **Data sources**:
    * [vais](https://vais.vn/)
    * [vivos](https://ailab.hcmus.edu.vn/vivos)
    * KTSpeech ([Chị Đào Chị Lý](http://www.sachnoionline.com/nghe-sach/chi-dao-chi-ly-nguoi-doc-thuy-tien), [Kẻ làm người chịu](http://www.sachnoionline.com/nghe-sach/ke-lam-nguoi-chiu-nguoi-doc-thuy-tien))
    * audiobook ([Trúng số độc đắc](http://www.sachnoionline.com/nghe-sach/trung-so-doc-dac-nguoi-doc-thuy-tien))
    * [King-ASR-M-008-Promotion](http://kingline.speechocean.com/exchange.php?id=19296&act=view)
2. **Processed data**:
    * Train set: 45182 samples ( > 41hrs) 
    * Test set: 5006 samples ( > 4hrs)
3. **Scripts**:
    * `gather_data.py`: Gathering all data from above sets then rearranging and preprocessing them. After gathering, data will be stored in `/data processing/asset/data/FINAL_DATA` folder.
    * `preprocess.py`: Preprocessing gathered data to get mfcc features. After preprocessing, preprocessed data will be stored in `/data processing/asset/data/preprocess` folder.
4. **Preprocessing**:
    * Run this to gather data and preprocess them (You might need to modify codes):  
        ```
        /data processing$ python gather_data.py
        ```
    * Or run this if you've already have the `FINAL_DATA` to preprocess them:  
        ```
        /data processing$ python preprocess.py
        ```

### Training:
1. **Architecture**:
    ![Architecture](/images/architecture.png)
2. **Training**:
    * Put `preprocess` (preprocessed data) folder in `/training/asset/data`.
    * You can modify codes in `train.py` and `model.py` to run in your case.
    * Before training, remember to adjust the `max_ep` (max epoch) parameter in `train.py` (default learning rate is 0.001, you can modify learning rate by the `lr` parameter in `train.py`).
    * Run this to begin training (trained models will be stored in `/training/asset/train`):  
        ```
        /training$ python train.py
        ```
    * Run this to test your latest model with the preprocessed test set (this will create a `loss.csv` file to store testing loss information and store the best model in the `best_model` folder):  
        ```
        /training$ python test.py
        ```

### Language Model:
1. **Data source**: [VnExpress](https://vnexpress.net/)
2. **Categories**: Thời sự, Góc nhìn, Thế giới, Kinh doanh, Giải trí, Thể thao, Pháp luật, Giáo dục, Sức khỏe, Gia đình, Du lịch, Khoa học, Số hóa, Xe, Cộng đồng, Tâm sự.
3. **Number of articles**: 198,139 
4. **Number of different words**: 147,378 
5. **Total number of words**: 77,907,100 
6. **Top 10 common words**: 
    ![Top 10 common words](/images/top10_common_words_table.png)
7. **Running crawler**:
    * You might need to modify codes in `vnexpress_spider.py` to run in your case.
    * Run this to crawl from listed categories above (500 pages each category, 100 pages for Góc nhìn), this will return a txt file and a csv file in `/language model/crawlers/vnexpress_crawler`:  
        ```
        /language model/crawlers/vnexpress_crawler$ scrapy crawl --nolog vnexpress_spider -o vnexpress.csv -t csv
        ```
8. **Correcting spell**:
    * Put this [VnExpress data](https://drive.google.com/file/d/1WA-LX3AZif_U4NMO2CXWxgJxsrXv82Ol/view?usp=sharing) into `/language model` folder to test the precrawled data with `correct_spell.py`.
    * You might need to modify codes in `correct_spell.py` to test the language model.

### Web App:
1. **Trained Model**:
    * Epoch: 20 
    * Step: 59283 
    * Training loss: 11.84 
    * Testing loss: 19.09 
2. **Running Web App**:
    * Put this [VnExpress data](https://drive.google.com/file/d/1WA-LX3AZif_U4NMO2CXWxgJxsrXv82Ol/view?usp=sharing) into `/web app` folder to run the Web App.
    * Run this to open the Web App on your localhost, you can test our model there:  
        ```
        /web app$ FLASK_APP=app.py flask run
        ```
3. **Heroku Web App**:
    * You can find our Web App here: https://thesis-vnmese-s2t-api-heroku.herokuapp.com/
    * But due to the lack of memory on our Heroku server, size of the language model using on the site is much smaller than the one running on your localhost here.

### Future Works:
* **Language Model**: Upgrading from single word to compound word.
* **Model libraries**: Upgrading to fit with newer version of libraries.
* **Model Architecture**: Modifying the model architecture to get better result.

### References:
1. [Speech-to-Text-WaveNet : End-to-end sentence level English speech recognition using DeepMind's WaveNet](https://github.com/buriburisuri/speech-to-text-wavenet)
2. [WaveNet: A Generative Model for Raw Audio](https://arxiv.org/abs/1609.03499)

### Citation:
```
Kim and Park. Speech-to-Text-WaveNet. 2016. GitHub repository. https://github.com/buriburisuri/.
```
