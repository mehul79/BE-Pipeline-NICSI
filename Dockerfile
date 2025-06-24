FROM apache/airflow:2.9.2-python3.9

# Copy requirements file as root
COPY requirements.txt /opt/airflow/requirements.txt

# Switch to airflow user
USER airflow

# Modify requirements file
RUN sed -i '/^model1=/d' /opt/airflow/requirements.txt

# Upgrade pip and install Cython
# RUN pip install --upgrade pip && pip install --no-cache-dir Cython

# Install packages from requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Attempt to install model1 separately
RUN pip install --no-cache-dir model1==1.0.4.8 || echo "Failed to install model1"



# Rename http.py if it exists
# RUN if [ -f /opt/airflow/http.py ]; then mv /opt/airflow/http.py /opt/airflow/custom_http.py; fi

# Ensure the standard library takes precedence
ENV PYTHONPATH="/usr/local/lib/python3.9:/usr/local/lib/python3.9/lib-dynload:/usr/local/lib/python3.9/site-packages:${PYTHONPATH}:/opt/airflow"

WORKDIR /opt/airflow