const csrftoken = Cookies.get('csrftoken');
let headers = {
  'Content-Type': 'application/json',
  'X-CSRFToken': csrftoken
};

var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data: {
    todoItems: null,
    newItem: {},
    errors: []
  },
  methods: {
    addItem: function () {
      this.errors = [];

      if (!this.newItem.hasOwnProperty('text') || this.newItem.text.length === 0) {
        this.errors.push('New todo items must have some text.');
      }

      if (this.errors.length) {
        return;
      }

      this.newItem.todo_list = todoListPk;
      if (!this.newItem.hasOwnProperty('completed')) {
        this.newItem.completed = false;
      }

      fetch(todoItemListApiUrl, {
        method: 'post',
        body: JSON.stringify(this.newItem),
        headers: headers
      })
        .then(response => response.json())
        .then(data => {
          this.todoItems.push(data);
          this.newItem = {};
        })
    },
    updateCompletion: function (item) {
      let url = `${todoItemListApiUrl}${item.pk}/`;

      fetch(url, {
        method: 'put',
        body: JSON.stringify(item),
        headers: headers
      })
        .then(response => response.text())
        .then(responseText => JSON.parse(responseText))
        .then(data => {
          console.log(`Set ${data.text} to ${data.completed ? "complete" : "incomplete"}.`)
        })
    },
    deleteItem: function (item) {
      let url = `${todoItemListApiUrl}${item.pk}/`;

      fetch(url, {
        method: 'delete',
        body: JSON.stringify(item),
        headers: headers
      })
        .then(response => {
          if (response.status === 204) {
            let index = this.todoItems.indexOf(item);
            this.todoItems.splice(index, 1);
          }
        })
    }
  },
  mounted: function () {
    let url = `${todoItemListApiUrl}?todo_list=${todoListPk}`;

    fetch(url, {
      method: 'get',
      headers: headers
    })
      .then(response => response.json())
      .then(data => {
        this.todoItems = data.results;
      })
  }
});
