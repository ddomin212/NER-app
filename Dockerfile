FROM python:3.10.7
COPY . /app
WORKDIR /app
RUN pip install --upgrade revChatGPT
RUN pip install -r requirements.txt
RUN mkdir -p /root/.kaggle
COPY kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json
ENV PAGE_SECRET YOUR_PAGE_SECRET
ENV PORT 5000
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app --timeout 600