<template>
    <div>
      <h2>Add Task</h2>
      <form @submit.prevent="addTask">
        <input type="text" v-model="newTask.title" placeholder="Title" required>
        <input type="text" v-model="newTask.description" placeholder="Description" required>
        <button type="submit">Add Task</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        newTask: { title: '', description: '' }
      };
    },
    methods: {
        async addTask() {
            try {
            const formData = new FormData();
            formData.append('title', this.newTask.title);
            formData.append('description', this.newTask.description);
                
            const response = await fetch('/tasks/create/', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                this.newTask = { title: '', description: '' }; // Clear input fields
                // Call fetchTasks to update task list
                this.fetchTasks();
            } else {
                console.error('Error adding task:', response.statusText);
            }
            } catch (error) {
            console.error('Error adding task:', error);
            }
        }
    }
  };
  </script>
  
  <style scoped>
  /* Add scoped styles if needed */
  </style>
  