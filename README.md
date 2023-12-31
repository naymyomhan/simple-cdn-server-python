# Simple-CDN-Server 💾

<a href="https://www.python.org/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/python-original.svg" alt="Python" height="50" /></a>  <a href="https://flask.palletsprojects.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/flask.png" alt="Flask" height="50" /></a>

 A Python project that aims to provide a simple Content Delivery Network (CDN) server solution.


## Prerequisites
Before you begin, ensure you have the following installed on your machine:
- Python (preferably Python 3.x)
- Git


### Example Usage with Axios

Here's a basic example of making a request to get presigned key:

```javascript

  const apiUrl = 'http://192.168.1.123:80/presign/request';

  const requestBody = {
    file_name: 'image_name.png',
    file_path: 'Post'
  };

  axios.post(apiUrl, requestBody)
    .then(response => {
      console.log('API Response:', response.data);
      // Handle the response data
    })
    .catch(error => {
      console.error('Error:', error.message);
      // Handle errors here
    });

```

Example response
```json
   {
    "success": true,
    "message": "presign key generate successful",
    "data": {
        "key": "780edc78-a0f5-4f51-9182-b3b851d0ca2a",
        "name": "app_6a444a0a-6981-450d-8c9d-b12a7120ae2a_31_12_2023.png"
      }
   }
```


## Setting Up

1.Clone the repository:

   ```bash
   git clone https://github.com/naymyomhan/simple-cdn-server-python
   ```

2.Navigate into the project directory:

   ```bash
   cd simple-cdn-server-python
   ```

3.Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   ```

4.Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5.Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```


