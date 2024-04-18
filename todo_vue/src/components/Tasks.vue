<template>
    <div>
      <h2>Add Task</h2>
      <div>
        <label for="title">Title:</label>
        <input id="title" type="text" v-model="newTask.title" required>
      </div>
      <div>
        <label for="description">Description:</label>
        <input id="description" type="text" v-model="newTask.description" required>
      </div>
      <div>
        <button @click.prevent="addTask">Add Task</button>
      </div>
  
      <!-- To Do List Section -->
      <div>
        <h2>To Do List</h2>
        <ul>
          <li v-for="task in tasks" :key="task.id">
            {{ task.title }} - {{ task.description }}
            <!-- Include edit and delete buttons if needed -->
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import TaskForm from './TaskForm.vue';
  
  export default {
    components: {
      TaskForm
    },
    data() {
      return {
        tasks: [],
        editingTaskId: null
      };
    },
    mounted() {
      this.fetchTasks();
    },
    methods: {
      async fetchTasks() {
        try {
          const response = await fetch('/tasks/');
          const data = await response.json();
          this.tasks = data.tasks;
          console.log("hello"); // Log the fetched tasks
        } catch (error) {
          console.error('Error fetching tasks:', error);
        }
      },
      async deleteTask(taskId) {
        try {
          const response = await fetch(`/tasks/${taskId}/delete/`, {
            method: 'POST', // Use POST for delete to comply with Django
          });
  
          if (response.ok) {
            this.fetchTasks(); // Refresh task list
          } else {
            console.error('Error deleting task:', response.statusText);
          }
        } catch (error) {
          console.error('Error deleting task:', error);
        }
      },
      editTask(task) {
        this.editingTaskId = task.id;
      },
      cancelEdit() {
        this.editingTaskId = null;
        this.fetchTasks(); // Refresh task list after editing
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add scoped styles if needed */
  </style>
  