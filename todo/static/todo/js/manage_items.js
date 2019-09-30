const csrftoken = Cookies.get('csrftoken');

const formToJSON = elements => [].reduce.call(elements, (data, element) => {
  if (element.name === "") {
    return data;
  }
  data[element.name] = element.type !== "checkbox" ? element.value : element.checked;

  return data;
}, {});

const handleError = (form, error) => {
  let errorDiv = document.createElement('div');
  errorDiv.className = "non-field-errors";

  let errorMessageDiv = document.createElement('div');
  errorMessageDiv.classList.add('alert', 'alert-danger');
  errorMessageDiv.setAttribute('role', 'alert');
  errorMessageDiv.textContent = error;

  errorDiv.append(errorMessageDiv);

  form.parentElement.insertBefore(errorDiv, form);
};

const submitFormData = async (url, method, data, form) => {
  try {
    const response = await fetch(url, {
      method: method,
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      }
    });
    return await response.json();
  } catch (error) {
    handleError(form, error);
  }
};

const handleAddItemFormSubmit = event => {
  event.preventDefault();

  const data = formToJSON(addItemForm.elements);

  submitFormData(addItemForm.action, addItemForm.method, data, addItemForm).then(response => {
    if (!response) {
      return;
    }
    if (response.hasOwnProperty('text')) {
      let newItem = document.createElement('li');

      newItem.textContent = response.text;

      items.appendChild(newItem);
    } else {
      handleError(addItemForm, response.detail);
    }
  });
};

const items = document.getElementById('id-todo-items');
const addItemForm = document.getElementById('id-add-item-form');

addItemForm.addEventListener('submit', handleAddItemFormSubmit);
