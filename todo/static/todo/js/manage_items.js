const formToJSON = elements => [].reduce.call(elements, (data, element) => {
  data[element.name] = element.type !== "checkbox" ? element.value : element.checked;

  return data;
}, {});

const handleError = error => {
  let errorDiv = document.createElement('div');
  errorDiv.className = "non-field-errors";

  let errorMessageDiv = document.createElement('div');
  errorMessageDiv.classList.add('alert', 'alert-danger');
  errorMessageDiv.setAttribute('role', 'alert');
  errorMessageDiv.textContent = error;

  errorDiv.append(errorMessageDiv);

  form.parentElement.insertBefore(errorDiv, form);
};

const addItem = async data => {
  let csrftoken = Cookies.get('csrftoken');

  try {
    const response = await fetch(form.action, {
      method: form.method,
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      }
    });
    return await response.json();
  } catch (error) {
    handleError(error);
  }
};

const handleAddItemFormSubmit = event => {
  event.preventDefault();

  const data = formToJSON(form.elements);

  addItem(data).then(response => {
    if (response.text) {
      let newItem = document.createElement('li');

      newItem.textContent = response.text;

      items.appendChild(newItem);
    } else {
      handleError(response.detail);
    }
  });
};

const items = document.getElementById('id-todo-items');
const form = document.getElementById('id-add-item-form');

form.addEventListener('submit', handleAddItemFormSubmit);
