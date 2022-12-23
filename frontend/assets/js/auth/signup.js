function getFormJson() {
  let signupForm = document.querySelector('.signup-form');
  let data = new FormData(signupForm);
  let serializedFormData = serialize(data);
  return JSON.stringify(serializedFormData);
}

function serialize(rawFormData) {
  let result = {};
  for (let [key, value] of rawFormData) {
    let sel = document.querySelectorAll('[name=' + key + ']');
    if (sel.length > 1) {
      if (result[key] === undefined) {
        result[key] = [];
      }
      result[key].push(value);
    } else {
      result[key] = value;
    }
  }
  return result;
}

async function submitSignupData() {
  var myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/json');

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: getFormJson(),
    redirect: 'follow',
  };

  const response = await fetch(SIGNUP_API_URL, requestOptions);
  if (response.status == 200) {
    signupResponse = await response.json();
    window.location.href = LOGIN_FRONTEND_URL;
  } else {
    alert(JSON.stringify(await response.json()));
  }
}
