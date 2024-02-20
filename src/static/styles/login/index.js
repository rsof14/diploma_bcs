async function login_user() {
  try {
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    var myHeaders = new Headers();
    myHeaders.append("X-Request-Id", "1");
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", "Bearer {{access_token}}");
    myHeaders.append("Access-Control-Allow-Origin", '*');

    var raw = JSON.stringify({
      "login": login,
      "password": password
    });

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    const response = await fetch("http://localhost:8000/api/v1/auth/login", requestOptions)
      .then(response => response.text())
      .then(result => console.log(result))
      .catch(error => console.log('error', error));

  } catch(err) {
    console.error(`Error: ${err}`);
  }

}